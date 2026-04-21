"""
DailyPaperProcessor：针对单个日期的论文处理流水线，从 run_pipeline.py 抽出。

逻辑与原 PaperPipeline.run_pipeline() 完全一致，只做结构化搬迁。
每个 step 是独立方法，run() 串联所有步骤。
"""

import os
import json
import shutil
from datetime import datetime, timezone
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from run_pipeline import (
    PaperPipeline,
    PipelineConfig,
    pipeline_debug,
    _set_pipeline_log_path,
    _count_json_files,
    _json_dict_sorted_by_key,
    FOCUS_SECTIONS,
    PROMPT_STEP04_SUMMARY,
    PROMPT_STEP06_DEEP,
)


class DailyPaperProcessor:
    """针对单个日期的论文处理类。持有 PaperPipeline 作为工具层，自身负责流程编排。"""

    def __init__(self, pipeline: PaperPipeline, date_str: str, force_rerun=None):
        assert hasattr(pipeline, 'cfg') and hasattr(pipeline, 'api_key'), "pipeline 必须是 PaperPipeline 实例"
        assert isinstance(date_str, str)
        assert force_rerun is None or isinstance(force_rerun, list)
        if force_rerun is None:
            force_rerun = []
        for step in force_rerun:
            assert isinstance(step, str)

        self.pipeline = pipeline
        self.cfg: PipelineConfig = pipeline.cfg
        self.date_str = date_str
        self.force_rerun = force_rerun

        # 缓存与输出路径
        self.pub_dir = self.cfg.output_pub_dir_fmt.format(date_str=date_str)
        self.pub_img_dir = f"{self.pub_dir}/{self.cfg.pub_images_subdir}"
        self.cache_root = self.cfg.output_cache_dir_fmt.format(date_str=date_str)

        self.step01_hf = f"{self.cache_root}/step01_hf_papers.json"
        self.step03_arxiv_abs = f"{self.cache_root}/step03_arxiv_abs"
        self.step04_summaries_llm = f"{self.cache_root}/step04_summaries_llm"
        self.step05_arxiv_html = f"{self.cache_root}/step05_arxiv_html"
        self.step06_deep_llm = f"{self.cache_root}/step06_deep_llm"
        self.step07b_key_figure_select = f"{self.cache_root}/step07b_key_figure_select"
        self.step08_figure_caption_zh = f"{self.cache_root}/step08_figure_caption_zh"

    def _should(self, step_name: str) -> bool:
        return step_name in self.force_rerun

    # ------------------------------------------------------------------
    # step01：拉取 HF 当日列表
    # ------------------------------------------------------------------
    def step01_fetch_hf(self) -> tuple[OrderedDict, dict]:
        base_info, hf_votes = self.pipeline.fetch_hf_papers(
            self.date_str, self.step01_hf, force_rerun=self._should("step01")
        )
        if not base_info:
            pipeline_debug("step01", "拉取论文列表", "当日无论文，停止")
            return base_info, hf_votes

        for aid in base_info:
            if aid not in hf_votes:
                hf_votes[aid] = 0

        os.makedirs(self.pub_dir, exist_ok=True)
        return base_info, hf_votes

    # ------------------------------------------------------------------
    # step02：抓取 arXiv 摘要页
    # ------------------------------------------------------------------
    def step02_fetch_arxiv_abs(self, base_info: OrderedDict) -> dict:
        details_by_aid = {}
        for aid in tqdm(
            base_info.keys(),
            desc="step02 | arxiv摘要页",
            unit="篇",
        ):
            details_by_aid[aid] = self.pipeline.get_arxiv_details(
                aid, self.step03_arxiv_abs, force_rerun=self._should("step02")
            )
        return details_by_aid

    # ------------------------------------------------------------------
    # step03：板块归类
    # ------------------------------------------------------------------
    def step03_classify(self, base_info: OrderedDict, details_by_aid: dict) -> tuple[OrderedDict, set]:
        focus_sections = OrderedDict((s["name"], []) for s in FOCUS_SECTIONS)
        focus_id_set = set()
        aid_list_unique = list(dict.fromkeys(base_info.keys()))
        total_papers = len(aid_list_unique)
        name_by_key = {s["key"]: s["name"] for s in FOCUS_SECTIONS}
        section_cache_dir = f"{self.cache_root}/step03_sections"

        def _classify_one(aid: str) -> tuple[str, str | None]:
            assert isinstance(aid, str)
            assert aid in base_info
            assert aid in details_by_aid
            assert "title" in base_info[aid]
            assert "abstract" in details_by_aid[aid]
            assert isinstance(base_info[aid]["title"], str)
            assert isinstance(details_by_aid[aid]["abstract"], str)

            pipeline_debug("step03", "板块归类提交", f"论文 aid={aid}")
            section_key = self.pipeline.classify_paper_section(
                base_info[aid]["title"],
                details_by_aid[aid]["abstract"],
                aid,
                section_cache_dir,
                FOCUS_SECTIONS,
                force_rerun=self._should("step03"),
                debug_step="step03",
                debug_title="板块归类",
            )
            return aid, section_key

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(_classify_one, aid): aid for aid in aid_list_unique}
            pbar = tqdm(total=total_papers, desc="step03 | 单篇投票筛选重点", unit="篇")
            try:
                done = 0
                for fut in as_completed(futures):
                    aid = futures[fut]
                    try:
                        aid, section_key = fut.result()
                    except Exception as e:
                        pipeline_debug("step03", "板块归类异常", f"论文 aid={aid} err={type(e).__name__}: {e}")
                        section_key = None

                    done += 1
                    pipeline_debug("step03", "板块归类进度", f"{done}/{total_papers} 论文 aid={aid}")
                    pbar.update(1)

                    if section_key is None:
                        continue
                    assert section_key in name_by_key
                    if aid in focus_id_set:
                        continue
                    focus_id_set.add(aid)
                    focus_sections[name_by_key[section_key]].append(aid)
            finally:
                pbar.close()

        for _sec_name, ids in focus_sections.items():
            assert isinstance(ids, list)
            ids.sort()

        pipeline_debug(
            "step03", "板块归类",
            f"板块数={len(focus_sections)} 重点总篇数={len(focus_id_set)} sections={ {k: len(v) for k,v in focus_sections.items()} }",
        )
        return focus_sections, focus_id_set

    # ------------------------------------------------------------------
    # step04：生成短文摘要（LLM）
    # ------------------------------------------------------------------
    def step04_summarize(self, base_info: OrderedDict, details_by_aid: dict) -> dict:
        summaries = {}
        aid_list_unique = list(dict.fromkeys(base_info.keys()))
        total04 = len(aid_list_unique)

        def _run_step04_one(aid: str) -> tuple[str, str | None]:
            assert isinstance(aid, str)
            assert aid in details_by_aid
            assert "abstract" in details_by_aid[aid]
            assert isinstance(details_by_aid[aid]["abstract"], str)

            sum_fp = os.path.join(self.step04_summaries_llm, f"{aid}.json")
            out = self.pipeline.call_llm(
                PROMPT_STEP04_SUMMARY.format(
                    title=base_info[aid]["title"],
                    abstract=details_by_aid[aid]["abstract"],
                ),
                sum_fp,
                cache_key=None,
                force_rerun=self._should("step04"),
                debug_step="step04",
                debug_title="生成短文摘要",
            )
            return aid, out

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(_run_step04_one, aid): aid for aid in aid_list_unique}
            pbar = tqdm(total=total04, desc="step04 | 生成短文摘要", unit="篇")
            try:
                done = 0
                for fut in as_completed(futures):
                    aid = futures[fut]
                    try:
                        aid, out = fut.result()
                    except Exception as e:
                        pipeline_debug("step04", "生成短文摘要异常", f"论文 aid={aid} err={type(e).__name__}: {e}")
                        out = None
                    done += 1
                    pipeline_debug("step04", "生成短文摘要进度", f"{done}/{total04} 论文 aid={aid}")
                    pbar.update(1)
                    if out is not None:
                        summaries[aid] = out
            finally:
                pbar.close()

        return summaries

    # ------------------------------------------------------------------
    # step05-08：重点篇 HTML + 深度解析 + 选图 + 图注翻译
    # ------------------------------------------------------------------
    def step05_08_deep(self, focus_ids_unique: list, base_info: OrderedDict) -> tuple[dict, dict]:
        deeps, imgs = {}, {}
        total_focus = len(focus_ids_unique)

        def _run_05_08_one(aid: str) -> tuple[str, str | None, list | None]:
            assert isinstance(aid, str)
            pipeline_debug("step05", "step05-08提交", f"重点编号={aid}")

            h_p, t_p = self.pipeline.download_arxiv_html(
                aid, self.step05_arxiv_html, force_rerun=self._should("step05")
            )
            if not os.path.exists(h_p):
                pipeline_debug("step05", "arxiv实验HTML", f"重点编号={aid} 无HTML缓存文件 路径={h_p} 已跳过深度与图示")
                return aid, None, None

            with open(h_p, "r", encoding="utf-8") as f:
                full_html = f.read()
            with open(t_p, "r", encoding="utf-8") as f:
                clean_txt = f.read()

            deep_fp = os.path.join(self.step06_deep_llm, f"{aid}.json")
            deep_out = self.pipeline.call_llm(
                PROMPT_STEP06_DEEP.format(paper_body_excerpt=clean_txt[: self.cfg.deep_body_max_chars]),
                deep_fp,
                cache_key=None,
                force_rerun=self._should("step06"),
                debug_step="step06",
                debug_title="深度解析",
            )

            raw_meta = self.pipeline.extract_images_from_html(
                full_html, aid, self.pub_img_dir,
                debug_step="step07", debug_title="抽取图示",
            )
            if not raw_meta:
                img_meta = []
            elif len(raw_meta) == 1:
                m0 = raw_meta[0]
                k_sel = self.cfg.key_figure_count
                assert isinstance(k_sel, int) and k_sel >= 1
                selected_meta = [
                    {
                        "path": m0["path"],
                        "caption": m0["caption"],
                        "role": self.pipeline._pipeline_role_for_slot(i),
                    }
                    for i in range(1, k_sel + 1)
                ]
                img_meta = self.pipeline.translate_figure_captions(
                    selected_meta, aid, self.step08_figure_caption_zh,
                    force_rerun=self._should("step08"),
                    debug_step="step08", debug_title="图注翻译",
                )
            else:
                selected_meta = self.pipeline.select_key_figures_by_caption_two_round(
                    raw_meta, aid, self.step07b_key_figure_select,
                    force_rerun=self._should("step07b"),
                    debug_step="step07b", debug_title="关键图选择",
                )
                img_meta = self.pipeline.translate_figure_captions(
                    selected_meta, aid, self.step08_figure_caption_zh,
                    force_rerun=self._should("step08"),
                    debug_step="step08", debug_title="图注翻译",
                )

            return aid, deep_out, img_meta

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(_run_05_08_one, aid): aid for aid in focus_ids_unique}
            pbar = tqdm(total=total_focus, desc="step05-08 | HTML+深度+图示+图注翻译", unit="篇")
            try:
                done = 0
                for fut in as_completed(futures):
                    aid = futures[fut]
                    try:
                        aid, deep_out, img_meta = fut.result()
                    except Exception as e:
                        pipeline_debug("step05-08", "重点篇异常", f"重点编号={aid} err={type(e).__name__}: {e}")
                        deep_out, img_meta = None, None
                    done += 1
                    pipeline_debug("step05-08", "进度", f"{done}/{total_focus} 重点编号={aid}")
                    pbar.update(1)
                    if deep_out is not None:
                        deeps[aid] = deep_out
                    if img_meta is not None:
                        imgs[aid] = img_meta
            finally:
                pbar.close()

        return deeps, imgs

    # ------------------------------------------------------------------
    # step09：落盘与发布
    # ------------------------------------------------------------------
    def step09_publish(
        self,
        base_info: OrderedDict,
        hf_votes: dict,
        focus_ids: list,
        focus_sections: OrderedDict,
        summaries: dict,
        deeps: dict,
        imgs: dict,
        details_by_aid: dict,
    ) -> None:
        if os.path.isdir(self.step03_arxiv_abs):
            pipeline_debug("step09", "发布前汇总", f"step03 arxiv摘要缓存目录存在 {self.step03_arxiv_abs}")
        if os.path.isdir(self.step04_summaries_llm):
            pipeline_debug("step09", "发布前汇总", f"step04 JSON文件数={_count_json_files(self.step04_summaries_llm)} 目录={self.step04_summaries_llm}")
        if os.path.isdir(self.step06_deep_llm):
            pipeline_debug("step09", "发布前汇总", f"step06 JSON文件数={_count_json_files(self.step06_deep_llm)} 目录={self.step06_deep_llm}")
        if os.path.isdir(self.step07b_key_figure_select):
            pipeline_debug("step09", "发布前汇总", f"step07b 关键图选择 JSON数={_count_json_files(self.step07b_key_figure_select)} 目录={self.step07b_key_figure_select}")
        if os.path.isdir(self.step08_figure_caption_zh):
            pipeline_debug("step09", "发布前汇总", f"step08 图注翻译缓存 JSON数={_count_json_files(self.step08_figure_caption_zh)} 目录={self.step08_figure_caption_zh}")

        report_data = {
            "date": self.date_str,
            "focus_ids": focus_ids,
            "focus_sections": focus_sections,
            "base_info": base_info,
            "summaries": _json_dict_sorted_by_key(summaries),
            "deep_analysis": _json_dict_sorted_by_key(deeps),
            "images_meta": _json_dict_sorted_by_key(imgs),
            "arxiv_details": _json_dict_sorted_by_key(details_by_aid),
        }

        hf_votes_out = {k: hf_votes[k] for k in sorted(hf_votes.keys())}

        with open(f"{self.pub_dir}/config.json", 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        with open(f"{self.pub_dir}/hf_votes.json", 'w', encoding='utf-8') as f:
            json.dump(hf_votes_out, f, indent=2, ensure_ascii=False)
        pipeline_debug(
            "step09", "导出站点",
            f"已写入 config.json + hf_votes.json 深度解析篇数={len(deeps)} 图示元数据篇数={len(imgs)}",
        )

        if os.path.exists(self.cfg.frontend_template_path):
            shutil.copy(self.cfg.frontend_template_path, f"{self.pub_dir}/index.html")
            pipeline_debug("step09", "导出站点", f"已复制 {self.cfg.frontend_template_path}")
        else:
            pipeline_debug("step09", "导出站点", f"未找到 {self.cfg.frontend_template_path}，已跳过复制")

        self.pipeline._update_date_index_config()

        # Docsify 渲染
        from renderers.docsify.sync import DocsifyRenderer
        from renderers.docsify.index_gen import update_global_sidebar, ensure_docsify_entry

        docsify = DocsifyRenderer()
        docsify.render_date(self.pub_dir, report_data, hf_votes_out)
        docs_date_dir = os.path.dirname(self.pub_dir)
        update_global_sidebar(docs_date_dir)
        ensure_docsify_entry(docs_date_dir)
        pipeline_debug("step09", "docsify", f"已生成 docsify .md 文件 目录={self.pub_dir}")

        print(f"\n完成！数据目录: {self.pub_dir}")

    # ------------------------------------------------------------------
    # run：串联所有步骤
    # ------------------------------------------------------------------
    def _rebuild_paths(self):
        """日期变化后重新计算所有路径。"""
        self.pub_dir = self.cfg.output_pub_dir_fmt.format(date_str=self.date_str)
        self.pub_img_dir = f"{self.pub_dir}/{self.cfg.pub_images_subdir}"
        self.cache_root = self.cfg.output_cache_dir_fmt.format(date_str=self.date_str)
        self.step01_hf = f"{self.cache_root}/step01_hf_papers.json"
        self.step03_arxiv_abs = f"{self.cache_root}/step03_arxiv_abs"
        self.step04_summaries_llm = f"{self.cache_root}/step04_summaries_llm"
        self.step05_arxiv_html = f"{self.cache_root}/step05_arxiv_html"
        self.step06_deep_llm = f"{self.cache_root}/step06_deep_llm"
        self.step07b_key_figure_select = f"{self.cache_root}/step07b_key_figure_select"
        self.step08_figure_caption_zh = f"{self.cache_root}/step08_figure_caption_zh"

    def run(self, skip_void_date: bool = False) -> None:
        # step01 缓存已存在时跳过日期解析（避免无谓的网络请求）
        if os.path.exists(self.step01_hf):
            pipeline_debug("step01", "日期解析", f"step01缓存已存在，跳过HF日期解析 日期={self.date_str}")
            new_date_str = self.date_str
        else:
            new_date_str = self.pipeline._resolve_hf_date(self.date_str)
        if new_date_str != self.date_str:
            pipeline_debug("step01", "日期解析", f"HF 从 {self.date_str} 跳转到 {new_date_str}")
            if skip_void_date:
                pipeline_debug("step01", "日期解析", f"跳过日期解析 日期={self.date_str}")
                return
        self.date_str = new_date_str
        self._rebuild_paths()

        log_dir = f"{self.cache_root}/logs"
        run_ts = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d_%H%M%S")
        _set_pipeline_log_path(f"{log_dir}/pipeline_{run_ts}.log")

        base_info, hf_votes = self.step01_fetch_hf()
        if not base_info:
            return

        details_by_aid = self.step02_fetch_arxiv_abs(base_info)
        focus_sections, _ = self.step03_classify(base_info, details_by_aid)
        summaries = self.step04_summarize(base_info, details_by_aid)

        focus_ids = []
        for _sec_name, ids in focus_sections.items():
            for aid in ids:
                focus_ids.append(aid)
        focus_ids_unique = list(dict.fromkeys(focus_ids))

        deeps, imgs = self.step05_08_deep(focus_ids_unique, base_info)
        self.step09_publish(base_info, hf_votes, focus_ids, focus_sections, summaries, deeps, imgs, details_by_aid)

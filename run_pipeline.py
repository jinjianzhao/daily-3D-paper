import os
import re
import json
import time
import shutil
import requests
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from collections import OrderedDict
from bs4 import BeautifulSoup
from tqdm import tqdm
import urllib3.exceptions



def pipeline_debug(step: str, title: str, msg: str = ""):
    assert isinstance(step, str)
    assert isinstance(title, str)
    assert isinstance(msg, str)
    suffix = f" {msg}" if msg else ""
    # flush=True：与 tqdm 同屏输出时避免 stdout 缓冲导致「看不到」某步日志
    print(f"[{step}][{title}]{suffix}", flush=True)


def _extract_vote_count(article_tag) -> int:
    """从 article 标签中提取投票数。

    直接在第三个子元素中搜索 div.leading-none 获取投票数。
    """
    assert hasattr(article_tag, 'children'), "article_tag 必须是 BeautifulSoup Tag 对象"

    non_empty = [child for child in article_tag.children if child.name is not None]
    if len(non_empty) < 3:
        return 0
    third = non_empty[2]
    vote_div = third.select_one("div.leading-none")
    if vote_div:
        text = vote_div.get_text(strip=True)
        if text.isdigit():
            return int(text)
    return 0


def _count_json_files(cache_dir: str) -> int:
    assert isinstance(cache_dir, str)
    assert os.path.isdir(cache_dir)
    return sum(1 for name in os.listdir(cache_dir) if name.endswith(".json"))


@dataclass
class PipelineConfig:
    """流水线可调参数：实例化后传入 PaperPipeline(..., cfg)。"""
    output_pub_dir_fmt: str = "docs/date/{date_str}"
    output_cache_dir_fmt: str = "output/cache/date/{date_str}"
    pub_images_subdir: str = "images"
    frontend_template_path: str = "templates/index.html"
    llm_model: str = "deepseek-ai/DeepSeek-V3.2"
    llm_api_url: str = "https://api.siliconflow.cn/v1/chat/completions"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2048
    llm_request_timeout_sec: int = 60
    # hf_mirror_base_url: str = "https://hf-mirror.com"
    hf_paper_link_prefix: str = "https://huggingface.co"
    hf_href_arxiv_id_regex: str = r"(\d{4}\.\d+)"
    http_user_agent: str = "Mozilla/5.0"
    timeout_hf_list_sec: int = 30
    timeout_arxiv_abs_sec: int = 20
    timeout_arxiv_html_sec: int = 60
    timeout_arxiv_image_sec: int = 20
    arxiv_abs_base_url: str = "https://arxiv.org/abs/"
    arxiv_html_base_url: str = "https://arxiv.org/html/"
    arxiv_html_image_base_url: str = "https://arxiv.org/html/"
    # False：图示 path 使用 arXiv 绝对 URL，不写本地 images/（默认）；True：下载到发布目录 images/
    store_arxiv_figures_locally: bool = False
    deep_body_max_chars: int = 8000
    max_figures_per_paper: int = 3
    arxiv_id_regex: str = r"\d{4}\.\d+"
    # step02：单篇论文投票判断次数（默认3次投票决定是否3D相关）
    focus_vote_times: int = 3
    # step08：图注译中文单次请求上限（图注可能很长）
    figure_caption_translate_max_tokens: int = 8192


# ================= 主流程 PaperPipeline =================
class PaperPipeline:
    def __init__(self, api_key, cfg):
        assert isinstance(api_key, str)
        assert isinstance(cfg, PipelineConfig)
        self.api_key = api_key
        self.cfg = cfg
        self.headers = {"User-Agent": cfg.http_user_agent}

    def _post_chat_completion(self, user_content: str, max_tokens: int | None = None) -> str:
        assert isinstance(user_content, str)
        assert max_tokens is None or (isinstance(max_tokens, int) and max_tokens > 0)
        mt = self.cfg.llm_max_tokens if max_tokens is None else max_tokens
        payload = {
            "model": self.cfg.llm_model,
            "messages": [{"role": "user", "content": user_content}],
            "temperature": self.cfg.llm_temperature,
            "max_tokens": mt,
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        retry_delays = [5, 10, 30, 60, 60*2, 60*5, 60*10, 60*30, 60*60]
        last_exception = None

        for attempt, delay in enumerate([0] + retry_delays):
            if delay > 0:
                time.sleep(delay)
                pipeline_debug(
                    "retry",
                    "LLM请求超时",
                    f"第{attempt}次超时，等待{delay}秒后重试...",
                )
            try:
                r = requests.post(
                    self.cfg.llm_api_url,
                    json=payload,
                    headers=headers,
                    timeout=self.cfg.llm_request_timeout_sec,
                )
                try:
                    body = r.json()
                except json.JSONDecodeError as e:
                    raise RuntimeError(
                        f"LLM HTTP {r.status_code} 响应非 JSON 前200字符={r.text[:200]!r}"
                    ) from e
                if r.status_code >= 400:
                    err = body["error"] if isinstance(body, dict) and "error" in body else body
                    raise RuntimeError(f"LLM HTTP {r.status_code} {err}")
                if not isinstance(body, dict) or "choices" not in body or not body["choices"]:
                    raise RuntimeError(f"LLM 响应缺少 choices 前200字符={str(body)[:200]!r}")
                return body["choices"][0]["message"]["content"]
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, urllib3.exceptions.ReadTimeoutError) as e:
                last_exception = e

        raise RuntimeError(
            f"LLM 请求在 {len(retry_delays)} 次重试后仍然超时"
        ) from last_exception

    def _call_multistep_llm_no_cache(
        self,
        prompt_first: str,
        prompt_second_fmt: str,
        *,
        debug_step: str,
        debug_title: str,
    ) -> str:
        assert isinstance(prompt_first, str)
        assert isinstance(prompt_second_fmt, str)
        assert isinstance(debug_step, str)
        assert isinstance(debug_title, str)
        assert "{step1_output}" in prompt_second_fmt
        out1 = self._post_chat_completion(prompt_first)
        pipeline_debug(debug_step, debug_title, f"多步LLM 第1轮 输出字符数={len(out1)}")
        prompt_second = prompt_second_fmt.replace("{step1_output}", out1)
        out2 = self._post_chat_completion(prompt_second)
        pipeline_debug(debug_step, debug_title, f"多步LLM 第2轮 输出字符数={len(out2)}")
        return out2

    def call_llm(
        self,
        prompt,
        cache_path,
        cache_key=None,
        force_rerun=False,
        *,
        debug_step: str,
        debug_title: str,
    ):
        assert isinstance(cache_path, str)
        assert cache_key is None or isinstance(cache_key, str)
        assert isinstance(force_rerun, bool)
        assert isinstance(debug_step, str)
        assert isinstance(debug_title, str)

        # cache_key 为 None 时：cache_path 指向单文件 JSON，结构为 {"output": "..."}
        if cache_key is None:
            if not force_rerun and os.path.exists(cache_path):
                with open(cache_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                assert isinstance(data, dict)
                assert "output" in data
                pipeline_debug(debug_step, debug_title, f"命中缓存 文件={cache_path}")
                return data["output"]
        else:
            store = {}
            if os.path.exists(cache_path):
                with open(cache_path, 'r', encoding='utf-8') as f:
                    store = json.load(f)
                assert isinstance(store, dict)
            if not force_rerun and cache_key in store:
                pipeline_debug(debug_step, debug_title, f"命中缓存 键={cache_key} 文件={cache_path}")
                return store[cache_key]

        res = self._post_chat_completion(prompt)

        parent = os.path.dirname(cache_path)
        if parent:
            os.makedirs(parent, exist_ok=True)

        if cache_key is None:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump({"output": res}, f, indent=2, ensure_ascii=False)
        else:
            store = {}
            if os.path.exists(cache_path):
                with open(cache_path, 'r', encoding='utf-8') as f:
                    store = json.load(f)
                assert isinstance(store, dict)
            store[cache_key] = res
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(store, f, indent=2, ensure_ascii=False)

        pipeline_debug(debug_step, debug_title, f"模型已返回 键={cache_key} 输出字符数={len(res)}")
        return res

    def call_multistep_llm(
        self,
        prompt_first: str,
        prompt_second_fmt: str,
        cache_path: str,
        force_rerun: bool = False,
        *,
        debug_step: str,
        debug_title: str,
    ):
        assert isinstance(prompt_first, str)
        assert isinstance(prompt_second_fmt, str)
        assert isinstance(cache_path, str)
        assert isinstance(force_rerun, bool)
        assert isinstance(debug_step, str)
        assert isinstance(debug_title, str)
        assert "{step1_output}" in prompt_second_fmt

        if not force_rerun and os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert isinstance(data, dict)
            assert "output" in data
            pipeline_debug(debug_step, debug_title, f"多步LLM 命中缓存 文件={cache_path}")
            return data["output"]

        res = self._call_multistep_llm_no_cache(
            prompt_first,
            prompt_second_fmt,
            debug_step=debug_step,
            debug_title=debug_title,
        )
        parent = os.path.dirname(cache_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump({"output": res}, f, indent=2, ensure_ascii=False)
        pipeline_debug(debug_step, debug_title, f"多步LLM 已写入 输出字符数={len(res)}")
        return res

    def call_llm_multitimes_and_merge(
        self,
        prompt_first: str,
        prompt_second_fmt: str,
        cache_path: str,
        n_runs: int,
        force_rerun: bool = False,
        *,
        debug_step: str,
        debug_title: str,
    ):
        assert isinstance(prompt_first, str)
        assert isinstance(prompt_second_fmt, str)
        assert isinstance(cache_path, str)
        assert isinstance(n_runs, int) and n_runs >= 1
        assert isinstance(force_rerun, bool)
        assert isinstance(debug_step, str)
        assert isinstance(debug_title, str)
        assert "{step1_output}" in prompt_second_fmt

        if not force_rerun and os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert isinstance(data, dict)
            assert "output" in data
            pipeline_debug(debug_step, debug_title, f"多轮合并 命中缓存 文件={cache_path}")
            return data["output"]

        merged_ids = set()
        for k in range(n_runs):
            text = self._call_multistep_llm_no_cache(
                prompt_first,
                prompt_second_fmt,
                debug_step=debug_step,
                debug_title=debug_title,
            )
            found = re.findall(self.cfg.arxiv_id_regex, text)
            merged_ids.update(found)
            pipeline_debug(
                debug_step,
                debug_title,
                f"多轮合并 完成第{k + 1}/{n_runs}次 本轮解析到编号数={len(found)} 累计去重={len(merged_ids)}",
            )

        res = "\n".join(sorted(merged_ids))
        parent = os.path.dirname(cache_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump({"output": res}, f, indent=2, ensure_ascii=False)
        pipeline_debug(debug_step, debug_title, f"多轮合并 已写入 去重后编号数={len(merged_ids)}")
        return res

    def _resolve_hf_date(self, date_str: str) -> str:
        """访问 HF 论文页，若发生跳转则提取实际日期（如周末/未更新时 HF 会跳转到前一日）。"""
        assert isinstance(date_str, str)
        url = f"{self.cfg.hf_paper_link_prefix}/papers/"
        resp = requests.get(url, headers=self.headers, timeout=self.cfg.timeout_hf_list_sec, allow_redirects=True)
        redirect_match = re.search(r"/papers/date/(\d{4}-\d{2}-\d{2})", resp.url)
        if redirect_match:
            actual = redirect_match.group(1)
            if actual != date_str:
                pipeline_debug("step01", "日期解析", f"HF 从 {date_str} 跳转到 {actual}")
                return actual
        return date_str

    def fetch_hf_papers(self, date_str, cache_path, force_rerun=False):
        assert isinstance(date_str, str)
        assert isinstance(cache_path, str)
        assert isinstance(force_rerun, bool)

        if not force_rerun and os.path.exists(cache_path):
            with open(cache_path, 'r', encoding='utf-8') as f:
                results = json.load(f)
            assert isinstance(results, dict)
            pipeline_debug("step01", "拉取论文列表", f"命中缓存 篇数={len(results)} 文件={cache_path}")
            return results

        url = f"{self.cfg.hf_mirror_base_url}/papers/date/{date_str}"
        resp = requests.get(url, headers=self.headers, timeout=self.cfg.timeout_hf_list_sec)
        soup = BeautifulSoup(resp.text, "html.parser")
        results_with_votes = []
        for a in soup.find_all("article"):
            title_tag = a.select_one("h3 a")
            if title_tag:
                id_match = re.search(self.cfg.hf_href_arxiv_id_regex, title_tag["href"])
                if id_match:
                    aid = id_match.group(1)
                    # 提取点赞数：article 的第三个子元素
                    vote_count = _extract_vote_count(a)
                    if vote_count == 0:
                        pass
                    results_with_votes.append({
                        "aid": aid,
                        "title": title_tag.get_text(strip=True),
                        "hf_link": f"{self.cfg.hf_paper_link_prefix}{title_tag['href']}",
                        "votes": vote_count,
                    })
        
        # 按点赞数降序排序，转换为 OrderedDict
        results_with_votes.sort(key=lambda x: x["votes"], reverse=True)
        results = OrderedDict()
        for item in results_with_votes:
            aid = item["aid"]
            results[aid] = {
                "title": item["title"],
                "hf_link": item["hf_link"],
                "votes": item["votes"],
            }
        
        pipeline_debug("step01", "拉取论文列表", f"HTTP状态={resp.status_code} 解析篇数={len(results)} 点赞最高={results_with_votes[0]['votes'] if results_with_votes else 0}")
        parent = os.path.dirname(cache_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        return results

    def get_arxiv_details(self, arxiv_id, cache_path, force_rerun=False):
        assert isinstance(arxiv_id, str)
        assert isinstance(cache_path, str)
        assert isinstance(force_rerun, bool)

        os.makedirs(cache_path, exist_ok=True)
        fp = os.path.join(cache_path, f"{arxiv_id}.json")
        if not force_rerun and os.path.exists(fp):
            with open(fp, 'r', encoding='utf-8') as f:
                data = json.load(f)
            assert isinstance(data, dict)
            assert "abstract" in data
            if "comments" not in data:
                data["comments"] = ""
            pipeline_debug("step03", "arxiv摘要页", f"命中缓存 编号={arxiv_id}")
            return data

        resp = requests.get(
            f"{self.cfg.arxiv_abs_base_url}{arxiv_id}",
            headers=self.headers,
            timeout=self.cfg.timeout_arxiv_abs_sec,
        )
        soup = BeautifulSoup(resp.text, "html.parser")
        abs_tag = soup.find('blockquote', class_='abstract')
        abstract = abs_tag.get_text(strip=True).replace('Abstract:', '').strip() if abs_tag else "无摘要"
        comments_td = soup.find(
            "td",
            class_=lambda c: c is not None and "comments" in c,
        )
        comments = comments_td.decode_contents().strip() if comments_td else ""
        out = {"abstract": abstract, "comments": comments}
        with open(fp, 'w', encoding='utf-8') as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        return out

    def download_arxiv_html(self, aid, cache_path, force_rerun=False):
        assert isinstance(aid, str)
        assert isinstance(cache_path, str)
        assert isinstance(force_rerun, bool)

        os.makedirs(cache_path, exist_ok=True)
        raw_h = os.path.join(cache_path, f"{aid}.html")
        txt_h = os.path.join(cache_path, f"{aid}.txt")
        if force_rerun:
            for p in (raw_h, txt_h):
                if os.path.exists(p):
                    os.remove(p)
        if not os.path.exists(raw_h):
            r = requests.get(
                f"{self.cfg.arxiv_html_base_url}{aid}",
                headers=self.headers,
                timeout=self.cfg.timeout_arxiv_html_sec,
            )
            pipeline_debug(
                "step05",
                "arxiv实验HTML",
                f"编号={aid} HTTP状态={r.status_code} 正文长度={len(r.text)}",
            )
            if r.status_code == 200:
                with open(raw_h, 'w', encoding='utf-8') as f:
                    f.write(r.text)
                soup = BeautifulSoup(r.text, 'html.parser')
                with open(txt_h, 'w', encoding='utf-8') as f:
                    f.write(soup.get_text(separator=' ', strip=True))
        else:
            pipeline_debug("step05", "arxiv实验HTML", f"编号={aid} 命中缓存 路径={raw_h}")
        return raw_h, txt_h

    def extract_images_from_html(
        self,
        html_content,
        aid,
        cache_path,
        *,
        debug_step: str,
        debug_title: str,
    ):
        """返回前端可用的图示地址：本地模式为 images/ 相对路径，远程模式为 https 绝对 URL。cache_path 为本地落盘目录。"""
        assert isinstance(html_content, str)
        assert isinstance(aid, str)
        assert isinstance(cache_path, str)
        assert isinstance(debug_step, str)
        assert isinstance(debug_title, str)

        if self.cfg.store_arxiv_figures_locally:
            os.makedirs(cache_path, exist_ok=True)
        soup = BeautifulSoup(html_content, 'html.parser')
        figures = soup.find_all('figure', class_='ltx_figure')
        pipeline_debug(
            debug_step,
            debug_title,
            f"编号={aid} LaTeX图注块数={len(figures)} 页内图片标签数={len(soup.find_all('img'))} HTML字符数={len(html_content)}",
        )
        meta = []
        count = 0
        for fig in figures:
            if count >= self.cfg.max_figures_per_paper:
                break
            img_tag = fig.find('img')
            if img_tag and img_tag.get('src'):
                img_src = img_tag['src']
                img_url = self.cfg.arxiv_html_image_base_url + img_src.lstrip('/')
                if self.cfg.store_arxiv_figures_locally:
                    ext = img_src.split('.')[-1]
                    fname = f"{aid}_fig_{count}.{ext}"
                    local_path = os.path.join(cache_path, fname)
                    if not os.path.exists(local_path):
                        ir = requests.get(
                            img_url, headers=self.headers, timeout=self.cfg.timeout_arxiv_image_sec
                        )
                        if ir.status_code == 200:
                            with open(local_path, 'wb') as f:
                                f.write(ir.content)
                        else:
                            pipeline_debug(
                                debug_step,
                                debug_title,
                                f"图片下载失败 编号={aid} HTTP状态={ir.status_code} 地址前100字符={img_url[:100]}",
                            )
                    out_path = f"images/{fname}"
                else:
                    out_path = img_url
                meta.append({"path": out_path, "caption": fig.get_text(strip=True)})
                count += 1
        pipeline_debug(debug_step, debug_title, f"编号={aid} 图示条目数={len(meta)}")
        return meta

    def _parse_json_array_from_llm(self, raw: str):
        assert isinstance(raw, str)
        s = raw.strip()
        fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", s)
        if fence:
            s = fence.group(1).strip()
        arr = json.loads(s)
        assert isinstance(arr, list)
        return arr

    def judge_paper_relevance(self, title, abstract, arxiv_id, cache_dir, force_rerun=False, *, debug_step, debug_title):
        """
        单篇论文相关性判断：多次调用LLM投票决定是否3D相关。
        
        Args:
            title: 论文标题
            abstract: 论文摘要
            arxiv_id: arXiv 论文编号
            cache_dir: 缓存目录路径
            force_rerun: 是否强制重跑
            debug_step: 调试步骤标识
            debug_title: 调试标题
            
        Returns:
            bool: True表示3D相关，False表示不相关
        """
        assert isinstance(title, str)
        assert isinstance(abstract, str)
        assert isinstance(arxiv_id, str)
        assert isinstance(cache_dir, str)
        assert isinstance(force_rerun, bool)
        assert isinstance(debug_step, str)
        assert isinstance(debug_title, str)
        
        # 构建缓存文件路径
        cache_file = os.path.join(cache_dir, f"{arxiv_id}_vote.json")
        
        if not force_rerun and os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached = json.load(f)
            assert isinstance(cached, dict)
            if "vote_result" in cached and "vote_details" in cached:
                pipeline_debug(debug_step, debug_title, f"命中投票缓存 编号={arxiv_id} 结果={cached['vote_result']}")
                return cached["vote_result"] == "true"
        
        # 执行多次投票
        votes = []
        for i in range(self.cfg.focus_vote_times):
            prompt = PROMPT_STEP02_JUDGE_SINGLE.format(title=title, abstract=abstract)
            response = self._post_chat_completion(prompt)
            response_clean = response.strip().lower()
            
            # 解析响应
            if "是" in response_clean:
                vote = True
            elif "否" in response_clean:
                vote = False
            else:
                # 无法解析时默认为否
                vote = False
            
            votes.append(vote)
            pipeline_debug(
                debug_step, 
                debug_title, 
                f"投票 {i+1}/{self.cfg.focus_vote_times} 编号={arxiv_id} 响应={response_clean} 判定={vote}"
            )
        
        # 投票统计：多数决定
        true_count = sum(votes)
        final_result = true_count > len(votes) / 2
        
        pipeline_debug(
            debug_step,
            debug_title,
            f"投票完成 编号={arxiv_id} 支持={true_count}/{len(votes)} 最终结果={'3D相关' if final_result else '不相关'}"
        )
        
        # 写入缓存
        os.makedirs(cache_dir, exist_ok=True)
        cache_data = {
            "arxiv_id": arxiv_id,
            "title": title,
            "vote_result": "true" if final_result else "false",
            "vote_details": votes,
            "support_count": true_count,
            "total_votes": len(votes)
        }
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
        
        return final_result

    def translate_figure_captions(
        self,
        meta_list,
        aid,
        cache_dir,
        force_rerun=False,
        *,
        debug_step: str,
        debug_title: str,
    ):
        """在抽取图示之后：将英文图注批量译为中文，写入 caption_zh；结果缓存按篇落盘。"""
        assert isinstance(meta_list, list)
        assert isinstance(aid, str)
        assert isinstance(cache_dir, str)
        assert isinstance(force_rerun, bool)
        assert isinstance(debug_step, str)
        assert isinstance(debug_title, str)
        for m in meta_list:
            assert isinstance(m, dict)
            assert "path" in m and "caption" in m
            assert isinstance(m["path"], str) and isinstance(m["caption"], str)

        if not meta_list:
            pipeline_debug(debug_step, debug_title, f"图注翻译 跳过 编号={aid} 无图示条目")
            return []

        os.makedirs(cache_dir, exist_ok=True)
        fp = os.path.join(cache_dir, f"{aid}.json")
        paths = [m["path"] for m in meta_list]
        source_captions = [m["caption"] for m in meta_list]

        if not force_rerun and os.path.exists(fp):
            with open(fp, "r", encoding="utf-8") as f:
                cached = json.load(f)
            assert isinstance(cached, dict)
            if (
                "paths" in cached
                and "source_captions" in cached
                and "figures" in cached
                and cached["paths"] == paths
                and cached["source_captions"] == source_captions
                and len(cached["figures"]) == len(meta_list)
            ):
                pipeline_debug(debug_step, debug_title, f"图注翻译 命中缓存 编号={aid} 条数={len(meta_list)}")
                return [
                    {
                        "path": m["path"],
                        "caption": m["caption"],
                        "caption_zh": cached["figures"][i]["caption_zh"],
                    }
                    for i, m in enumerate(meta_list)
                ]
            pipeline_debug(
                debug_step,
                debug_title,
                f"图注翻译 缓存未命中或已变更 编号={aid} 将重新请求 LLM 文件={fp}",
            )
        elif force_rerun and os.path.exists(fp):
            pipeline_debug(
                debug_step,
                debug_title,
                f"图注翻译 强制重跑 编号={aid} 忽略已有缓存",
            )

        n = len(meta_list)
        pipeline_debug(
            debug_step,
            debug_title,
            f"图注翻译 请求LLM 编号={aid} 条数={n}",
        )
        numbered = "\n".join(f"[{i}] {m['caption']}" for i, m in enumerate(meta_list))
        prompt = PROMPT_STEP08_CAPTION_ZH.format(n=n, numbered_captions=numbered)
        raw = self._post_chat_completion(
            prompt,
            max_tokens=self.cfg.figure_caption_translate_max_tokens,
        )
        pipeline_debug(
            debug_step,
            debug_title,
            f"图注翻译 LLM已返回 编号={aid} 原始字符数={len(raw)}",
        )

        zh_list = None
        try:
            zh_list = self._parse_json_array_from_llm(raw)
        except (json.JSONDecodeError, AssertionError, TypeError, ValueError) as e:
            pipeline_debug(debug_step, debug_title, f"图注翻译 JSON 解析失败 编号={aid} err={e}")

        if zh_list is None or len(zh_list) != n:
            pipeline_debug(
                debug_step,
                debug_title,
                f"图注翻译 条数不符或解析失败 编号={aid} 期望={n} 回退为原文",
            )
            zh_list = list(source_captions)

        figures_store = []
        out_meta = []
        for i, m in enumerate(meta_list):
            cz = zh_list[i]
            if not isinstance(cz, str):
                cz = str(cz)
            figures_store.append({"path": m["path"], "caption_zh": cz})
            out_meta.append({"path": m["path"], "caption": m["caption"], "caption_zh": cz})

        payload = {
            "arxiv_id": aid,
            "paths": paths,
            "source_captions": source_captions,
            "figures": figures_store,
        }
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        pipeline_debug(debug_step, debug_title, f"图注翻译 已落盘缓存 文件={fp} 条数={n}")
        return out_meta

    def run_pipeline(self, date_str, force_rerun=None):
        assert isinstance(date_str, str)
        assert force_rerun is None or isinstance(force_rerun, list)
        if force_rerun is None:
            force_rerun = []
        for step in force_rerun:
            assert isinstance(step, str)

        def _should(step_name: str) -> bool:
            return step_name in force_rerun

        # 先解析 HF 实际可用日期（若 HF 跳转到前一日，跟随）
        date_str = self._resolve_hf_date(date_str)

        pub_dir = self.cfg.output_pub_dir_fmt.format(date_str=date_str)
        pub_img_dir = f"{pub_dir}/{self.cfg.pub_images_subdir}"
        cache_root = self.cfg.output_cache_dir_fmt.format(date_str=date_str)
        # 分步缓存目录与文件名（step 前缀），顺序与流水线一致
        step01_hf = f"{cache_root}/step01_hf_papers.json"
        step03_arxiv_abs = f"{cache_root}/step03_arxiv_abs"
        step04_summaries_llm = f"{cache_root}/step04_summaries_llm"
        step05_arxiv_html = f"{cache_root}/step05_arxiv_html"
        step06_deep_llm = f"{cache_root}/step06_deep_llm"
        step08_figure_caption_zh = f"{cache_root}/step08_figure_caption_zh"

        # step01：拉取 HF 当日列表（无 tqdm，单次请求）
        base_info = self.fetch_hf_papers(date_str, step01_hf, force_rerun=_should("step01"))
        if not base_info:
            pipeline_debug("step01", "拉取论文列表", "当日无论文，停止")
            return print("当日无论文。")

        os.makedirs(pub_dir, exist_ok=True)

        # step02：抓取 arXiv 摘要页（需要在投票筛选之前）
        details_by_aid = {}
        for aid in tqdm(
            base_info.keys(),
            desc="step02 | arxiv摘要页",
            unit="篇",
        ):
            details_by_aid[aid] = self.get_arxiv_details(aid, step03_arxiv_abs, force_rerun=_should("step02"))

        # step03：单篇论文投票判断 3D 相关重点
        focus_ids = []
        for aid in tqdm(
            base_info.keys(),
            desc="step03 | 单篇投票筛选重点",
            unit="篇",
        ):
            # 使用 judge_paper_relevance 函数进行投票判断
            vote_cache_dir = f"{cache_root}/step03_votes"
            is_related = self.judge_paper_relevance(
                base_info[aid]["title"],
                details_by_aid[aid]["abstract"],
                aid,  # arxiv_id
                vote_cache_dir,
                force_rerun=_should("step03"),
                debug_step="step03",
                debug_title="投票筛选重点",
            )
            if is_related:
                focus_ids.append(aid)
        pipeline_debug("step03", "投票筛选重点", f"重点篇数={len(focus_ids)} 编号列表={focus_ids}")

        # step04：逐篇生成短文摘要（LLM）
        summaries = {}
        for aid in tqdm(
            base_info.keys(),
            desc="step04 | 生成短文摘要",
            unit="篇",
        ):
            sum_fp = os.path.join(step04_summaries_llm, f"{aid}.json")
            summaries[aid] = self.call_llm(
                PROMPT_STEP04_SUMMARY.format(abstract=details_by_aid[aid]["abstract"]),
                sum_fp,
                cache_key=None,
                force_rerun=_should("step04"),
                debug_step="step04",
                debug_title="生成短文摘要",
            )

        # step05～08：重点篇下载 HTML、深度解析、抽图、图注翻译
        deeps, imgs = {}, {}
        for aid in tqdm(
            focus_ids,
            desc="step05-08 | HTML+深度+图示+图注翻译",
            unit="篇",
        ):
            h_p, t_p = self.download_arxiv_html(aid, step05_arxiv_html, force_rerun=_should("step05"))
            if os.path.exists(h_p):
                with open(h_p, 'r', encoding='utf-8') as f:
                    full_html = f.read()
                with open(t_p, 'r', encoding='utf-8') as f:
                    clean_txt = f.read()
                deep_fp = os.path.join(step06_deep_llm, f"{aid}.json")
                deeps[aid] = self.call_llm(
                    PROMPT_STEP06_DEEP.format(
                        paper_body_excerpt=clean_txt[: self.cfg.deep_body_max_chars],
                    ),
                    deep_fp,
                    cache_key=None,
                    force_rerun=_should("step06"),
                    debug_step="step06",
                    debug_title="深度解析",
                )
                raw_meta = self.extract_images_from_html(
                    full_html,
                    aid,
                    pub_img_dir,
                    debug_step="step07",
                    debug_title="抽取图示",
                )
                imgs[aid] = self.translate_figure_captions(
                    raw_meta,
                    aid,
                    step08_figure_caption_zh,
                    force_rerun=_should("step08"),
                    debug_step="step08",
                    debug_title="图注翻译",
                )
            else:
                pipeline_debug(
                    "step05",
                    "arxiv实验HTML",
                    f"重点编号={aid} 无HTML缓存文件 路径={h_p} 已跳过深度与图示",
                )

        # step09：落盘与发布（各步 LLM 结果已在 call_llm 内写入缓存文件）
        if os.path.isdir(step03_arxiv_abs):
            pipeline_debug("step09", "发布前汇总", f"step03 arxiv摘要缓存目录存在 {step03_arxiv_abs}")
        if os.path.isdir(step04_summaries_llm):
            pipeline_debug(
                "step09",
                "发布前汇总",
                f"step04 JSON文件数={_count_json_files(step04_summaries_llm)} 目录={step04_summaries_llm}",
            )
        if os.path.isdir(step06_deep_llm):
            pipeline_debug(
                "step09",
                "发布前汇总",
                f"step06 JSON文件数={_count_json_files(step06_deep_llm)} 目录={step06_deep_llm}",
            )
        if os.path.isdir(step08_figure_caption_zh):
            pipeline_debug(
                "step09",
                "发布前汇总",
                f"step08 图注翻译缓存 JSON数={_count_json_files(step08_figure_caption_zh)} 目录={step08_figure_caption_zh}",
            )

        report_data = {
            "date": date_str,
            "focus_ids": focus_ids,
            "base_info": base_info,
            "summaries": summaries,
            "deep_analysis": deeps,
            "images_meta": imgs,
            "arxiv_details": details_by_aid,
        }
        
        # 写入 config.json，供前端 index.html 读取
        with open(f"{pub_dir}/config.json", 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        pipeline_debug(
            "step09",
            "导出站点",
            f"已写入 config.json 深度解析篇数={len(deeps)} 图示元数据篇数={len(imgs)}",
        )

        # 复制前端页面模板
        if os.path.exists(self.cfg.frontend_template_path):
            shutil.copy(self.cfg.frontend_template_path, f"{pub_dir}/index.html")
            pipeline_debug("step09", "导出站点", f"已复制 {self.cfg.frontend_template_path}")
        else:
            pipeline_debug(
                "step09",
                "导出站点",
                f"未找到 {self.cfg.frontend_template_path}，已跳过复制",
            )

        # 更新日期索引：output/papers/date/config.json
        self._update_date_index_config()

        print(f"\n✅ 完成！数据目录: {pub_dir}")

    def _update_date_index_config(self):
        """扫描 docs/date/ 下所有日期目录，生成索引 config.json。"""
        date_dir_root = "docs/date"
        if not os.path.isdir(date_dir_root):
            return

        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        dates = []
        paper_counts = {}

        for name in sorted(os.listdir(date_dir_root)):
            dir_path = os.path.join(date_dir_root, name)
            if not os.path.isdir(dir_path) or not date_pattern.match(name):
                continue
            dates.append(name)
            # 尝试读取该日期目录的 config.json 获取论文篇数
            date_config_path = os.path.join(dir_path, "config.json")
            if os.path.exists(date_config_path):
                try:
                    with open(date_config_path, 'r', encoding='utf-8') as f:
                        dc = json.load(f)
                    if isinstance(dc, dict) and "base_info" in dc and isinstance(dc["base_info"], dict):
                        paper_counts[name] = len(dc["base_info"])
                except (json.JSONDecodeError, KeyError, TypeError):
                    pass

        index_config = {
            "dates": sorted(dates, reverse=True),
            "paper_counts": paper_counts,
        }
        out_path = os.path.join(date_dir_root, "config.json")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(index_config, f, indent=2, ensure_ascii=False)
        pipeline_debug(
            "step09",
            "更新日期索引",
            f"已写入 {out_path} 日期数={len(dates)}",
        )


# ---------------------------------------------------------------------------
# LLM 提示词
# - 仅 step02「筛重点、输出规整编号列表」用 call_llm_multitimes_and_merge + 两步提示；
#   第二轮须含 {step1_output}，便于先乱想再约束成「每行/空格分隔的编号」等机器友好格式。
# - step04 / step06：单次 call_llm；占位符 {abstract} {paper_body_excerpt}
# - step08：translate_figure_captions 批量图注中译；缓存目录 step08_figure_caption_zh/{aid}.json
# PipelineConfig.focus_selection_llm_runs 控制 step02 合并轮数；缓存单文件 step02_focus_llm.json（output）
# ---------------------------------------------------------------------------
PROMPT_STEP02_FOCUS_STEP1 = """
{paper_list}
上述是今日论文列表。请通读标题与编号，思考哪些与以下的领域强相关。请你思考后给出答案。
3D生成、3D重建、计算机图形学、Mesh几何处理、3D参数化表达、3D表达、3D理解
"""

PROMPT_STEP02_FOCUS_STEP2 = """
{step1_output}
上述为第一轮分析草稿，可能杂乱。
请只根据上文，输出与3D相关的 所有 arXiv 编号，
格式严格便于程序解析：仅编号本身，多个编号用空格分隔，
格式如 2604.01234，不要其它说明文字。
"""

# 新的单篇论文判断提示词
PROMPT_STEP02_JUDGE_SINGLE = """
论文标题：{title}
论文摘要：{abstract}

请判断这篇论文是否与以下领域强相关：
3D生成、3D重建、计算机图形学、Mesh几何处理、3D参数化表达、3D表达、3D理解

请只回答"是"或"否"，不要任何解释。
"""

PROMPT_STEP04_SUMMARY = """
{abstract}
请你先给出这篇论文是人工智能下属的哪个一级和哪个二级领域（不包含人工智能）, 2个词语, 分号隔开
然后请用两句话概括上述论文摘要的核心内容：他的背景/任务是什么。他做了什么。
输出3行，第一行是2个分号隔开的领域，第二行是背景/任务，第三行是做了什么。
"""

PROMPT_STEP06_DEEP = """
{paper_body_excerpt}
上述是从 arXiv HTML 抽取的正文片段，请你当我是一个低年级博士生，只拥有对该领域比较浅的认知
但是对基础知识比如Transformer模型之类的都了解
用简单的语言告诉我这篇论文的核心内容.
(1) 这篇论文所在的任务是什么: 任务输入, 任务输出, 任务功能
(2) 这篇论文想解决什么问题
(3) 论文的核心思路是什么
(4) 结果怎么样
请你使用简体中文输出
"""

PROMPT_STEP08_CAPTION_ZH = """下面是同一篇论文的 {n} 条英文图注（可能含「Figure 1」等编号与 LaTeX 转写噪声）。
请按顺序逐条翻译为流畅的**简体中文**，保留学术语气；必要时可保留无法翻译的专有名词英文。

图注列表：
{numbered_captions}

**只输出**一个 JSON 数组，长度必须为 {n}，第 i 个元素对应上文 [i]。每个元素为字符串。
不要输出 Markdown 代码围栏、不要加任何解释。示例格式：["第一条译文","第二条译文"]"""


if __name__ == "__main__":
    my_api_key = os.getenv("MY_API_KEY")
    cfg = PipelineConfig()
    pipeline = PaperPipeline(my_api_key, cfg)
    today = datetime.now(timezone.utc)
    pipeline.run_pipeline(today.strftime("%Y-%m-%d"), force_rerun=["step01"])
 
    
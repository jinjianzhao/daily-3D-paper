"""
每日定时调度 run_pipeline.py，按固定整点列表运行。

启动时：
1. 读取全局变量 DAILY_SLOTS（0~23 的整点小时列表，去重排序后生效），
2. 每 5 分钟轮询一次，若当前小时命中未执行的时刻则立刻运行，
3. 每天 0 点重置执行记录，重新开始新一天。

环境变量 MY_API_KEY 会自动传递给子进程。
"""

import os
import sys
import time
from datetime import datetime, timedelta, timezone

CST = timezone(timedelta(hours=8))
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.join(SCRIPT_DIR, "run_pipeline.py")
POLL_INTERVAL = 60 * 5  # 5 分钟
DAILY_SLOTS: list[int] = [2, 10, 19]


def build_daily_slots() -> list[int]:
    """读取 DAILY_SLOTS 并规范化为 (0~23) 的去重排序列表。"""
    assert isinstance(DAILY_SLOTS, list), "DAILY_SLOTS 必须是 list[int]"
    assert all(isinstance(h, int) for h in DAILY_SLOTS), "DAILY_SLOTS 必须是 list[int]"
    assert len(DAILY_SLOTS) > 0, "DAILY_SLOTS 不能为空"
    assert all(0 <= h <= 23 for h in DAILY_SLOTS), "DAILY_SLOTS 每个小时必须在 0~23 之间"
    return sorted(set(DAILY_SLOTS))

def run_cmd(cmd: str) -> int:
    """通过 os.system 调用命令，继承当前进程环境变量。"""
    ret = os.system(cmd)
    if ret != 0:
        print(f"[scheduler:{cmd}] 返回非零 exit code: {ret}", flush=True)
    else:
        print(f"[scheduler:{cmd}] 执行完毕", flush=True)
    return ret

def run_pipeline_once():
    """依次执行 pull → date pipeline → area pipeline → push。"""
    auto_pull = os.path.join(SCRIPT_DIR, "auto_pull.sh")
    run_cmd(f'cd "{SCRIPT_DIR}" && bash "{auto_pull}"')

    auto_pipeline = os.path.join(SCRIPT_DIR, "run_pipeline.py")
    run_cmd(f'cd "{SCRIPT_DIR}" && "{sys.executable}" "{auto_pipeline}"')

    auto_notion_area = os.path.join(SCRIPT_DIR, "area_processor.py")
    run_cmd(f'cd "{SCRIPT_DIR}" && "{sys.executable}" "{auto_notion_area}"')

    auto_push = os.path.join(SCRIPT_DIR, "auto_push.sh")
    run_cmd(f'cd "{SCRIPT_DIR}" && bash "{auto_push}"')

def main():
    # 启动时立刻跑一次，及早发现错误
    print(f"[scheduler] 启动，先执行一次 pipeline ...", flush=True)
    run_pipeline_once()

    slots = build_daily_slots()
    print(f"[scheduler] 今日执行时段（整点）: {slots}", flush=True)

    executed: set[int] = set()
    last_date = datetime.now(CST).strftime("%Y-%m-%d")

    while True:
        now = datetime.now(CST)
        today = now.strftime("%Y-%m-%d")
        hour = now.hour

        # 跨天重置
        if today != last_date:
            slots = build_daily_slots()
            executed = set()
            last_date = today
            print(f"[scheduler] 新的一天 {today}，重置，执行时段: {slots}", flush=True)

        if hour in slots and hour not in executed:
            print(f"[scheduler] 当前 {now.strftime('%H:%M')} 命中时段 {hour}:00，开始执行", flush=True)
            run_pipeline_once()
            executed.add(hour)
            remaining = [s for s in slots if s not in executed]
            print(f"[scheduler] 今日剩余时段: {remaining}", flush=True)

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()

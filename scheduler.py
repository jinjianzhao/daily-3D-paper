"""
每日定时调度 run_pipeline.py，每天运行 6 次（间隔约 4 小时）。

启动时：
1. 取当前整点小时 h0（向下取整），
2. 以 h0 为锚点算出当天 6 个固定执行时刻：h0, h0+4, h0+8, h0+12, h0+16, h0+20（模 24，去重排序），
3. 每 5 分钟轮询一次，若当前小时命中未执行的时刻则立刻运行，
4. 每天 0 点重置执行记录，重新开始新一天。

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


def build_daily_slots() -> list[int]:
    """以当前整点为锚，生成当天 6 个执行时刻（0~23，去重排序）。"""
    now_h = datetime.now(CST).hour
    raw = [(now_h + 4 * i) % 24 for i in range(6)]
    return sorted(set(raw))


def run_pipeline_once():
    """通过 os.system 调用 run_pipeline.py，继承当前进程环境变量。"""
    cmd = f'"{sys.executable}" "{PIPELINE}"'
    print(f"[scheduler] 执行: {cmd}", flush=True)
    ret = os.system(cmd)
    if ret != 0:
        print(f"[scheduler] pipeline 返回非零 exit code: {ret}", flush=True)
    else:
        print(f"[scheduler] pipeline 执行完毕", flush=True)


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

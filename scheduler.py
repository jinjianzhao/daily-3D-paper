"""
每日定时调度，date pipeline 和 area pipeline 分别按各自策略运行。

DAILY_SLOTS       → pull → date pipeline → push（整点触发）
AREA_INTERVAL_SEC → area pipeline（固定间隔轮询）

共享一把互斥锁，保证同一时刻只有一个 pipeline 在跑。
area watcher 拿不到锁就跳过本轮，date pipeline 拿不到锁就等待。
"""

import os
import sys
import time
import threading
from datetime import datetime, timedelta, timezone

CST = timezone(timedelta(hours=8))
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DAILY_SLOTS: list[int] = [2, 10, 19]
AREA_INTERVAL_SEC: int = 120

# 全局互斥锁：date 和 area 不同时跑
_mutex = threading.Lock()


def _validate_slots(slots: list[int], name: str) -> list[int]:
    assert isinstance(slots, list) and all(isinstance(h, int) and 0 <= h <= 23 for h in slots), \
        f"{name} 必须是 0~23 的整数列表"
    return sorted(set(slots))


def _run(cmd: str):
    print(f"[scheduler] $ {cmd}", flush=True)
    ret = os.system(cmd)
    if ret != 0:
        print(f"[scheduler] exit code {ret}", flush=True)


def _cd(script: str) -> str:
    return f'cd "{SCRIPT_DIR}" && {script}'


def do_date_pipeline():
    """pull → date pipeline → push。阻塞等锁。"""
    with _mutex:
        print(f"[date] === 开始 ===", flush=True)
        _run(_cd('bash auto_pull.sh'))
        _run(_cd(f'"{sys.executable}" run_pipeline.py'))
        _run(_cd('bash auto_push.sh'))
        print(f"[date] === 结束 ===", flush=True)


def do_area_pipeline():
    """area pipeline。非阻塞尝试拿锁，拿不到就跳过。"""
    acquired = _mutex.acquire(blocking=False)
    if not acquired:
        print(f"[area] 其他 pipeline 正在运行，跳过", flush=True)
        return
    try:
        print(f"[area] === 开始 ===", flush=True)
        _run(_cd(f'"{sys.executable}" area_processor.py'))
        print(f"[area] === 结束 ===", flush=True)
    finally:
        _mutex.release()


def _area_loop():
    """后台线程：每隔 AREA_INTERVAL_SEC 执行一次 area pipeline。"""
    while True:
        do_area_pipeline()
        time.sleep(AREA_INTERVAL_SEC)


def main():
    daily_slots = _validate_slots(DAILY_SLOTS, "DAILY_SLOTS")
    print(f"[scheduler] date 时段: {daily_slots}  area 间隔: {AREA_INTERVAL_SEC}s", flush=True)

    # 启动时各跑一次
    do_date_pipeline()
    do_area_pipeline()

    # 启动 area 后台线程
    threading.Thread(target=_area_loop, daemon=True).start()

    # 主线程负责 date pipeline
    daily_executed: set[int] = set()
    last_date = datetime.now(CST).strftime("%Y-%m-%d")

    while True:
        now = datetime.now(CST)
        today = now.strftime("%Y-%m-%d")
        hour = now.hour

        if today != last_date:
            daily_executed = set()
            last_date = today
            print(f"[scheduler] 新的一天 {today}", flush=True)

        if hour in daily_slots and hour not in daily_executed:
            print(f"[scheduler] {now.strftime('%H:%M')} 命中 date 时段", flush=True)
            do_date_pipeline()
            daily_executed.add(hour)

        time.sleep(60)


if __name__ == "__main__":
    main()

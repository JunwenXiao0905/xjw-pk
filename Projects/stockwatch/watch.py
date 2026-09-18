#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""持续盯盘 — 终端原地刷新, 看起来就像在跑任务/看日志. Ctrl+C 退出.

用法:
  python watch.py                    # 盯 watchlist.txt 自选
  python watch.py 600519 300750      # 盯指定代码
  python watch.py 贵州茅台 半导体 BK1036  # 名称/板块也行(自动解析)
  python watch.py --interval 5       # 刷新间隔秒数(默认 10)
  python watch.py --log              # 日志模式: 每次刷新追加一行, 更低调
"""
import os
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quote import (fetch, load_watchlist, resolve_arg, render_term,
                   fmt_num, market_status)
from groups import expand

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def parse_args(argv):
    interval, log_mode, color = 10.0, False, True
    codes, i = [], 0
    while i < len(argv):
        a = argv[i]
        if a == "--interval" and i + 1 < len(argv):
            try:
                interval = max(2.0, float(argv[i + 1]))
            except ValueError:
                pass
            i += 2
            continue
        if a == "--log":
            log_mode = True
        elif a == "--no-color":
            color = False
        else:
            codes.append(a)
        i += 1
    return interval, log_mode, color, codes


def main(argv):
    interval, log_mode, color, codes = parse_args(argv)
    targets = expand(codes) if codes else load_watchlist()
    secids = [s for s in (resolve_arg(c) for c in targets) if s]
    if not secids:
        print("无有效代码")
        return 1
    prev_lines = 0
    while True:
        now = datetime.now()
        err = None
        rows = None
        try:
            rows = fetch(secids)
        except Exception as e:
            err = e
        try:
            if log_mode:
                if rows:
                    body = " ".join(
                        f"{d.get('f14')} {fmt_num(d.get('f2'))}"
                        f"({fmt_num(d.get('f3'), pct=True, sign=True)})"
                        for d in rows)
                    print(f"[{now:%H:%M:%S}] {body}", flush=True)
                else:
                    print(f"[{now:%H:%M:%S}] fetch error: {err}", flush=True)
            else:
                if prev_lines:
                    sys.stdout.write("\033[%dA\033[J" % prev_lines)
                text = (render_term(rows, now, color=color) if rows
                        else f"{now:%H:%M:%S} 获取行情失败: {err}, {int(interval)}s后重试")
                print(text, flush=True)
                prev_lines = text.count("\n") + 1
        except KeyboardInterrupt:
            print("\n已停止盯盘")
            return 0
        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\n已停止盯盘")
            return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""10:10 趋势观察器 — 战法来源: 用户2026-09-15发现, 经50日数据验证.

用法:
  python timing.py                 # 全部核心ETF
  python timing.py 515880 159516   # 指定标的

规则(基于 m15 数据统计, 2026-07-07~09-15):
  - 10:15 bar 开盘价 vs 今日开盘价 -> 方向信号, 预测收盘方向
  - A股ETF整体 ~72-78%, 低开反弹日 ~83-85%
  - 用途: 10:10 定当日基调, 不操作; 操作仍走 14:30 决策窗
"""
import os
import sys
import json
import time
import urllib.request
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quote import resolve_arg

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0"}

DEFAULTS = ["159516", "515880", "513120", "513770", "159801", "159586"]


def _get(url, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5)
    raise last


def load_m15(sym):
    raw = _get("https://proxy.finance.qq.com/ifzqgtimg/appstock/app/kline/mkline?param=%s,m15,,800" % sym)
    bars = json.loads(raw)["data"][sym]["m15"]
    days = defaultdict(dict)  # date -> {hhmm: (bar_open, bar_close)}
    for b in bars:
        days[b[0][:8]][b[0][8:]] = (float(b[1]), float(b[2]))
    return days


def analyze(sym, name):
    days = load_m15(sym)
    dates = sorted(days)

    def close_of(d):
        ts = sorted(days[d])
        return days[d][ts[-1]][1]

    prev_close = {}
    for i, d in enumerate(dates):
        ts = sorted(days[d])
        prev_close[d] = days[d][ts[0]][0] if i == 0 else close_of(dates[i - 1])

    total = hit = low_total = low_hit = 0
    for d in dates[1:]:
        ts = sorted(days[d])
        o = days[d][ts[0]][0]
        c = close_of(d)
        p10 = days[d].get("1015")
        if p10 is None or abs(c - o) < 1e-9:
            continue
        act = c > o
        total += 1
        hit += (p10[0] > o) == act
        if o < prev_close[d]:
            low_total += 1
            low_hit += (p10[0] > o) == act

    # 今日信号
    today = dates[-1]
    ts = sorted(days[today])
    o = days[today][ts[0]][0]
    p10 = days[today].get("1015")
    gap = "高开" if o > prev_close[today] else ("低开" if o < prev_close[today] else "平开")
    if p10:
        sig = "反弹站回开盘上方 → 偏强" if p10[0] > o else "跌破开盘下方 → 偏弱"
        bias = "偏强" if p10[0] > o else "偏弱"
    else:
        sig = "(未到10:15或数据缺失)"
        bias = "—"
    hist = "%.0f%% (%d日)" % (hit / total * 100, total) if total else "—"
    lowh = "%.0f%% (%d日)" % (low_hit / low_total * 100, low_total) if low_total >= 5 else "样本少"
    print("%s %s" % (name, sym))
    print("  今日: %s | 10:15信号: %s → 今日基调[%s]" % (gap, sig, bias))
    print("  历史命中率: %s | 低开日: %s" % (hist, lowh))
    print()


def main(argv):
    targets = []
    for a in argv:
        s = resolve_arg(a)
        if s:
            targets.append((a, s))
    if not targets:
        targets = [(c, c) for c in DEFAULTS]
    print("== 10:10 趋势观察 (腾讯m15, 近50交易日回测) ==")
    print("   战法: 10:15价>今开=偏强; 低开日反弹确认最强(A股ETF ~85%)")
    print("   注意: 只定基调不操作, 操作在14:30决策窗\n")
    for disp, secid in targets:
        # 腾讯符号: 沪 sh / 深 sz
        code = secid.split(".")[-1]
        prefix = "sh" if secid.startswith("1.") else "sz"
        try:
            analyze(prefix + code, disp)
        except Exception as e:  # noqa: BLE001
            print("%s %s  获取失败: %s\n" % (disp, code, repr(e)[:50]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

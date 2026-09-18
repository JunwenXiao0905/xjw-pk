#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""K线图 — 终端ASCII蜡烛图 / matplotlib图片 (东方财富, 前复权)

用法:
  python kline.py 贵州茅台              # 终端ASCII日K, 近60根
  python kline.py 600519 --png          # 图片版: 近120日, MA5/10/20+成交量
  python kline.py BK1036 --png          # 板块指数也能画
  python kline.py 贵州茅台 --week       # 周K (另有 --month)
  python kline.py 600519 -n 90          # 指定根数
  通用: --no-color
"""
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quote import _http_get, resolve_arg, RED, GREEN, DIM, RESET

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
CHART_DIR = os.path.join(BASE, "charts")

KLINE_URL = ("https://push2his.eastmoney.com/api/qt/stock/kline/get"
             "?secid={}&klt={klt}&fqt=1&beg=0&end=20500101"
             "&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57"
             "&ut=fa5fd1943c7b386f172d6893dbfba10b")
KLT_NAMES = {101: "日", 102: "周", 103: "月"}


def fetch_kline(secid, klt=101):
    d = json.loads(_http_get(KLINE_URL.format(secid, klt=klt)).decode("utf-8"))
    data = d.get("data") or {}
    bars = []
    for line in data.get("klines") or []:
        p = line.split(",")
        if len(p) < 7:
            continue
        bars.append({"date": p[0], "open": float(p[1]), "close": float(p[2]),
                     "high": float(p[3]), "low": float(p[4]),
                     "vol": float(p[5]), "amount": float(p[6])})
    return data.get("name") or secid, bars


def ma(closes, p):
    return sum(closes[-p:]) / p if len(closes) >= p else None


def render_ascii(bars, name, secid, klt_name, color=True):
    n = len(bars)
    H = 18
    lo = min(b["low"] for b in bars)
    hi = max(b["high"] for b in bars)
    mid = (hi + lo) / 2
    half = (hi - lo) * 0.55 or 1.0        # 上下留点白
    hi2, lo2 = mid + half, mid - half

    def row(p):
        return int(round((hi2 - p) / (hi2 - lo2) * (H - 1)))

    grid = [[" "] * n for _ in range(H)]
    style = [[None] * n for _ in range(H)]
    for c, b in enumerate(bars):
        up = b["close"] >= b["open"]
        st = RED if up else GREEN
        for r in range(row(b["high"]), row(b["low"]) + 1):
            grid[r][c], style[r][c] = "│", st
        r1, r2 = row(max(b["open"], b["close"])), row(min(b["open"], b["close"]))
        for r in range(r1, r2 + 1):
            grid[r][c], style[r][c] = ("█" if up else "▒"), st

    closes = [b["close"] for b in bars]
    last, prev = bars[-1], bars[-2] if n > 1 else bars[-1]
    pct = (last["close"] / prev["close"] - 1) * 100 if prev["close"] else 0
    mas = " ".join(f"MA{p}:{ma(closes, p):.2f}" for p in (5, 10, 20) if ma(closes, p))
    lines = [f"{name} {secid.split('.', 1)[1]} {klt_name}K 近{n}根  "
             f"{bars[0]['date'][2:]}~{last['date'][2:]}  最新{last['close']:.2f}({pct:+.2f}%)  {mas}"]
    legend = " " * 10 + "(█涨 ▒跌 │影线)"
    lines.append(f"{DIM}{legend}{RESET}" if color else legend)
    for r in range(H):
        label = f"{hi2 - r / (H - 1) * (hi2 - lo2):>9.2f}│" if r % 6 == 0 else " " * 10
        cells = []
        for c in range(n):
            ch, st = grid[r][c], style[r][c]
            if color and st and ch != " ":
                cells.append(f"{st}{ch}{RESET}")
            else:
                cells.append(ch)
        lines.append(label + "".join(cells))
    return "\n".join(lines)


def render_png(bars, name, code, klt_name, out_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
    plt.rcParams["axes.unicode_minus"] = False

    UP, DOWN = "#e74c3c", "#26a69a"       # 红涨绿跌(阳线空心, 阴线实心)
    xs = range(len(bars))
    closes = [b["close"] for b in bars]

    fig, (ax, axv) = plt.subplots(2, 1, figsize=(14, 7.5), sharex=True, dpi=120,
                                  gridspec_kw={"height_ratios": [3, 1]})
    for i, b in enumerate(bars):
        up = b["close"] >= b["open"]
        col = UP if up else DOWN
        ax.vlines(i, b["low"], b["high"], color=col, linewidth=0.8)
        h = abs(b["close"] - b["open"]) or b["close"] * 1e-4
        ax.add_patch(Rectangle((i - 0.35, min(b["open"], b["close"])), 0.7, h,
                               facecolor="white" if up else DOWN,
                               edgecolor=col, linewidth=0.8))
        axv.bar(i, b["vol"], width=0.7, color=col, alpha=0.75)
    for p, colr in ((5, "#f5a623"), (10, "#2d8cf0"), (20, "#9b59b6")):
        ys = ma(closes, p)
        if ys:
            ax.plot(xs, [None] * (p - 1) + [sum(closes[i - p + 1:i + 1]) / p
                                            for i in range(p - 1, len(closes))],
                    linewidth=1.1, color=colr, label=f"MA{p}={ys:.2f}")
    ax.legend(loc="upper left", fontsize=9)
    ax.set_title(f"{name}({code}) {klt_name}K线 · 前复权 · 截至{bars[-1]['date']}", fontsize=13)
    ax.set_ylabel("价格")
    ax.grid(alpha=0.25)
    axv.set_ylabel("成交量(手)", fontsize=9)
    axv.grid(alpha=0.25)
    step = max(1, len(bars) // 9)
    ticks = list(range(0, len(bars), step))
    if len(bars) - 1 not in ticks:
        ticks.append(len(bars) - 1)
    ax.set_xticks(ticks)
    ax.set_xticklabels([bars[i]["date"][2:] for i in ticks], fontsize=8)
    ax.set_xlim(-1, len(bars))
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def main(argv):
    color = "--no-color" not in argv
    png = "--png" in argv
    klt = 103 if "--month" in argv else 102 if "--week" in argv else 101
    num = 120 if png else 60
    if "-n" in argv:
        i = argv.index("-n")
        try:
            num = max(10, min(500, int(argv[i + 1])))
        except (ValueError, IndexError):
            pass
    args = [a for a in argv if not a.startswith("-")]
    if not args:
        print(__doc__)
        return 1
    secid = resolve_arg(args[0])
    if not secid:
        print(f"无法识别: {args[0]}")
        return 1
    code = secid.split(".", 1)[1]
    try:
        name, bars = fetch_kline(secid, klt)
    except Exception as e:
        print(f"获取K线失败: {e}")
        return 1
    if not bars:
        print(f"{name} 没有K线数据")
        return 1
    bars = bars[-num:]
    klt_name = KLT_NAMES[klt]
    if png:
        os.makedirs(CHART_DIR, exist_ok=True)
        out = os.path.join(CHART_DIR, f"{code}_{klt}.png")
        try:
            render_png(bars, name, code, klt_name, out)
        except ImportError:
            print("图片模式需要 matplotlib(pip install matplotlib), 或用终端模式")
            print(render_ascii(bars, name, secid, klt_name, color))
            return 1
        print(f"已生成: {out}")
    else:
        print(render_ascii(bars, name, secid, klt_name, color))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

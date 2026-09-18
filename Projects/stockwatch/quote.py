#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""实时行情快照(数据源: 东方财富免费接口, 无需 key)

用法(bash, .dataenv python 即可, 纯标准库):
  python quote.py                  # 查 watchlist.txt 里的自选
  python quote.py 600519 300750    # 查指定代码
  python quote.py --md             # 输出 markdown 表格(给 /stock 命令用)
  python quote.py --no-color       # 关闭 ANSI 颜色

代码格式:
  A股/ETF  6位数字:   600519 300750 510300 (5/6/9开头按沪市, 其余按深市)
  港股     4-5位数字: 00700 / 700
  美股     字母代码:  AAPL NVDA
  指数     原始secid: 1.000001(上证) 0.399001(深成) 0.399006(创业板)
  板块     BK代码:    BK1036(半导体)
  中文名/拼音(腾讯搜索自动解析): 贵州茅台 / maotai
"""
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from datetime import datetime, time as dtime

from groups import expand

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
WATCHLIST_FILE = os.path.join(BASE, "watchlist.txt")

EM_URL = ("https://push2.eastmoney.com/api/qt/ulist.np/get"
          "?fltt=2&fields=f2,f3,f4,f5,f6,f8,f12,f13,f14,f15,f16,f17,f18&secids={}")
TX_URL = "https://qt.gtimg.cn/q={}"

# 完整 UA 必须带: 接口会拒绝裸 "Mozilla/5.0"
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://quote.eastmoney.com/",
}

RED, GREEN, DIM, RESET = "\033[31m", "\033[32m", "\033[2m", "\033[0m"


def to_secid(raw):
    s = str(raw).strip().upper()
    if re.fullmatch(r"\d{1,3}\.[0-9A-Z]+", s):
        return s
    if re.fullmatch(r"BK\d+", s):
        return "90." + s
    if re.fullmatch(r"[A-Z]{1,6}", s):
        return "105." + s
    if re.fullmatch(r"\d{6}", s):
        return ("1." if s[0] in "569" else "0.") + s
    if re.fullmatch(r"\d{1,5}", s):
        return "116." + s.zfill(5)
    return None


def load_watchlist():
    items = []
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, encoding="utf-8") as f:
            for line in f:
                line = line.split("#", 1)[0].strip()
                if line:
                    items.append(line)
    return items


def _http_get(url, referer=None):
    """带重试的 GET(本机到行情接口偶发被掐断)"""
    headers = dict(BROWSER_HEADERS)
    if referer:
        headers["Referer"] = referer
    last = None
    for attempt in range(3):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.read()
        except Exception as e:
            last = e
            time.sleep(0.5 * (attempt + 1))
    raise last


def _fetch_eastmoney(secids):
    data = json.loads(_http_get(EM_URL.format(",".join(secids))).decode("utf-8"))
    return ((data.get("data") or {}).get("diff")) or []


def _to_tencent_symbol(secid):
    market, code = secid.split(".", 1)
    if market == "1":
        return "sh" + code
    if market == "0":
        return "sz" + code
    if market == "116":
        return "hk" + code
    if market == "105":
        return "us" + code.upper()
    return None


def _fetch_tencent(secids):
    """备用源(腾讯), 字段位置按 ~ 分隔: 1名称 2代码 3现价 4昨收 5今开
    31涨跌 32涨跌幅 33最高 34最低 37成交额万(仅A股)"""
    pairs = [(s, _to_tencent_symbol(s)) for s in secids]
    syms = ",".join(p for _, p in pairs if p)
    if not syms:
        return []
    text = _http_get(TX_URL.format(syms), referer="https://gu.qq.com/").decode("gbk", "replace")
    out = []
    for secid, sym in pairs:
        m = re.search(r'v_' + re.escape(sym) + r'="([^"]*)"', text)
        if not m or "~" not in m.group(1):
            continue
        p = m.group(1).split("~")
        market = secid.split(".", 1)[0]

        def num(i):
            try:
                return float(p[i])
            except (ValueError, IndexError):
                return None

        amount = None
        if market in ("0", "1") and len(p) > 37:
            try:
                amount = float(p[37]) * 1e4
            except ValueError:
                pass
        row = {
            "f14": p[1], "f12": secid.split(".", 1)[1],
            "f2": num(3), "f18": num(4), "f17": num(5),
            "f4": num(31), "f3": num(32), "f15": num(33), "f16": num(34),
            "f6": amount,
        }
        if market in ("0", "1") and len(p) > 38:      # A股 p[38]=换手率
            row["f8"] = num(38)
        out.append(row)
    return out


SMARTBOX = "https://smartbox.gtimg.cn/s3/?v=2&q={}&t=all"

# smartbox 市场前缀 -> eastmoney secid 前缀
_SMARTBOX_MARKET = {"sh": "1.", "sz": "0.", "bj": "0.", "hk": "116.", "us": "105."}


def smartbox_lookup(q):
    """腾讯智能搜索: 中文名/拼音 -> 候选 [(secid, 名称, 类型)]"""
    text = _http_get(SMARTBOX.format(urllib.parse.quote(str(q))),
                     referer="https://gu.qq.com/").decode("gbk", "replace")
    entries = []
    for m in re.finditer(r'"([^"~]*~[^"]*)"', text):
        for item in m.group(1).split("^"):
            p = item.split("~")
            if len(p) < 5:
                continue
            market, code, name, typ = p[0].lower(), p[1], p[2], p[4].upper()
            prefix = _SMARTBOX_MARKET.get(market)
            if prefix:
                entries.append((prefix + code, name, typ))

    def prio(e):
        t = e[2]
        return (0 if t.startswith("GP") else 1 if t == "ETF"
                else 2 if t == "ZS" else 3)

    entries.sort(key=prio)
    return entries


def resolve_arg(raw):
    """代码/中文名/拼音/BK代码 -> secid(名称解析结果缓存7天)"""
    s = str(raw).strip()
    secid = to_secid(s)
    if secid is not None and re.search(r"\d", s):
        return secid
    cached = _cache_get(s)
    if cached:
        return cached
    try:
        cands = smartbox_lookup(s)
        if cands:
            _cache_put(s, cands[0][0])
            return cands[0][0]
    except Exception:
        pass
    return secid


RESOLVE_CACHE_FILE = os.path.join(BASE, "resolve_cache.json")
RESOLVE_CACHE_TTL = 7 * 86400


def _cache_get(key):
    try:
        with open(RESOLVE_CACHE_FILE, encoding="utf-8") as f:
            c = json.load(f)
        v, ts = c[key]
        if time.time() - float(ts) < RESOLVE_CACHE_TTL:
            return v
    except Exception:
        pass
    return None


def _cache_put(key, value):
    try:
        try:
            with open(RESOLVE_CACHE_FILE, encoding="utf-8") as f:
                c = json.load(f)
        except Exception:
            c = {}
        c[key] = [value, time.time()]
        with open(RESOLVE_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(c, f, ensure_ascii=False)
    except Exception:
        pass


BOARD_URL = ("https://push2.eastmoney.com/api/qt/stock/get"
             "?secid={}&ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2"
             "&fields=f43,f44,f45,f46,f48,f57,f58,f60,f168,f169,f170")


def _fetch_board(secid):
    """板块指数(90.BKxxxx) ulist 不支持, 走 stock/get 单查"""
    d = json.loads(_http_get(BOARD_URL.format(secid)).decode("utf-8")).get("data") or {}
    if not d.get("f57"):
        return None
    return {"f2": d.get("f43"), "f15": d.get("f44"), "f16": d.get("f45"),
            "f17": d.get("f46"), "f6": d.get("f48"), "f12": d.get("f57"),
            "f14": d.get("f58"), "f18": d.get("f60"), "f4": d.get("f169"),
            "f3": d.get("f170"), "f8": d.get("f168")}


def _fetch_normal(secids):
    """东财优先, 失败切腾讯, 腾讯也空再回试东财一次"""
    try:
        return _fetch_eastmoney(secids)
    except Exception as first_err:
        try:
            rows = _fetch_tencent(secids)
            if rows:
                return rows
        except Exception:
            pass
        try:
            return _fetch_eastmoney(secids)
        except Exception:
            raise first_err


def fetch(secids):
    """按请求顺序返回行情(股票/指数/板块混合)"""
    rows_by_code = {}
    err = None
    normal = [s for s in secids if not s.startswith("90.")]
    if normal:
        try:
            for r in _fetch_normal(normal):
                rows_by_code[r.get("f12")] = r
        except Exception as e:
            err = e
    for s in [s for s in secids if s.startswith("90.")]:
        try:
            r = _fetch_board(s)
            if r:
                rows_by_code[r["f12"]] = r
        except Exception as e:
            if err is None:
                err = e
    rows = [rows_by_code[s.split(".", 1)[1]] for s in secids
            if s.split(".", 1)[1] in rows_by_code]
    if not rows:
        raise err or RuntimeError("无数据")
    return rows


def market_status(now=None):
    now = now or datetime.now()
    t, wd = now.time(), now.weekday()
    if wd >= 5:
        return "休市·周末"
    if t < dtime(9, 15):
        return "未开盘"
    if t < dtime(9, 30):
        return "集合竞价"
    if t <= dtime(11, 30):
        return "交易中"
    if t < dtime(13, 0):
        return "午间休市"
    if t <= dtime(15, 0):
        return "交易中"
    return "已收盘"


def dwidth(s):
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in str(s))


def pad(s, w, left=False):
    s = str(s)
    fill = " " * max(0, w - dwidth(s))
    return fill + s if left else s + fill


def trunc(s, w):
    """按显示宽度截断, 超长补省略号"""
    s = str(s)
    out, cw = "", 0
    for ch in s:
        cwid = 2 if unicodedata.east_asian_width(ch) in "WF" else 1
        if cw + cwid > w - 1:
            return out + "…"
        out += ch
        cw += cwid
    return out


def fmt_num(v, pct=False, sign=False):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return "--"
    if pct:
        return f"{x:+.2f}%" if sign else f"{x:.2f}%"
    return f"{x:+.2f}" if sign else f"{x:.2f}"


def fmt_amount(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return "--"
    return f"{x/1e8:.1f}亿" if x >= 1e8 else f"{x/1e4:.0f}万"


def tone(pct):
    try:
        x = float(pct)
    except (TypeError, ValueError):
        return ""
    return RED if x > 0 else GREEN if x < 0 else ""


def render_term(rows, now, color=True):
    def c(s, code):
        return f"{code}{s}{RESET}" if (color and code) else s
    lines = [f"{now:%Y-%m-%d %H:%M:%S}  {DIM}{market_status(now)} · 东方财富实时{RESET}",
             DIM + (pad("名称", 12) + pad("代码", 8) + pad("最新", 9) + pad("涨跌", 8)
                    + pad("涨跌幅", 8) + pad("今开", 9) + pad("最高", 9) + pad("最低", 9)
                    + pad("成交额", 8)) + RESET]
    for d in rows:
        t = tone(d.get("f3"))
        lines.append(
            pad(trunc(d.get("f14", "--"), 12), 12) + pad(d.get("f12", "--"), 8)
            + c(pad(fmt_num(d.get("f2")), 9), t)
            + c(pad(fmt_num(d.get("f4"), sign=True), 8), t)
            + c(pad(fmt_num(d.get("f3"), pct=True, sign=True), 8), t)
            + pad(fmt_num(d.get("f17")), 9) + pad(fmt_num(d.get("f15")), 9)
            + pad(fmt_num(d.get("f16")), 9) + pad(fmt_amount(d.get("f6")), 8))
    return "\n".join(lines)


def render_md(rows, now):
    out = [f"> {now:%Y-%m-%d %H:%M} · {market_status(now)}", "",
           "| 名称 | 代码 | 最新 | 涨跌 | 涨跌幅 | 今开 | 最高 | 最低 | 成交额 |",
           "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for d in rows:
        out.append(
            f"| {d.get('f14', '--')} | {d.get('f12', '--')} | {fmt_num(d.get('f2'))} "
            f"| {fmt_num(d.get('f4'), sign=True)} | {fmt_num(d.get('f3'), pct=True, sign=True)} "
            f"| {fmt_num(d.get('f17'))} | {fmt_num(d.get('f15'))} | {fmt_num(d.get('f16'))} "
            f"| {fmt_amount(d.get('f6'))} |")
    return "\n".join(out)


def main(argv):
    md = "--md" in argv
    color = "--no-color" not in argv
    raw = expand([a for a in argv if not a.startswith("--")] or load_watchlist())
    pairs = [(r, resolve_arg(r)) for r in raw]
    bad = [r for r, s in pairs if s is None]
    secids = [s for _, s in pairs if s]
    if not secids:
        print("无有效代码" + (f", 无法识别: {' '.join(bad)}" if bad else " (watchlist.txt 为空?)"))
        return 1
    try:
        rows = fetch(secids)
    except Exception as e:
        print(f"获取行情失败: {e}")
        return 1
    if bad:
        print(f"已忽略无法识别的代码: {' '.join(bad)}")
    if not rows:
        print("接口未返回数据, 请检查代码是否正确")
        return 1
    now = datetime.now()
    print(render_md(rows, now) if md else render_term(rows, now, color))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""板块榜单 / 个股榜单 / 板块成分股 (东方财富免费接口)

用法:
  python list.py industry              # 行业板块涨幅榜(默认前20)
  python list.py concept               # 概念板块涨幅榜
  python list.py region                # 地域板块涨幅榜
  python list.py up [N]                # 个股涨幅榜前N(默认20)
  python list.py down [N]              # 跌幅榜
  python list.py amount [N]            # 成交额榜
  python list.py turnover [N]          # 换手率榜
  python list.py board 半导体           # 板块成分股涨幅榜(名称模糊匹配或BK代码)
  python list.py board BK1036
  通用参数: --md(markdown输出) --no-color --top N(条数, 默认20, 上限200)
"""
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quote import (_http_get, fetch, resolve_arg, pad, trunc, fmt_num, fmt_amount,
                   tone, market_status, DIM, RESET)
from groups import load_groups, get_group

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CLIST = ("https://push2.eastmoney.com/api/qt/clist/get"
         "?pn={pn}&pz={pz}&po={po}&np=1&fltt=2&invt=2&fid={fid}&fs={fs}&fields={fields}")

SUGGEST = ("https://searchadapter.eastmoney.com/api/suggest/get"
           "?input={}&type=14&token=D43BF722C8E33BDC906FB84D85E326E8&count=20")

TX_RANK = ("https://proxy.finance.qq.com/cgi/cgi-bin/rank/pt/getRank"
           "?board_type={bt}&sort_type=PriceRatio&direct=down&offset=0&count={n}")
TX_BOARD_KINDS = {"industry": "hy", "concept": "gn"}   # 腾讯板块榜兜底(东财限流时)

SINA_RANK = ("https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/"
             "Market_Center.getHQNodeData?page={page}&num={num}&sort={sort}&asc={asc}&node=hs_a")
SINA_SORTS = {"up": ("changepercent", 0), "down": ("changepercent", 1),
              "amount": ("amount", 0), "turnover": ("turnoverratio", 0)}   # 新浪个股榜兜底


def _fetch_stocks_sina(kind, top):
    sort, asc = SINA_SORTS[kind]
    rows, page = [], 1
    while len(rows) < top:
        num = min(100, top - len(rows))
        raw = _http_get(SINA_RANK.format(page=page, num=num, sort=sort, asc=asc),
                        referer="https://finance.sina.com.cn")
        try:
            items = json.loads(raw.decode("utf-8"))
        except UnicodeDecodeError:
            items = json.loads(raw.decode("gbk", "replace"))
        if not items or len(items) < num:
            rows.extend({"f14": d.get("name"), "f12": str(d.get("symbol", ""))[2:],
                         "f2": d.get("trade"), "f3": d.get("changepercent"),
                         "f6": d.get("amount"), "f8": d.get("turnoverratio")}
                        for d in items)
            break
        rows.extend({"f14": d.get("name"), "f12": str(d.get("symbol", ""))[2:],
                     "f2": d.get("trade"), "f3": d.get("changepercent"),
                     "f6": d.get("amount"), "f8": d.get("turnoverratio")} for d in items)
        page += 1
    return rows[:top]


def _fetch_boards_tencent(kind, top):
    data = json.loads(_http_get(TX_RANK.format(bt=TX_BOARD_KINDS[kind], n=top),
                                referer="https://gu.qq.com/").decode("utf-8"))
    rows = []
    for d in ((data.get("data") or {}).get("rank_list")) or []:
        updn = str(d.get("zgb", "/")).split("/")
        lzg = d.get("lzg") or {}
        rows.append({
            "f14": d.get("name", "--"), "f12": d.get("code", "--"),
            "f3": d.get("zdf"),
            "f104": updn[0] if updn and updn[0] else "--",
            "f105": updn[1] if len(updn) > 1 and updn[1] else "--",
            "f128": lzg.get("name", "--"), "f136": lzg.get("zdf"),
        })
    return rows[:top]

CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "boards_cache.json")
CACHE_TTL = 6 * 3600   # 板块清单缓存6小时(翻全量列表易触发接口限流)

BOARD_KINDS = {"industry": ("m:90+t:2", "行业板块"),
               "concept": ("m:90+t:3", "概念板块"),
               "region": ("m:90+t:1", "地域板块")}
STOCK_FS = "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048"   # 沪深京A股
BOARD_FIELDS = "f3,f12,f14,f104,f105,f128,f136,f140"
STOCK_FIELDS = "f2,f3,f6,f8,f12,f14"
STOCK_KINDS = {"up": ("f3", 1, "涨幅榜"), "down": ("f3", 0, "跌幅榜"),
               "amount": ("f6", 1, "成交额榜"), "turnover": ("f8", 1, "换手率榜")}


def clist(fs, fid="f3", po=1, top=20, fields=STOCK_FIELDS):
    rows, pn = [], 1
    while len(rows) < top:
        pz = min(100, top - len(rows))
        url = CLIST.format(pn=pn, pz=pz, po=po, fid=fid,
                           fs=urllib.parse.quote(fs, safe=""), fields=fields)
        data = json.loads(_http_get(url).decode("utf-8"))
        d = data.get("data") or {}
        diff = d.get("diff") or []
        if not diff:
            break
        rows.extend(diff)
        if len(rows) >= int(d.get("total") or 0):
            break
        pn += 1
        time.sleep(0.4)          # 连续翻页太快会被接口限流掐断
    return rows[:top]


def _header(title, now, color=True):
    t = f"{now:%Y-%m-%d %H:%M}  {market_status(now)} · {title}"
    return f"{DIM}{t}{RESET}" if color else t


def render_boards(rows, title, now, color=True, md=False):
    if md:
        out = [f"> {now:%Y-%m-%d %H:%M} · {market_status(now)} · {title}", "",
               "| 板块 | 代码 | 涨跌幅 | 涨/跌家数 | 领涨股 | 领涨股涨幅 |",
               "|---|---|---:|---:|---|---:|"]
        for d in rows:
            out.append(
                f"| {d.get('f14', '--')} | {d.get('f12', '--')} "
                f"| {fmt_num(d.get('f3'), pct=True, sign=True)} "
                f"| {d.get('f104', '--')}/{d.get('f105', '--')} "
                f"| {d.get('f128', '--')} "
                f"| {fmt_num(d.get('f136'), pct=True, sign=True)} |")
        return "\n".join(out)

    def c(s, code):
        return f"{code}{s}{RESET}" if (color and code) else s

    lines = [_header(title, now, color),
             DIM + (pad("板块", 18) + pad("代码", 8) + pad("涨跌幅", 9)
                    + pad("涨/跌", 8) + pad("领涨股", 10) + pad("领涨%", 9)) + RESET]
    for d in rows:
        lines.append(
            pad(trunc(d.get("f14", "--"), 18), 18) + pad(d.get("f12", "--"), 8)
            + c(pad(fmt_num(d.get("f3"), pct=True, sign=True), 9), tone(d.get("f3")))
            + pad(f"{d.get('f104', '--')}/{d.get('f105', '--')}", 8)
            + pad(trunc(d.get("f128", "--"), 10), 10)
            + c(pad(fmt_num(d.get("f136"), pct=True, sign=True), 9), tone(d.get("f136"))))
    return "\n".join(lines)


def render_stocks(rows, title, now, color=True, md=False):
    if md:
        out = [f"> {now:%Y-%m-%d %H:%M} · {market_status(now)} · {title}", "",
               "| 名称 | 代码 | 最新 | 涨跌幅 | 成交额 | 换手率 |",
               "|---|---|---:|---:|---:|---:|"]
        for d in rows:
            out.append(
                f"| {d.get('f14', '--')} | {d.get('f12', '--')} | {fmt_num(d.get('f2'))} "
                f"| {fmt_num(d.get('f3'), pct=True, sign=True)} "
                f"| {fmt_amount(d.get('f6'))} | {fmt_num(d.get('f8'), pct=True)} |")
        return "\n".join(out)

    def c(s, code):
        return f"{code}{s}{RESET}" if (color and code) else s

    lines = [_header(title, now, color),
             DIM + (pad("#", 4) + pad("名称", 10) + pad("代码", 8) + pad("最新", 9)
                    + pad("涨跌幅", 9) + pad("成交额", 9) + pad("换手率", 7)) + RESET]
    for i, d in enumerate(rows, 1):
        t = tone(d.get("f3"))
        lines.append(
            pad(str(i), 4) + pad(d.get("f14", "--"), 10) + pad(d.get("f12", "--"), 8)
            + c(pad(fmt_num(d.get("f2")), 9), t)
            + c(pad(fmt_num(d.get("f3"), pct=True, sign=True), 9), t)
            + pad(fmt_amount(d.get("f6")), 9)
            + pad(fmt_num(d.get("f8"), pct=True), 7))
    return "\n".join(lines)


def _load_board_cache():
    try:
        with open(CACHE_FILE, encoding="utf-8") as f:
            c = json.load(f)
        if time.time() - float(c.get("ts") or 0) < CACHE_TTL:
            return c.get("boards") or []
    except Exception:
        pass
    return None


def _save_board_cache(boards):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({"ts": time.time(), "boards": boards}, f, ensure_ascii=False)
    except Exception:
        pass


def _resolve_board_suggest(q):
    """搜索接口按名称/拼音解析板块, 单请求(避免全量翻页触发限流)"""
    data = json.loads(_http_get(SUGGEST.format(urllib.parse.quote(str(q)))).decode("utf-8"))
    items = ((data.get("QuotationCodeTable") or {}).get("Data")) or []
    bks = [(d.get("Code"), d.get("Name")) for d in items if d.get("Classify") == "BK"]
    if not bks:
        return None, None
    exact = [b for b in bks if b[1] == q]
    return exact[0] if exact else bks[0]


def group_stats(rows):
    pcts = [r["f3"] for r in rows if isinstance(r.get("f3"), (int, float))]
    avg = sum(pcts) / len(pcts) if pcts else None
    up = sum(1 for p in pcts if p > 0)
    dn = sum(1 for p in pcts if p < 0)
    return len(pcts), avg, up, dn


def render_group_summary(entries, title, now, color=True, md=False):
    if md:
        out = [f"> {now:%Y-%m-%d %H:%M} · {market_status(now)} · {title}", "",
               "| 分组 | 只数 | 平均涨跌幅 | 涨/跌 |",
               "|---|---:|---:|---:|"]
        for gname, n, avg, up, dn in entries:
            a = f"{avg:+.2f}%" if avg is not None else "--"
            out.append(f"| {gname} | {n} | {a} | {up}/{dn} |")
        return "\n".join(out)

    def c(s, code):
        return f"{code}{s}{RESET}" if (color and code) else s

    lines = [_header(title, now, color),
             DIM + (pad("分组", 14) + pad("只数", 5) + pad("平均涨跌幅", 10)
                    + pad("涨/跌", 8)) + RESET]
    for gname, n, avg, up, dn in entries:
        a = f"{avg:+.2f}%" if avg is not None else "--"
        lines.append(
            pad(trunc(gname, 14), 14) + pad(str(n), 5)
            + c(pad(a, 10), tone(avg)) + pad(f"{up}/{dn}", 8))
    return "\n".join(lines)


def _fetch_rotation(top):
    data = json.loads(_http_get(TX_RANK.format(bt="hy", n=100),
                                referer="https://gu.qq.com/").decode("utf-8"))
    rows = []
    for d in ((data.get("data") or {}).get("rank_list")) or []:
        try:
            rows.append({"f14": d.get("name", "--"),
                         "d0": float(d.get("zdf") or 0),
                         "d5": float(d.get("zdf_d5") or 0),
                         "d20": float(d.get("zdf_d20") or 0)})
        except (TypeError, ValueError):
            continue
    rows.sort(key=lambda r: r["d0"], reverse=True)
    return rows[:top]


def _rot_signal(d0, d5):
    if d0 >= 0 and d5 >= 0:
        return "延续强势"
    if d0 >= 0 > d5:
        return "低位回升"
    if d0 < 0 <= d5:
        return "高位回落"
    return "延续弱势"


def render_rotation(rows, now, color=True, md=False):
    if md:
        out = [f"> {now:%Y-%m-%d %H:%M} · 行业板块轮动(今日/5日/20日)", "",
               "| 板块 | 今日 | 5日 | 20日 | 信号 |",
               "|---|---:|---:|---:|---|"]
        for r in rows:
            out.append(f"| {r['f14']} | {r['d0']:+.2f}% | {r['d5']:+.2f}% "
                       f"| {r['d20']:+.2f}% | {_rot_signal(r['d0'], r['d5'])} |")
        return "\n".join(out)

    def c(s, v):
        t = tone(v)
        return f"{t}{s}{RESET}" if (color and t) else s

    lines = [_header("行业板块轮动(今日/5日/20日)", now, color),
             DIM + (pad("板块", 12) + pad("今日", 8) + pad("5日", 8)
                    + pad("20日", 8) + "信号") + RESET]
    for r in rows:
        lines.append(pad(trunc(r["f14"], 12), 12)
                     + c(pad(f"{r['d0']:+.2f}%", 8), r["d0"])
                     + c(pad(f"{r['d5']:+.2f}%", 8), r["d5"])
                     + c(pad(f"{r['d20']:+.2f}%", 8), r["d20"])
                     + _rot_signal(r["d0"], r["d5"]))
    return "\n".join(lines)


def resolve_board(q):
    s = q.strip()
    if re.fullmatch(r"BK\d+", s.upper()):
        return s.upper(), s.upper()
    try:
        code, name = _resolve_board_suggest(s)
        if code:
            return code, name
    except Exception:
        pass
    all_boards = _load_board_cache()
    if all_boards is None:
        all_boards = clist(BOARD_KINDS["industry"][0], top=1000, fields=BOARD_FIELDS)
        all_boards += clist(BOARD_KINDS["concept"][0], top=1000, fields=BOARD_FIELDS)
        _save_board_cache(all_boards)
    exact = [r for r in all_boards if r.get("f14") == s]
    if exact:
        return exact[0]["f12"], exact[0]["f14"]
    cands = [r for r in all_boards if s in r.get("f14", "")]
    if cands:
        return cands[0]["f12"], cands[0]["f14"]
    return None, None


SW_L1 = ["农林牧渔", "基础化工", "钢铁", "有色金属", "电子", "家用电器", "食品饮料",
         "纺织服饰", "轻工制造", "医药生物", "公用事业", "交通运输", "房地产",
         "商贸零售", "社会服务", "综合", "建筑材料", "建筑装饰", "电力设备",
         "国防军工", "计算机", "传媒", "通信", "银行", "非银金融", "汽车",
         "机械设备", "石油石化", "环保", "美容护理"]


def fetch_day_boards(date8):
    """历史某日:申万一级行业当日涨跌幅(逐板块拉日K)."""
    cached = _load_board_cache()
    if cached is None:                       # 过期则现场重建(只用行业板块)
        cached = clist(BOARD_KINDS["industry"][0], top=1000, fields=BOARD_FIELDS)
    boards = {b["f14"]: b["f12"] for b in (cached or [])
              if b.get("f14") in SW_L1}
    ds = "{}-{}-{}".format(date8[:4], date8[4:6], date8[6:])
    rows, miss = [], 0
    for name, bk in boards.items():
        url = ("https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=90.{}"
               "&fields1=f1&fields2=f51,f59&klt=101&fqt=0&lmt=45&end=20500101").format(bk)
        try:
            kl = json.loads(_http_get(url))["data"]["klines"]
            hit = next((r for r in kl if r.startswith(ds)), None)
            if hit:
                rows.append((name, float(hit.split(",")[1])))
            else:
                miss += 1
        except Exception:
            miss += 1
        time.sleep(0.12)
    rows.sort(key=lambda x: -x[1])
    return rows, miss


def day_view(date8, top=12, color=True, md=False):
    out = []
    brd, miss = fetch_day_boards(date8)
    out.append("== {} 行业当日涨幅(申万一级{} ==".format(
        date8, ",缺{}个" .format(miss) if miss else ""))
    if md:
        out += ["| 行业 | 当日 |", "|---|---:|"]
        out += ["| {} | {:+.2f}% |".format(n, v) for n, v in brd]
    else:
        for n, v in brd:
            out.append("  {:+7.2f}%  {}".format(v, n))
    # 涨停池按行业分组
    pool, dd, tc = fetch_ztpool(date8, 300)
    grp = {}
    for r in pool:
        grp.setdefault(r["hy"] or "其他", []).append(r)
    out += ["", "== {} 涨停分布({}家,按行业) ==".format(dd, tc or len(pool))]
    for hy in sorted(grp, key=lambda k: -len(grp[k])):
        ss = grp[hy]
        line = "  {}({}): ".format(hy, len(ss)) + " | ".join(
            "{} {}板/{}".format(r["name"], r["lbc"], r["fbt"]) for r in ss)
        out.append(line)
    return chr(10).join(out)


def fetch_ztpool(date=None, top=20):
    """东财涨停池:按首次封板时间升序(封板越早=主力优先级越高).date=YYYYMMDD可选."""
    import urllib.request, json as _json
    d = date or datetime.now().strftime("%Y%m%d")
    url = ("https://push2ex.eastmoney.com/getTopicZTPool?ut=7eea3edcaed734bea9cbfc24409ed989"
           "&dpt=wz.ztzt&Pageindex=0&pagesize={}&sort=fbt%3Aasc&date={}").format(max(top, 100), d)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = (_json.loads(urllib.request.urlopen(req, timeout=10).read()) or {}).get("data") or {}
    rows = []
    for x in (data.get("pool") or [])[:top]:
        fbt = str(x.get("fbt") or 0).zfill(6)     # HMMSS: 92500=09:25:00
        t = "{:02d}:{}".format(int(fbt[:2]), fbt[2:4])
        rows.append({"name": x.get("n"), "code": x.get("c"),
                     "fbt": t, "lbc": x.get("lbc") or 1, "zbc": x.get("zbc") or 0,
                     "hy": x.get("hybk") or ""})
    return rows, data.get("date") or d, data.get("tc")


def render_ztpool(rows, date, total, now, color=True, md=False):
    head = "涨停池 {} (共{}家,按封板时间排序,炸板次数>0标!)"
    if md:
        out = ["| 封板时间 | 股票 | 代码 | 连板 | 炸板 | 行业 |", "|---|---|---|---:|---:|---|"]
        for r in rows:
            out.append("| {} | {} | {} | {} | {} | {} |".format(
                r["fbt"], r["name"], r["code"], r["lbc"], r["zbc"] or "-", r["hy"]))
        return "> " + now.strftime("%m-%d %H:%M") + " · " + head.format(date, total) + "\n\n" + "\n".join(out)
    lines = [head.format(date, total),
             "{:<8} {:<10} {:<8} {:>4} {:>4} {}".format("封板", "股票", "代码", "连板", "炸板", "行业")]
    for r in rows:
        lines.append("{:<8} {:<10} {:<8} {:>4} {:>4} {}".format(
            r["fbt"], r["name"], r["code"], r["lbc"], r["zbc"] or "-", r["hy"]))
    return chr(10).join(lines)


def parse_args(argv):
    md = "--md" in argv
    color = "--no-color" not in argv
    top, args, i = 20, [], 0
    while i < len(argv):
        a = argv[i]
        if a == "--top" and i + 1 < len(argv):
            try:
                top = max(1, min(200, int(argv[i + 1])))
            except ValueError:
                pass
            i += 2
            continue
        if a in ("--md", "--no-color"):
            i += 1
            continue
        args.append(a)
        i += 1
    return md, color, top, args


def main(argv):
    md, color, top, args = parse_args(argv)
    if not args:
        print(__doc__)
        return 1
    cmd, rest = args[0].lower(), args[1:]
    if rest and rest[0].isdigit():                     # up 30 简写
        top = max(1, min(200, int(rest[0])))
        rest = rest[1:]
    now = datetime.now()
    try:
        if cmd in BOARD_KINDS:
            fs, title = BOARD_KINDS[cmd]
            try:
                rows = clist(fs, fid="f3", po=1, top=top, fields=BOARD_FIELDS)
            except Exception:
                rows = _fetch_boards_tencent(cmd, top) if cmd in TX_BOARD_KINDS else []
            print(render_boards(rows, f"{title}涨幅榜(前{len(rows)})", now, color, md))
        elif cmd in ("rotation", "rot"):
            rows = _fetch_rotation(top)
            print(render_rotation(rows, now, color, md))
        elif cmd in ("zt", "ztpool"):
            # 日期参数可能被通用逻辑误吃成top,从原始args里找8位日期
            d = next((a for a in args[1:] if len(a) == 8 and a.isdigit() and a.startswith("20")), None)
            if top > 200:
                top = 20
            rows, dd, tc = fetch_ztpool(d, top)
            print(render_ztpool(rows, dd, tc, now, color, md))
        elif cmd == "day":
            d = next((a for a in args[1:] if len(a) == 8 and a.isdigit() and a.startswith("20")), None)
            if not d:
                print("用法: python list.py day 20260916")
                return 1
            print(day_view(d, top, color, md))
        elif cmd in STOCK_KINDS:
            fid, po, title = STOCK_KINDS[cmd]
            try:
                rows = clist(STOCK_FS, fid=fid, po=po, top=top, fields=STOCK_FIELDS)
            except Exception:
                rows = _fetch_stocks_sina(cmd, top)
            print(render_stocks(rows, f"个股{title}(前{len(rows)})", now, color, md))
        elif cmd == "group":
            gs = load_groups()
            if not rest:
                print("用法: python list.py group <组名>。现有分组: "
                      + ("、".join(gs) if gs else "(还没有, 在 groups.txt 里定义)"))
                return 0
            gname = " ".join(rest)
            members = get_group(gname)
            if members is None:
                print(f"没有分组 [{gname}]。现有分组: "
                      + ("、".join(gs) if gs else "(还没有)"))
                return 1
            secids = [s for s in (resolve_arg(m) for m in members) if s]
            rows = fetch(secids)
            n, avg, up, dn = group_stats(rows)
            a = f"{avg:+.2f}%" if avg is not None else "--"
            print(render_stocks(rows, f"{gname} · {n}只 · 平均{a} · 涨{up}/跌{dn}",
                                now, color, md))
        elif cmd in ("groups", "gs"):
            gs = load_groups()
            if not gs:
                print("还没有分组: 在 groups.txt 里用 [组名]+每行一个代码 定义")
                return 0
            secid_of = {c: resolve_arg(c) for c in
                        {m for ms in gs.values() for m in ms}}
            uniq = [s for s in dict.fromkeys(secid_of.values()) if s]
            rows_by_code = {r["f12"]: r for r in fetch(uniq)}
            entries = []
            for gname, members in gs.items():
                rows = [rows_by_code[s.split(".", 1)[1]] for s in
                        (secid_of.get(m) for m in members)
                        if s and s.split(".", 1)[1] in rows_by_code]
                entries.append((gname, *group_stats(rows)))
            print(render_group_summary(entries, "自定义分组总览", now, color, md))
        elif cmd == "board":
            if not rest:
                print("用法: python list.py board <板块名或BK代码>")
                return 1
            code, name = resolve_board(" ".join(rest))
            if not code:
                print(f"找不到板块: {' '.join(rest)} (先跑 industry/concept 可看全部板块名)")
                return 1
            rows = clist("b:" + code, fid="f3", po=1, top=top, fields=STOCK_FIELDS)
            print(render_stocks(rows, f"{name} 成分股涨幅榜(前{len(rows)})", now, color, md))
        else:
            print(__doc__)
            return 1
    except Exception as e:
        print(f"获取失败: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

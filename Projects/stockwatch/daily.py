#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每日复盘自动生成器 — 生成三个文件:
  今日持仓和盈亏.md: 持仓表(自动) + 今日操作/反思(手填)
  大盘分析.md:       指数量能+行业前5+轮动信号+池内ETF全景(全部自动,markdown表格)
  博主复盘学习.md:   固定博主模板(六边形/C哥/强哥/岚哥/野哥/布衣/歌神小易)+仓位轨迹

用法:
  python daily.py              # 打印到屏幕预览
  python daily.py --save       # 写入 Obsidian 每日信息/{当日}/ 两个文件(已存在则跳过)

持仓登记: D:/projects/xjw-pk/Areas/基金股票/持仓登记.md(Obsidian里直接编辑)
原理: 净值=东财基金页(昨日);当日%=参考ETF场内实时(盘中估值接口fundgz已被东财下线,已验证404)
"""
import json
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quote import _http_get, load_watchlist, resolve_arg, fetch

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.normpath(os.path.join(BASE, "..", "..", "Areas", "基金股票"))  # 相对脚本定位vault,随目录迁移
POSITIONS = os.path.join(VAULT, "持仓登记.md")
WATCH_STOCKS = os.path.join(VAULT, "个股盯盘清单.md")


def fmt_pct(v):
    try:
        return "{:+.2f}%".format(float(v))
    except (TypeError, ValueError):
        return "--"


def load_positions():
    rows = []
    with open(POSITIONS, encoding="utf-8") as f:
        for line in f:
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 6 or cells[0] in ("代码", "---") or set(cells[0]) <= {"-", " "}:
                continue
            rows.append({
                "code": cells[0], "name": cells[1], "kind": cells[2],
                "shares": float(cells[3] or 0),
                "cost": float(cells[4]) if cells[4] not in ("-", "", "0") else None,
                "ref": cells[5], "note": cells[6] if len(cells) > 6 else "",
            })
    return rows


def load_watch_stocks():
    """读取个股盯盘清单:只取 热盯/试温 状态的股票."""
    rows = []
    if not os.path.exists(WATCH_STOCKS):
        return rows
    with open(WATCH_STOCKS, encoding="utf-8") as f:
        for line in f:
            t = line.strip()
            if not t.startswith("|"):
                continue
            cells = [c.strip() for c in t.strip("|").split("|")]
            if len(cells) < 6 or cells[0].startswith("股票") or set(cells[0]) <= {"-", " "}:
                continue
            m = re.search(r"(\d{6})", cells[0])
            if m and ("\U0001F525" in cells[1] or "\U0001F321" in cells[1]):
                rows.append({"code": m.group(1)})
    return rows


def fund_nav(code):
    try:
        html = _http_get("https://fund.eastmoney.com/{}.html".format(code),
                         referer="https://fund.eastmoney.com/").decode("utf-8", "replace")
        m = re.search(r"单位净值.*?(\d+\.\d{4})", html, re.S)
        return float(m.group(1)) if m else None
    except Exception:
        return None


def build(now):
    pos = load_positions()
    ref_secids = []
    for p in pos:
        s = resolve_arg(p["ref"])
        if s and s not in ref_secids:
            ref_secids.append(s)
    idx_secids = ["1.000001", "0.399001", "0.399006", "1.000688", "0.399106"]
    Q = {}
    for s in idx_secids + ref_secids:
        try:
            r = fetch([s])[0]
            Q[r.get("f12")] = r
        except Exception:
            pass
    idx = {c: Q.get(c, {}) for c in ["000001", "399001", "399006", "000688"]}

    # ---- 大盘分析.md ----
    mkt = ["# 大盘(自动生成 {})".format(now.strftime("%Y-%m-%d %H:%M")), ""]
    try:
        amt = (float(idx["000001"].get("f6") or 0) + float(Q.get("399106", {}).get("f6") or 0)) / 1e8
        mkt += ["**两市成交 {:.0f}亿**".format(amt), "",
                "| 指数 | 点位 | 涨跌幅 | 指数 | 点位 | 涨跌幅 |",
                "|---|---:|---:|---|---:|---:|"]
        order = ["000001", "399001", "399006", "000688"]
        for pair in [(0, 1), (2, 3)]:
            cells = []
            for c in (order[pair[0]], order[pair[1]]):
                if idx.get(c):
                    cells += [idx[c]["f14"], str(idx[c].get("f2", "--")), fmt_pct(idx[c].get("f3"))]
            if cells:
                mkt.append("| " + " | ".join(cells) + " |")
        mkt.append("")
    except Exception:
        pass
    try:
        amounts = {}
        for secid in ("1.000001", "0.399001"):
            url = ("https://push2his.eastmoney.com/api/qt/stock/kline/get?secid={}"
                   "&fields1=f1&fields2=f51,f57&klt=101&fqt=0&lmt=6&end=20500101").format(secid)
            try:
                for row in json.loads(_http_get(url))["data"]["klines"]:
                    dt, amt = row.split(",")
                    amounts[dt] = amounts.get(dt, 0) + float(amt)
            except Exception:
                pass
        if amounts:
            mkt += ["## 近5日两市成交额(自动)", "", "| 日期 | 成交额 |", "|---|---:|"]
            for dt in sorted(amounts)[-5:]:
                mkt.append("| {} | {:.2f}万亿 |".format(dt[5:].replace("-", "/"), amounts[dt] / 1e12))
            mkt.append("")
    except Exception:
        pass
    try:
        from list import _fetch_rotation, render_rotation
        mkt += ["## 板块轮动(自动)", "", render_rotation(_fetch_rotation(8), now, color=False, md=True), ""]
    except Exception:
        pass
    try:
        secids = [s for s in (resolve_arg(c) for c in load_watchlist()) if s]
        from quote import render_md
        table = render_md(fetch(secids), now)
        mkt += ["## 池内ETF全景(自动)", "", table, ""]
    except Exception as e:
        mkt += ["(池内全景失败: {})".format(e), ""]
    try:
        ws = load_watch_stocks()
        if ws:
            secids = [x for x in (resolve_arg(w["code"]) for w in ws) if x]
            from quote import render_md as _rmd
            mkt += ["## 盯盘股票(自动,来自[[个股盯盘清单]]的热盯/试温)", "",
                    _rmd(fetch(secids), now), ""]
    except Exception as e:
        mkt += ["(盯盘股票失败: {})".format(e), ""]
    mkt += ["## 推动因素分析(手填)", "", "## 个股分析(手填)", ""]

    # ---- 今日持仓和盈亏.md ----
    hd = ["# 持仓(自动:净值=昨日,当日%=参考ETF场内)", "",
          "| 名称 | 代码 | 类型 | 净值(昨) | 当日 | 市值 | 总盈亏 | 备注 |",
          "|---|---|---|---:|---:|---:|---:|---|"]
    for p in pos:
        is_etf = "etf" in p["kind"].lower()
        ref = p["code"] if is_etf else p["ref"]          # 场内ETF参考自身
        q = Q.get(ref, {})
        nav = (float(q.get("f2") or 0) or None) if is_etf else fund_nav(p["code"])
        name = (q.get("f14") or p.get("name") or p["code"]) if is_etf             else (p.get("name") or q.get("f14") or p["code"])
        mval = "{:.0f}".format(nav * p["shares"]) if (nav and p["shares"]) else "--"
        pl = "{:+.0f}".format((nav - p["cost"]) * p["shares"]) if (nav and p["shares"] and p["cost"]) else "--"
        hd.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
            name, p["code"], p["kind"],
            "{:.4f}".format(nav) if nav else "--", fmt_pct(q.get("f3")), mval, pl, p["note"]))
    hd += ["", "> 份额待填:支付宝→持仓→『持有份额』→ 更新 [[持仓登记]]", "",
           "# 今日操作(手填)", "", "# 反思(手填)", ""]

    # ---- 博主复盘学习.md ----
    bl = ["# 博主复盘学习(自动生成 {})".format(now.strftime("%Y-%m-%d")), "",
          "> 用法:每天扫一遍各博主,记**仓位猜测**(大多看不到具体,猜板块+大致比例)和观点;不跟单。",
          "> 原则:只记录观点和仓位,重要的写一行『我的判断』;月底回看关键日谁说了什么。", ""]
    bloggers = [
        ("六边形(大盘/技术面/有色)", None),
        ("C哥(养基,大资金)", None),
        ("强哥(支付宝可见约70w,全科技风格)", """### 仓位轨迹
| 日期 | 板块猜测(比例) | 当日操作 | 我的判断 |
|---|---|---|---|
| 9/15 | 全科技~70%:嘉实28.8w/华泰质量成长8w/科创芯片5.6w/弘毅4.6w/平安3.6w/广发设备2.8w/央企红利2.5w+债9w | 加科创芯片1w、医疗1w;减债2w | 当日涨当日加=追涨;医疗次日回调验证 |
"""),
        ("岚哥(游资/短线)", None),
        ("野哥(游资,MLCC+大消费)", """### 仓位轨迹
| 日期 | 持仓猜测 | 当日操作 | 我的判断 |
|---|---|---|---|
| 9/15 | MLCC(双星新材涨停)/大消费(国芳、百大跌停) | — | 大消费情绪退潮印证 |
"""),
        ("布衣", None),
        ("歌神小易", None),
    ]
    for title, seed in bloggers:
        bl.append("## " + title)
        bl.append("")
        if seed:
            bl += [seed]
        bl += ["- **仓位(猜)**:", "- **今日观点**:", ""]
    plan = ["# 后期规划(自动生成 {})".format(now.strftime("%Y-%m-%d")), "",
            "> 明天唯一要盯的事:", "", "> 待办:", "", "> 灵感/疑问:", ""]
    return {"今日持仓和盈亏.md": "\n".join(hd), "大盘分析.md": "\n".join(mkt),
            "博主复盘学习.md": "\n".join(bl), "后期规划.md": "\n".join(plan)}


def main(argv):
    now = datetime.now()
    files = build(now)
    if "--save" in argv:
        day = now.strftime("%m%d")
        folder = os.path.join(VAULT, "每日信息", day)
        os.makedirs(folder, exist_ok=True)
        for name, content in files.items():
            path = os.path.join(folder, name)
            # 大盘分析=纯自动数据,始终覆盖(手动模板会挡住生成);
            # 持仓盈亏=手写反思区,已存在则跳过
            if os.path.exists(path) and name != "大盘分析.md":
                print("已存在,跳过:", path)
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print("已生成:", path)
    else:
        for name, content in files.items():
            print("=" * 12, name, "=" * 12)
            print(content)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

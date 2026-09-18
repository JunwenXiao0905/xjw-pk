#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自定义分组(同花顺"自定义板块/分组"的平替)

文件: groups.txt, INI 风格:

    [组名]
    贵州茅台
    600519
    半导体        # 板块也行
    002475       # 注释随意写

用法: list.py group <组名> / list.py groups(总览) / quote.py @组名 / watch.py @组名
"""
import os

GROUPS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "groups.txt")


def load_groups():
    groups, cur = {}, None
    if not os.path.exists(GROUPS_FILE):
        return groups
    with open(GROUPS_FILE, encoding="utf-8") as f:
        for line in f:
            s = line.split("#", 1)[0].strip()
            if not s:
                continue
            if s.startswith("[") and s.endswith("]"):
                cur = s[1:-1].strip()
                if cur:
                    groups.setdefault(cur, [])
            elif cur:
                groups[cur].append(s)
    return groups


def get_group(name):
    return load_groups().get(str(name).strip())


def expand(items):
    """把列表里的 @组名 展开成组成员, 其余原样返回"""
    out = []
    for it in items:
        if isinstance(it, str) and it.startswith("@"):
            g = get_group(it[1:])
            if g:
                out.extend(g)
                continue
        out.append(it)
    return out

#!/usr/bin/env python3
"""新增/更新一期：复制 HTML 到 digests/、注入返回链接、更新 digests.json、重建 index.html。
用法: python3 scripts/add_digest.py <源HTML> --date YYYY-MM-DD --count N --highlight "一句话看点" [--range "覆盖范围"]
"""
import argparse, json, pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("--date", required=True)
ap.add_argument("--count", type=int, required=True); ap.add_argument("--highlight", required=True)
ap.add_argument("--range", default="")
a = ap.parse_args()
s = pathlib.Path(a.src).read_text(encoding="utf-8")
BACK = ('<nav class="backnav" style="max-width:920px;margin:0 auto;padding:16px 18px 0">'
        '<a href="../index.html" style="display:inline-block;text-decoration:none;color:#2b6cb0;'
        'font-weight:700;font-size:14px;background:#fff;border:1px solid #9cc5f0;border-radius:999px;'
        'padding:5px 16px;box-shadow:0 2px 8px rgba(43,108,176,.1)">← 返回往期目录</a></nav>')
if 'class="backnav"' not in s:
    s, n = re.subn(r"(<body[^>]*>)", r"\1" + BACK, s, count=1)
    if n != 1: sys.exit("未找到 <body> 标签")
(ROOT / "digests").mkdir(exist_ok=True)
(ROOT / "digests" / f"{a.date}.html").write_text(s, encoding="utf-8")
mf = ROOT / "digests.json"
items = [x for x in json.loads(mf.read_text(encoding="utf-8")) if x["date"] != a.date]
items.append({"date": a.date, "count": a.count, "range": a.range, "highlight": a.highlight})
items.sort(key=lambda x: x["date"], reverse=True)
mf.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
subprocess.run([sys.executable, str(ROOT / "scripts" / "build_index.py")], check=True)

#!/usr/bin/env python3
"""新增/替换一期，并更新 digests.json 与 index.html。
推荐（新模板）：
  python3 scripts/add_digest.py --json data/YYYY-MM-DD.json
    读取结构化数据 → 用 scripts/render_digest.py 渲染 digests/YYYY-MM-DD.html（含返回目录链接）
    篇数、覆盖范围、一句话看点自动取自 JSON（count=len(papers)、range、highlight）
兼容（旧方式，直接放入现成 HTML）：
  python3 scripts/add_digest.py 源.html --date YYYY-MM-DD --count N --highlight "..." [--range "..."]
"""
import argparse, json, pathlib, re, shutil, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT
ap = argparse.ArgumentParser()
ap.add_argument("src", nargs="?"); ap.add_argument("--json")
ap.add_argument("--date"); ap.add_argument("--count", type=int)
ap.add_argument("--highlight"); ap.add_argument("--range", default="")
a = ap.parse_args()
(ROOT / "digests").mkdir(exist_ok=True)
if a.json:
    jp = pathlib.Path(a.json).resolve()
    D = json.loads(jp.read_text(encoding="utf-8"))
    dst = ROOT / "data" / f'{D["date"]}.json'
    if jp != dst.resolve():
        dst.parent.mkdir(exist_ok=True); shutil.copyfile(jp, dst)
    from render_digest import render
    (ROOT / "digests" / f'{D["date"]}.html').write_text(render(D), encoding="utf-8")
    entry = {"date": D["date"], "count": len(D["papers"]), "range": D.get("range", ""), "highlight": D["highlight"]}
else:
    if not (a.src and a.date and a.count and a.highlight):
        sys.exit("用法错误：使用 --json，或提供 源.html --date --count --highlight")
    s = pathlib.Path(a.src).read_text(encoding="utf-8")
    if "../index.html" not in s:
        back = ('<nav style="max-width:760px;margin:0 auto;padding:16px 22px 0;font-size:14px">'
                '<a href="../index.html" style="color:#2b6cb0;text-decoration:none">← 返回往期目录</a></nav>')
        s, n = re.subn(r"(<body[^>]*>)", r"\1" + back, s, count=1)
        if n != 1: sys.exit("未找到 <body> 标签")
    (ROOT / "digests" / f"{a.date}.html").write_text(s, encoding="utf-8")
    entry = {"date": a.date, "count": a.count, "range": a.range, "highlight": a.highlight}
mf = ROOT / "digests.json"
items = [x for x in json.loads(mf.read_text(encoding="utf-8")) if x["date"] != entry["date"]]
items.append(entry); items.sort(key=lambda x: x["date"], reverse=True)
mf.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f'已写入 digests/{entry["date"]}.html（{entry["count"]} 篇）')
subprocess.run([sys.executable, str(ROOT / "scripts" / "build_index.py")], check=True)
subprocess.run([sys.executable, str(ROOT / "scripts" / "build_search.py")], check=True)

#!/usr/bin/env python3
"""从 data/*.json 生成 search-index.json 和 search.html（索引内联，离线也可用）。"""
import json, re, html, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, head, hjfy

def text(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()

docs = []
for f in sorted((ROOT / "data").glob("*.json")):
    D = json.loads(f.read_text(encoding="utf-8"))
    date = D["date"]
    for i, p in enumerate(D.get("papers", []), 1):
        comps = " ".join(f'{c["name"]}：{text(c["html"])}' for c in p.get("components", []))
        docs.append({
            "id": p["id"], "short": p.get("short", ""), "title": p["title"], "zh": p.get("zh", ""),
            "aff": p.get("aff", ""), "tags": p.get("tags", []), "date": date, "stars": p.get("stars", 0),
            "problem": text(p.get("problem")), "method": (text(p.get("idea")) + " " + comps).strip(),
            "setup": text(p.get("setup")), "results": text(p.get("results")), "why": text(p.get("why")),
            "url": f"digests/{date}.html#p{i}", "arxiv": f"https://arxiv.org/abs/{p['id']}", "hjfy": hjfy(p["id"]),
            "code": p.get("code") or "", "brief": False})
    for o in D.get("others", []):
        docs.append({
            "id": o["id"], "short": o["title"].split(":")[0], "title": o["title"], "zh": "", "aff": "", "tags": ["简要"],
            "date": date, "stars": 0, "problem": "", "method": text(o.get("desc")), "setup": "", "results": "", "why": "",
            "url": f"digests/{date}.html#others", "arxiv": f"https://arxiv.org/abs/{o['id']}", "hjfy": hjfy(o["id"]),
            "code": "", "brief": True})

idx = json.dumps(docs, ensure_ascii=False, separators=(",", ":"))
(ROOT / "search-index.json").write_text(idx + "\n", encoding="utf-8")
tpl = (ROOT / "templates" / "search.html").read_text(encoding="utf-8")
page = head("搜索往期论文 · 视频生成后训练 arXiv 每日精选") + tpl.replace("/*__INDEX__*/[]", idx.replace("</", "<\\/")) + "</body></html>"
(ROOT / "search.html").write_text(page, encoding="utf-8")
print(f"search-index.json / search.html 已生成，共 {len(docs)} 条")

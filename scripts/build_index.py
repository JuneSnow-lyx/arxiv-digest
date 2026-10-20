#!/usr/bin/env python3
"""根据 digests.json 生成 index.html（往期目录，按日期倒序，最新一期突出显示）。"""
import json, html, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, head, cn_date
items = sorted(json.loads((ROOT / "digests.json").read_text(encoding="utf-8")), key=lambda x: x["date"], reverse=True)
out = [head("视频生成后训练 · arXiv 每日精选 · 往期目录"), '<div class="wrap">',
       '<div class="topbar"><span class="brand"><span class="dot"></span>arXiv 每日精选</span><span>每个工作日更新</span></div>',
       '<span class="eyebrow">Video Generation · Post-Training</span>',
       '<h1 class="title">视频生成后训练 · 每日论文精选</h1>',
       '<p class="lede">聚焦视频生成模型的后训练：蒸馏、少步采样、缓存、稀疏注意力、量化，以及 RL / 偏好对齐与长视频生成效率。每期精读 3–8 篇，讲清问题、方法与真实结果。</p>',
       f'<div class="facts"><span>共 <b>{len(items)}</b> 期</span><span>最近更新 <b>{items[0]["date"] if items else "-"}</b></span><span>数据来源 arXiv</span></div>',
       '<h2 class="section-h">往期目录</h2><p class="section-sub">按日期倒序 · 点击卡片阅读</p><div class="issues">']
for i, it in enumerate(items):
    dc, wd = cn_date(it["date"])
    latest = i == 0
    out.append(f'<a class="issue{" latest" if latest else ""}" href="digests/{it["date"]}.html">'
               f'<div class="d">{dc}<span style="font-size:.7em;color:var(--muted)"> · {wd}</span>{"<span class=badge>最新一期</span>" if latest else ""}</div>'
               f'<div class="m">精选 {it["count"]} 篇{(" · " + html.escape(it["range"])) if it.get("range") else ""}</div>'
               f'<p>{html.escape(it["highlight"])}</p><span class="go">阅读本期 →</span></a>')
out.append('</div><footer>由 论文推送Bot 生成 · 所有数字均来自论文原文</footer></div></body></html>')
(ROOT / "index.html").write_text("\n".join(out), encoding="utf-8")
print(f"index.html 已生成，共 {len(items)} 期")

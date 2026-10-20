#!/usr/bin/env python3
"""把一期的结构化数据（data/YYYY-MM-DD.json）渲染为单文件自包含 HTML。
用法: python3 scripts/render_digest.py data/2026-10-20.json [-o 输出路径]
默认输出到 digests/<date>.html。JSON 字段见 README。字符串字段允许内联 HTML（<b>/<mark>/<code>/<sub> 等）。"""
import json, sys, argparse, html, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, head, cn_date

def stars(s):
    full = int(s); half = (s - full) >= 0.5
    return ("★" * full + ('<span style="opacity:.45">★</span>' if half else "") + f'<span class="off">{"★" * (5 - full - (1 if half else 0))}</span>'
            + f'<span class="sc">{s:g}</span>')

def render(D, back_link=True):
    date_cn, wd = cn_date(D["date"])
    P = D["papers"]
    out = [head(f'视频生成后训练 · arXiv 每日精选 · {D["date"]}'), '<div class="wrap">']
    out.append('<div class="topbar"><span class="brand"><span class="dot"></span>arXiv 每日精选</span>'
               + ('<a href="../index.html">← 返回往期目录</a>' if back_link else '') + '</div>')
    out.append('<span class="eyebrow">Video Generation · Post-Training</span>')
    out.append('<h1 class="title">视频生成后训练 · 每日论文精选</h1>')
    out.append(f'<p class="lede">{D.get("lede","聚焦视频生成模型的后训练：蒸馏、少步采样、缓存、稀疏注意力、量化，以及 RL / 偏好对齐与长视频生成效率。")}</p>')
    out.append(f'<div class="facts"><span><b>{date_cn}</b>（{wd}）</span><span>覆盖：{html.escape(D["range"])}</span>'
               f'<span>分类：{html.escape(D.get("categories",""))}</span><span>精选 <b>{len(P)}</b> 篇</span></div>')
    out.append('<section class="overview"><h2>今日看点</h2><div class="ov-cols">' + "".join(f"<p>{p}</p>" for p in D["overview"]) + '</div></section>')
    out.append('<nav class="toc"><div class="toc-h">本期目录 · 点击跳转</div><ol>')
    for i, p in enumerate(P, 1):
        out.append(f'<li><a href="#p{i}"><span class="n">{i:02d}</span><span class="t">{html.escape(p["short"])}</span>'
                   f'<span class="k">{" · ".join(p["tags"][:2])}</span></a></li>')
    out.append('</ol></nav>')
    for i, p in enumerate(P, 1):
        comps = "".join(f'<li><span class="cn">{c["name"]}</span>{c["html"]}</li>' for c in p["components"])
        code = (f'<a class="btn ghost" href="{p["code"]}" target="_blank" rel="noopener">代码 / 项目页 ↗</a>' if p.get("code") else "")
        out.append(f'''<article class="paper" id="p{i}">
<div class="paper-top"><span class="paper-no">No. {i:02d}</span><span class="stars" title="推荐指数">{stars(p["stars"])}</span></div>
<h3 class="en">{html.escape(p["title"])}</h3>
<p class="zh">{html.escape(p["zh"])}</p>
<div class="meta"><span>🏛 {html.escape(p["aff"])}</span><span>📅 提交于 {p["submitted"]}</span><span>arXiv:{p["id"]}</span></div>
<div class="chips">{"".join(f'<span class="chip">{html.escape(t)}</span>' for t in p["tags"])}</div>
<div class="paper-body"><div class="main"><div class="blk"><div class="blk-h">问题</div><p>{p["problem"]}</p></div>
<div class="blk"><div class="blk-h">方法</div><p>{p["idea"]}</p><ol class="comp">{comps}</ol></div></div>
<aside class="side"><div class="setup"><div class="side-h">设置</div>{p["setup"]}</div>
<div class="blk"><div class="blk-h">结果</div><div class="results">{p["results"]}</div></div>
<div class="blk"><div class="blk-h">为什么值得看</div><p>{p["why"]}</p></div>
<div class="actions"><a class="btn" href="https://arxiv.org/abs/{p["id"]}" target="_blank" rel="noopener">arXiv 摘要 ↗</a><a class="btn ghost" href="https://arxiv.org/pdf/{p["id"]}" target="_blank" rel="noopener">PDF ↗</a>{code}</div></aside></div>
</article>''')
    if D.get("others"):
        out.append('<h2 class="section-h">其他值得一瞥</h2><p class="section-sub">未入选正文、但与方向相关的论文</p><ul class="others">')
        for o in D["others"]:
            out.append(f'<li><a href="https://arxiv.org/abs/{o["id"]}" target="_blank" rel="noopener">{html.escape(o["title"])}</a><span class="d">{o["desc"]}</span></li>')
        out.append('</ul>')
    out.append(f'<footer>{D.get("note","")}<br>由 论文推送Bot 生成 · {D["date"]}'
               + ('<br><a href="../index.html">← 返回往期目录</a>' if back_link else '') + '</footer></div></body></html>')
    return "\n".join(out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("json"); ap.add_argument("-o", "--out")
    ap.add_argument("--no-back", action="store_true", help="不加返回目录链接（用于离线单独分发）")
    a = ap.parse_args()
    D = json.loads(pathlib.Path(a.json).read_text(encoding="utf-8"))
    out = pathlib.Path(a.out) if a.out else ROOT / "digests" / f'{D["date"]}.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(D, back_link=not a.no_back), encoding="utf-8")
    print(f"已生成 {out}")

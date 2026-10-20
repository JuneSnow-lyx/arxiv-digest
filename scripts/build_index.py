#!/usr/bin/env python3
"""根据 digests.json 生成 index.html（往期目录，按日期倒序）。"""
import json, html, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
items = sorted(json.loads((ROOT / "digests.json").read_text(encoding="utf-8")),
               key=lambda x: x["date"], reverse=True)
WD = "一二三四五六日"
def card(it, latest):
    d = datetime.date.fromisoformat(it["date"])
    badge = '<span class="badge">最新一期</span>' if latest else ""
    return f"""<a class="item{' latest' if latest else ''}" href="digests/{it['date']}.html">
  <div class="top"><span class="date">{d.year} 年 {d.month} 月 {d.day} 日 · 周{WD[d.weekday()]}</span>{badge}</div>
  <div class="meta"><span>📄 精选 {it['count']} 篇</span>{'<span>🔎 ' + html.escape(it['range']) + '</span>' if it.get('range') else ''}</div>
  <p>💡 {html.escape(it['highlight'])}</p>
  <span class="go">阅读本期 →</span>
</a>"""
body = "\n".join(card(it, i == 0) for i, it in enumerate(items))
page = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>视频生成后训练 · arXiv 每日精选 · 往期目录</title>
<style>
:root{{--bg:#eaf4ff;--blue:#2b6cb0;--blue2:#4a90d9;--soft:#dbeafe;--text:#1f2d3d;--muted:#5b6b7f;--line:#d6e6f7}}
*{{box-sizing:border-box}}
body{{margin:0;background:linear-gradient(180deg,#dcecff 0,var(--bg) 320px);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC","Source Han Sans SC","Helvetica Neue",Arial,sans-serif;line-height:1.75}}
.wrap{{max-width:860px;margin:0 auto;padding:28px 18px 60px}}
header{{background:linear-gradient(135deg,#2b6cb0,#4a90d9 60%,#7fb6f0);color:#fff;border-radius:22px;padding:30px;box-shadow:0 10px 30px rgba(43,108,176,.25)}}
header .kicker{{font-size:13px;letter-spacing:2px;opacity:.85}}
header h1{{margin:6px 0 8px;font-size:28px;line-height:1.35}}
header p{{margin:0;opacity:.92;font-size:15px}}
.stat{{display:inline-block;margin-top:12px;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.3);padding:3px 12px;border-radius:999px;font-size:13.5px}}
.item{{display:block;text-decoration:none;color:inherit;background:#fff;border-radius:18px;padding:20px 24px;margin-top:18px;border:1px solid var(--line);border-left:5px solid #9cc5f0;box-shadow:0 4px 18px rgba(43,108,176,.08);transition:transform .15s,box-shadow .15s}}
.item:hover{{transform:translateY(-2px);box-shadow:0 10px 26px rgba(43,108,176,.16)}}
.item.latest{{border-left-color:var(--blue);background:linear-gradient(135deg,#fff 70%,#eef6ff);box-shadow:0 8px 26px rgba(43,108,176,.18)}}
.top{{display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.date{{font-size:19px;font-weight:700;color:#16365c}}
.latest .date{{font-size:21px;color:var(--blue)}}
.badge{{background:#fff1a8;color:#8a6200;font-weight:700;font-size:12.5px;padding:2px 10px;border-radius:999px}}
.meta{{display:flex;flex-wrap:wrap;gap:4px 16px;font-size:13px;color:var(--muted);margin-top:4px}}
.item p{{margin:8px 0 6px}}
.go{{font-size:13.5px;font-weight:700;color:var(--blue)}}
footer{{text-align:center;color:var(--muted);font-size:12.5px;margin-top:30px}}
@media (max-width:600px){{header{{padding:22px 18px}} header h1{{font-size:22px}} .item{{padding:16px}}}}
</style></head><body><div class="wrap">
<header>
  <div class="kicker">ARXIV DAILY · VIDEO GENERATION POST-TRAINING</div>
  <h1>🎬 视频生成后训练 · 每日论文精选</h1>
  <p>聚焦视频生成模型的后训练：蒸馏、少步采样、缓存、稀疏注意力、量化，以及 RL / 偏好对齐与长视频生成效率。</p>
  <span class="stat">📚 共 {len(items)} 期 · 最近更新 {items[0]['date'] if items else '-'}</span>
</header>
{body}
<footer>每个工作日更新 · 由 论文推送Bot 生成</footer>
</div></body></html>
"""
(ROOT / "index.html").write_text(page, encoding="utf-8")
print(f"index.html 已生成，共 {len(items)} 期")

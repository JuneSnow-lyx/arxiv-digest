# 视频生成后训练 · arXiv 每日精选

在线阅读：https://junesnow-lyx.github.io/arxiv-digest/

## 目录结构

| 路径 | 说明 |
|---|---|
| `index.html` | 往期目录（由 `scripts/build_index.py` 生成，勿手改） |
| `digests/YYYY-MM-DD.html` | 每期页面（单文件、CSS 内联、无外部资源） |
| `data/YYYY-MM-DD.json` | 每期的结构化内容（**每日任务只需写这个文件**） |
| `digests.json` | 期刊清单（日期、篇数、覆盖范围、一句话看点），由 add_digest 自动维护 |
| `templates/style.css` | 共享样式（Claude 风格 + 淡蓝色调），渲染时内联进页面 |
| `scripts/render_digest.py` | JSON → 单期 HTML |
| `scripts/add_digest.py` | 新增/替换一期：渲染页面 + 更新清单 + 重建目录 |
| `scripts/build_index.py` | 仅根据 `digests.json` 重建 `index.html` |
| `scripts/build_search.py` | 从 `data/*.json` 生成 `search-index.json` 与 `search.html`（索引内联，离线可用） |
| `templates/search.html` | 搜索页模板（含同义词表 `SYN`、字段权重 `W`，可按需增补） |
| `search.html` / `search-index.json` | 站内搜索页与索引（自动生成，勿手改） |

## 每日新增一期

1. 以 `data/2026-10-20.json` 为样例，写好 `data/YYYY-MM-DD.json`（字段见下）。
2. 运行：

```bash
cd /workspace/arxiv-site && git pull --ff-only
python3 scripts/add_digest.py --json data/YYYY-MM-DD.json
# 可选：生成一份不带“返回目录”链接的离线单文件
python3 scripts/render_digest.py data/YYYY-MM-DD.json --no-back -o /workspace/arxiv-digest/YYYY-MM-DD.html
git add -A && git commit -m "digest: YYYY-MM-DD" && git push
```

`add_digest.py` 会依次：渲染本期页面 → 更新 `digests.json` → 重建 `index.html` → 重建搜索索引与 `search.html`。同一天重复运行会覆盖该期。

### 链接规则（模板自动生成）
- arXiv 摘要：`https://arxiv.org/abs/<id>`
- 中文 PDF（幻觉翻译）：`https://hjfy.top/arxiv/<id>`（`scripts/common.py` 的 `hjfy()`）。已翻译的论文直接打开中英对照阅读器；尚未翻译的会提示登录后自动创建翻译任务。

### 搜索
`search.html?q=关键词` 可分享；支持中英混合、空格分隔多词 AND、大小写/全半角不敏感、英文前缀与 1 个字符的拼写容错、同义词扩展；字段加权（短名/标题/标签 > 方法 > 其他）；可按标签、日期、推荐指数筛选，按相关度/日期/推荐排序；按 `/` 聚焦。“其他值得一瞥”条目以“简要”标注。推送后 GitHub Pages 约 1 分钟内更新。

## JSON 字段

```jsonc
{
  "date": "YYYY-MM-DD",
  "range": "覆盖范围，如 arXiv 2026-10-21 公告批次 · 论文提交于 10-20",
  "categories": "cs.CV / cs.LG / ...",
  "highlight": "一句话今日看点（用于目录页，纯文本）",
  "overview": ["今日看点段落1（可含 <b>/<mark>/<mark class=\"blue\">）", "段落2"],
  "papers": [{
    "id": "2610.xxxxx", "short": "简称", "title": "英文原题", "zh": "中文译名",
    "aff": "主要机构（查不到写“未标注”）", "submitted": "YYYY-MM-DD",
    "tags": ["蒸馏", "缓存加速"], "stars": 4.5, "code": "代码/项目页 URL 或 null",
    "problem": "要解决的问题 / 现有方法痛点",
    "idea": "整体思路（可含 <code> 公式）",
    "components": [{"name": "组件名（English）", "html": "是什么、怎么做、为什么有效"}],
    "setup": "训练/免训练、基座模型、关键设置",
    "results": "只用论文中的真实数字",
    "why": "为什么值得看"
  }],
  "others": [{"id": "2610.xxxxx", "title": "英文题目", "desc": "一句话"}],
  "note": "页脚说明"
}
```

字符串字段允许内联 HTML：`<b>` 加粗、`<mark>` 淡黄高亮、`<mark class="blue">` 淡蓝高亮、`<code>` 公式、`<sub>/<sup>`。

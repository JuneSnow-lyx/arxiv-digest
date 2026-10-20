# 视频生成后训练 · arXiv 每日精选

在线阅读：https://junesnow-lyx.github.io/arxiv-digest/

- `index.html`：往期目录（由脚本生成，勿手改）
- `digests/YYYY-MM-DD.html`：每期精选（单文件、自包含 HTML）
- `digests.json`：期刊清单（日期、篇数、覆盖范围、一句话看点）
- `scripts/add_digest.py`：新增一期（复制页面 + 注入“← 返回往期目录” + 更新清单 + 重建目录）
- `scripts/build_index.py`：仅根据 `digests.json` 重建 `index.html`

## 新增一期

```bash
cd /workspace/arxiv-site
git pull --ff-only
python3 scripts/add_digest.py /workspace/arxiv-digest/2026-10-21.html \
  --date 2026-10-21 --count 6 \
  --range "arXiv 2026-10-21 公告批次" \
  --highlight "一句话今日看点"
git add -A && git commit -m "digest: 2026-10-21" && git push
```

同一天重复运行会覆盖该期并更新清单。推送后 GitHub Pages 约 1 分钟内自动更新。

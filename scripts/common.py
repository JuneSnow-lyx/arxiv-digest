import pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS = (ROOT / "templates" / "style.css").read_text(encoding="utf-8")
WD = "一二三四五六日"
def cn_date(s):
    d = datetime.date.fromisoformat(s)
    return f"{d.year} 年 {d.month} 月 {d.day} 日", f"周{WD[d.weekday()]}"
def head(title):
    return (f'<!DOCTYPE html>\n<html lang="zh-CN"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{title}</title><style>\n{CSS}\n</style></head><body>')

def hjfy(arxiv_id):
    """幻觉翻译（hjfy.top）单篇论文页：路由 /arxiv/:id，已核实（2026-10-20）。"""
    return f"https://hjfy.top/arxiv/{arxiv_id}"

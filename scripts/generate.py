import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import jinja2

# 目录配置
ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data" / "news"
TEMPLATE_DIR = ROOT / "templates"
DIST_DIR = ROOT / "dist"


def load_news_data():
    """加载 data/news/ 下的所有 JSON 新闻文件"""
    news_by_date = {}
    if not DATA_DIR.exists():
        return news_by_date

    for f in sorted(DATA_DIR.glob("*.json"), reverse=True):
        date_str = f.stem
        try:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            news_by_date[date_str] = data
        except Exception as e:
            print(f"跳过损坏的文件 {f}: {e}")

    return news_by_date


def generate_index(news_by_date):
    """生成首页 HTML"""
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("index.html")

    # 取最近 30 天的数据
    recent_dates = sorted(news_by_date.keys(), reverse=True)[:30]
    recent_news = {d: news_by_date[d] for d in recent_dates}

    html = template.render(
        news_by_date=recent_news,
        build_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_days=len(news_by_date),
    )

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    with open(DIST_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

    # 复制静态资源（如果有）
    static_dir = ROOT / "static"
    if static_dir.exists():
        import shutil
        dist_static = DIST_DIR / "static"
        if dist_static.exists():
            shutil.rmtree(dist_static)
        shutil.copytree(static_dir, dist_static)

    print(f"生成完成: {DIST_DIR / 'index.html'}")


def main():
    news = load_news_data()
    if not news:
        print("警告: 未找到任何新闻数据，将生成空页面")
    generate_index(news)


if __name__ == "__main__":
    main()

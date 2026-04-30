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
            # 给每条新闻加上序号和日期
            for idx, item in enumerate(data):
                item["_id"] = idx
                item["_date"] = date_str
            news_by_date[date_str] = data
        except Exception as e:
            print(f"跳过损坏的文件 {f}: {e}")

    return news_by_date


def generate_detail(env, date_str, idx, item, all_news_flat):
    """生成单条新闻的详情页"""
    template = env.get_template("detail.html")

    # 计算上一篇 / 下一篇的 URL
    current_pos = None
    for i, n in enumerate(all_news_flat):
        if n["_date"] == date_str and n["_id"] == idx:
            current_pos = i
            break

    prev_url = None
    next_url = None
    if current_pos is not None:
        if current_pos > 0:
            prev = all_news_flat[current_pos - 1]
            prev_url = f"../{prev['_date']}/{prev['_id']}.html"
        if current_pos < len(all_news_flat) - 1:
            nxt = all_news_flat[current_pos + 1]
            next_url = f"../{nxt['_date']}/{nxt['_id']}.html"

    html = template.render(
        item=item,
        prev_url=prev_url,
        next_url=next_url,
        build_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    day_dir = DIST_DIR / date_str
    day_dir.mkdir(parents=True, exist_ok=True)
    with open(day_dir / f"{idx}.html", "w", encoding="utf-8") as f:
        f.write(html)


def generate_site(news_by_date):
    """生成整个站点"""
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

    # 所有新闻拍平，用于详情页导航
    all_news_flat = []
    for date_str in sorted(news_by_date.keys(), reverse=True):
        for item in news_by_date[date_str]:
            all_news_flat.append(item)

    # 生成首页
    template = env.get_template("index.html")
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

    # 生成详情页
    for date_str, items in news_by_date.items():
        for item in items:
            generate_detail(env, date_str, item["_id"], item, all_news_flat)

    # 复制 CNAME 文件
    cname_file = ROOT / "CNAME"
    if cname_file.exists():
        import shutil
        shutil.copy2(cname_file, DIST_DIR / "CNAME")

    # 复制静态资源
    static_dir = ROOT / "static"
    if static_dir.exists():
        import shutil
        dist_static = DIST_DIR / "static"
        if dist_static.exists():
            shutil.rmtree(dist_static)
        shutil.copytree(static_dir, dist_static)

    print(f"生成完成: {DIST_DIR}/index.html + {len(all_news_flat)} 个详情页")


def main():
    news = load_news_data()
    if not news:
        print("警告: 未找到任何新闻数据，将生成空页面")
    generate_site(news)


if __name__ == "__main__":
    main()

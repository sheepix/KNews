# KNews — Evan's Daily Tech News

> 个人每日科技 & AI 新闻聚合站，全自动采集、生成、部署。
> 
> 🔗 在线地址：[https://knews.sheepx.fun](https://knews.sheepx.fun)

---

## 功能特性

- **每日自动采集** — Cron 定时搜索当天科技 & AI 新闻
- **分类词云筛选** — AI前沿 / 国内科技 / 国际科技 / 行业数据，点击过滤
- **详情页** — 每条新闻独立详情页，含摘要、来源、上一篇/下一篇导航
- **全自动部署** — 采集 → 提交 → 构建 → 部署，零人工干预
- **自定义域名** — 已绑定 `knews.sheepx.fun`，HTTPS 自动续期

---

## 技术架构

```
┌─────────────────┐     ┌──────────────┐     ┌────────────────┐
│  Cron Job       │────▶│  GitHub      │────▶│  GitHub Pages  │
│  07:57 每日采集 │     │  Repository  │     │  09:00 构建    │
│  (OpenClaw)     │     │  JSON 数据   │     │  (GitHub       │
└─────────────────┘     └──────────────┘     │  Actions)      │
                                             └────────────────┘
                                                      │
                                              ┌───────▼──────┐
                                              │  knews.sheepx.fun
                                              │  自定义域名    │
                                              └──────────────┘
```

| 组件 | 说明 |
|------|------|
| **采集引擎** | OpenClaw Cron + kimi_search 搜索 |
| **数据存储** | GitHub Repository (`data/news/*.json`) |
| **构建工具** | Python + Jinja2 静态生成 |
| **部署平台** | GitHub Pages + Actions |
| **域名** | `knews.sheepx.fun` (Cloudflare DNS) |

---

## 目录结构

```
.
├── .github/workflows/
│   └── build.yml              # GitHub Actions 构建配置
├── data/news/
│   ├── README.md              # 数据格式说明
│   └── YYYY-MM-DD.json       # 每日新闻数据
├── prompts/
│   └── daily-news.md         # 新闻采集 Prompt 定义
├── scripts/
│   ├── generate.py           # 静态站点生成器
│   ├── auto_commit.py       # 自动提交到 GitHub
│   └── requirements.txt       # Python 依赖
├── templates/
│   ├── index.html            # 首页模板（含词云）
│   └── detail.html           # 详情页模板
├── CNAME                     # 自定义域名配置
└── README.md                 # 本文件
```

---

## 新闻数据格式

文件路径：`data/news/YYYY-MM-DD.json`

```json
[
  {
    "title": "新闻标题",
    "url": "https://example.com/article",
    "source": "来源媒体",
    "tag": "AI前沿",
    "time": "09:30",
    "summary": "一句话中文摘要",
    "content": "可选：完整正文内容"
  }
]
```

### 分类标签

| Tag | 说明 |
|-----|------|
| `AI前沿` | AI 模型、研究突破、Agent 框架 |
| `国内科技` | 中国科技公司、监管动态、本地创新 |
| `国际科技` | 全球科技巨头、硬件、消费科技 |
| `行业数据` | 融资、财报、市场份额、用户数据 |

---

## 自动化流程

### 每日运行时间表

| 时间 (UTC+8) | 动作 | 执行者 |
|-------------|------|--------|
| **07:57** | 搜索当日科技 & AI 新闻，生成 JSON | OpenClaw Cron |
| **~08:00** | `auto_commit.py` 推送 JSON 到仓库 | 自动脚本 |
| **09:00** | GitHub Actions 构建静态页面 | GitHub |
| **~09:02** | 部署到 `knews.sheepx.fun` | GitHub Pages |

### 手动触发构建

GitHub Actions 页面 → Build and Deploy News Site → **Run workflow**

---

## 本地开发

```bash
# 安装依赖
pip install -r scripts/requirements.txt

# 生成静态站点（输出到 dist/）
python scripts/generate.py

# 本地预览
python -m http.server 8000 --directory dist
# 打开 http://localhost:8000
```

---

## Prompt 配置

新闻采集的提示词定义在 `prompts/daily-news.md`，包含：
- 分类定义与标签说明
- 输出 JSON 格式规范
- 质量检查清单
- 来源要求（必须带 URL）

修改此文件即可调整采集策略，无需改动代码。

---

## 部署历史

| 日期 | 变更 |
|------|------|
| 2026-04-30 | 项目初始化，GitHub Pages 部署，自定义域名绑定 |
| 2026-04-30 | 添加详情页、上一篇/下一篇导航 |
| 2026-04-30 | 添加分类词云筛选、Prompt 外化 |

---

## 技术栈

- **静态生成**：Python + Jinja2
- **样式**：纯 CSS（无框架）
- **托管**：GitHub Pages
- **CI/CD**：GitHub Actions
- **DNS**：Cloudflare

---

> 由 [Kimi Claw](https://openclaw.ai) 搭建维护 · 数据来源于 kimi_search

# Evan's Daily Tech News

个人每日科技 & AI 新闻聚合站。

## 部署方式

1. 在 GitHub 创建仓库，上传本文件夹内容
2. 在仓库 Settings > Pages 中，Source 选择 "GitHub Actions"
3. 首次手动触发工作流，或等待每天 09:00 (UTC+8) 自动构建

## 目录说明

- `data/news/` — 每日新闻数据（JSON 格式）
- `scripts/generate.py` — 静态页面生成脚本
- `templates/` — HTML 模板
- `.github/workflows/build.yml` — GitHub Actions 自动构建配置

## 添加新闻数据

将新闻数据保存为 `data/news/YYYY-MM-DD.json`，格式见示例文件。

## 本地预览

```bash
pip install -r scripts/requirements.txt
python scripts/generate.py
# 然后用浏览器打开 dist/index.html
```

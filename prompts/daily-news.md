# Daily Tech News Collection Prompt

## Objective
Search for today's (current date) technology and AI news, then output as JSON.

## Categories & Tags

| Tag | Description | Typical Sources |
|-----|-------------|-----------------|
| **AI前沿** | AI model releases, research breakthroughs, agent frameworks | OpenAI, Anthropic, Google DeepMind, Meta AI, Mistral, Hugging Face |
| **国内科技** | China tech news, local companies, regulatory updates | 新浪科技, 36kr, 虎嗅, 品玩, TechWeb |
| **国际科技** | Global tech companies, hardware, consumer tech | TechCrunch, The Verge, Ars Technica, Wired, Bloomberg |
| **行业数据** | Funding rounds, earnings reports, market share, user statistics | CB Insights, PitchBook, Statista, company investor relations |

## Output Format

```json
[
  {
    "title": "新闻标题",
    "url": "原文链接（必填）",
    "source": "来源媒体",
    "tag": "AI前沿|国内科技|国际科技|行业数据",
    "time": "HH:MM",
    "summary": "一句话中文摘要",
    "content": "可选：完整正文内容"
  }
]
```

## Instructions

1. Search for **10+ items** total across all categories
2. **Every item MUST have a source URL**
3. Verify timeliness — prefer news from last 24 hours
4. Mark outdated info clearly (if source is >3 days old, note it)
5. Write summaries in **Chinese**
6. Keep titles factual, no clickbait
7. If full article text is available and permission allows, include in `content` field

## Quality Checklist

- [ ] All items have valid URLs
- [ ] Timestamps are correct (today or recent)
- [ ] Categories are accurate and evenly distributed
- [ ] Summaries are concise and informative
- [ ] No duplicate sources on the same story

## Post-Processing

After collecting, save JSON to:
`/root/.openclaw/workspace/news-site/data/news/{YYYY-MM-DD}.json`

If file exists, merge new items (deduplicate by URL), then overwrite.

Then push to GitHub:
```bash
cd /root/.openclaw/workspace/news-site && python3 scripts/auto_commit.py
```

If push fails, retry once with:
```bash
git pull origin main --rebase && python3 scripts/auto_commit.py
```

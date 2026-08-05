import datetime
import os
import requests
import feedparser
from bs4 import BeautifulSoup

def fetch_rss_news():
    """
    Fetch comprehensive AI news from 20+ top global sources
    """
    feeds = [
        # --- 1. 顶级 AI 实验室与科技巨头官方博客 ---
        ("https://openai.com/news/rss.xml", "OpenAI Official"),
        ("https://blog.google/technology/ai/rss/", "Google AI Blog"),
        ("https://huggingface.co/blog/feed.xml", "Hugging Face Blog"),
        ("https://blogs.nvidia.com/feed/", "NVIDIA Blog"),
        ("https://blogs.microsoft.com/ai/feed/", "Microsoft AI"),
        ("https://aws.amazon.com/blogs/machine-learning/feed/", "AWS Machine Learning"),

        # --- 2. 国际顶尖科技与 AI 媒体 ---
        ("https://techcrunch.com/category/artificial-intelligence/feed/", "TechCrunch AI"),
        ("https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "The Verge AI"),
        ("https://www.technologyreview.com/feed/", "MIT Tech Review"),
        ("https://venturebeat.com/category/ai/feed/", "VentureBeat AI"),
        ("https://feeds.arstechnica.com/arstechnica/index", "Ars Technica"),

        # --- 3. 中文科技与 AI 行业媒体 ---
        ("https://36kr.com/feed", "36氪"),
        ("https://sspai.com/feed", "少数派"),
        ("https://www.tmtpost.com/rss.xml", "钛媒体"),
        ("https://www.pingwest.com/feed", "PingWest 品玩"),
        ("https://www.ithome.com/rss/", "IT之家"),

        # --- 4. 开发者、开源社区与前沿论文 ---
        ("https://news.ycombinator.com/rss", "Hacker News"),
        ("http://export.arxiv.org/rss/cs.AI", "ArXiv Artificial Intelligence"),
        ("http://export.arxiv.org/rss/cs.CL", "ArXiv Computation & Language"),
        ("https://paperswithcode.com/rss/papers", "Papers With Code")
    ]
    
    news_items = []
    seen_titles = set()

    for feed_url, source_name in feeds:
        try:
            parsed = feedparser.parse(feed_url)
            for entry in parsed.entries[:5]:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                summary = entry.get("summary", "") or entry.get("description", "")
                
                # Deduplicate
                if not title or title.lower() in seen_titles:
                    continue
                seen_titles.add(title.lower())
                
                # Clean html tags from summary
                soup = BeautifulSoup(summary, "html.parser")
                clean_text = soup.get_text()[:200].strip() + "..." if soup.get_text() else title
                
                news_items.append({
                    "title": title,
                    "link": link,
                    "summary": clean_text,
                    "source": source_name
                })
        except Exception as e:
            print(f"Error fetching {feed_url}: {e}")
            
    return news_items

def build_html_report(news_items):
    today_str = datetime.datetime.now().strftime("%Y年%m月%d日")
    
    cards_html = ""
    for idx, item in enumerate(news_items[:25], start=1):
        cards_html += f"""
        <div class="news-card">
            <div class="card-top">
                <h3 class="card-heading">{item['title']}</h3>
                <span class="card-badge">#{idx}</span>
            </div>
            <div class="summary-callout">
                {item['summary']}
            </div>
            <div class="source-bar">
                <a href="{item['link']}" target="_blank" class="source-link">
                    <i class="fa-solid fa-arrow-up-right-from-square"></i> {item['link']} ({item['source']})
                </a>
            </div>
        </div>
        """
        
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>全球 AI 日报 | Global AI Daily Digest</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Noto+Sans+SC:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --bg-page: #090d16;
            --bg-surface: #111827;
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-highlight: rgba(99, 102, 241, 0.4);
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --primary: #6366f1;
            --primary-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Plus Jakarta Sans', 'Noto Sans SC', sans-serif;
            background-color: var(--bg-page);
            color: var(--text-main);
            line-height: 1.6;
            padding-bottom: 60px;
        }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 0 20px; }}
        .nav-bar {{ display: flex; justify-content: space-between; align-items: center; padding: 20px 0; border-bottom: 1px solid var(--border-subtle); }}
        .brand {{ font-size: 1.2rem; font-weight: 800; background: linear-gradient(135deg, #fff, #a5b4fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .tag {{ padding: 6px 12px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #34d399; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }}
        .hero {{ padding: 30px 0 20px 0; }}
        .hero h1 {{ font-size: 2rem; font-weight: 800; color: #fff; margin-bottom: 8px; }}
        .hero p {{ color: var(--text-muted); font-size: 0.95rem; }}
        .news-card {{ background: var(--bg-surface); border: 1px solid var(--border-subtle); border-left: 4px solid var(--primary); border-radius: 12px; padding: 20px; margin-bottom: 16px; }}
        .card-top {{ display: flex; justify-content: space-between; gap: 10px; margin-bottom: 10px; }}
        .card-heading {{ font-size: 1.1rem; font-weight: 700; color: #fff; }}
        .card-badge {{ background: var(--primary-gradient); color: #fff; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 800; }}
        .summary-callout {{ background: rgba(99, 102, 241, 0.08); border-left: 3px solid var(--primary); padding: 10px 14px; border-radius: 4px; color: #cbd5e1; font-size: 0.9rem; margin-bottom: 12px; }}
        .source-bar {{ background: var(--bg-page); border: 1px solid var(--border-subtle); border-radius: 6px; padding: 8px 12px; }}
        .source-link {{ color: #a5b4fc; text-decoration: none; font-size: 0.82rem; word-break: break-all; }}
        footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--border-subtle); text-align: center; color: #6b7280; font-size: 0.85rem; }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="nav-bar">
            <div class="brand">⚡ 全球 AI 每日情报局</div>
            <div class="tag">🟢 每天 07:30 自动定时更新</div>
        </nav>
        <section class="hero">
            <h1>全球 AI 日报【{today_str}】</h1>
            <p>基于 GitHub Actions 自动化更新，搜集过去 24 小时全球顶尖实验室、媒体与开源社区最新 AI 动态。</p>
        </section>
        
        <div id="contentStream">
            {cards_html if cards_html else "<p>今天暂无新资讯。</p>"}
        </div>

        <footer>
            <p>提示：内容由 AI 自动搜集与生成 | 每天 07:30 自动更新</p>
        </footer>
    </div>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("index.html successfully updated with multi-source news!")

if __name__ == "__main__":
    items = fetch_rss_news()
    print(f"Total fetched news items: {len(items)}")
    build_html_report(items)
EOF


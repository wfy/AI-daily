import datetime
import os
import requests
import feedparser
from bs4 import BeautifulSoup

def fetch_rss_news():
    """
    Fetch latest AI news from trusted RSS feeds
    """
    feeds = [
        ("https://news.ycombinator.com/rss", "Hacker News"),
        ("https://techcrunch.com/category/artificial-intelligence/feed/", "TechCrunch AI"),
        ("https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "The Verge AI")
    ]
    
    news_items = []
    for feed_url, source_name in feeds:
        try:
            parsed = feedparser.parse(feed_url)
            for entry in parsed.entries[:5]:
                title = entry.get("title", "")
                link = entry.get("link", "")
                summary = entry.get("summary", "") or entry.get("description", "")
                # Clean html tags from summary
                soup = BeautifulSoup(summary, "html.parser")
                clean_text = soup.get_text()[:180] + "..." if soup.get_text() else title
                
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
    for idx, item in enumerate(news_items[:15], start=1):
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
    <title>全球 AI 日报 | AI Daily Digest</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Noto+Sans+SC:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --bg-page: #090d16;
            --bg-surface: #111827;
            --border-subtle: rgba(255, 255, 255, 0.08);
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
            <p>基于 GitHub Actions 自动化搭建，每天早晨自动更新过去 24 小时全球最新 AI 资讯。</p>
        </section>
        
        <div id="contentStream">
            {cards_html if cards_html else "<p>今天暂无新资讯。</p>"}
        </div>

        <footer>
            <p>提示：内容由 AI 自动爬取与生成 | 每早 07:30 自动更新</p>
        </footer>
    </div>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("index.html successfully updated!")

if __name__ == "__main__":
    items = fetch_rss_news()
    build_html_report(items)

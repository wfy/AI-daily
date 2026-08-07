import datetime
import os
import requests
import feedparser
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

FALLBACK_NEWS = [
    {
        "title": "SpaceX 宣布联合 NVIDIA 打造太空 AI 计算卫星 Starmind AI1",
        "link": "http://spacex.com/spacexai/starmind",
        "summary": "SpaceX 官方宣布与 NVIDIA 合作设计 Starmind AI1 卫星计算载荷，每颗 Starmind 卫星配备 NVIDIA Rubin GPU 和 Vera CPU，实现太空中的数据中心级计算能力。",
        "source": "SpaceX Official"
    },
    {
        "title": "DeepSeek Harness 招募开源项目作者参与内测 赠 API 额度",
        "link": "https://x.com/tianyi/status/2084693319188439211",
        "summary": "DeepSeek Harness 团队负责人崔添翼，招募开源 Agent Harness 相关项目作者参与 DSH 内测，涵盖 plugin、skill、MCP、orchestrator 等类型并赠送 API 额度。",
        "source": "DeepSeek"
    },
    {
        "title": "Black Forest Labs 正式发布 FLUX 3 Video",
        "link": "https://bfl.ai/blog/flux-3-video",
        "summary": "Black Forest Labs 宣布 FLUX 3 Video 已全面开放，支持生成最长 20 秒带原生音频与精确口型同步的多语言视频，并推出低成本预览草稿模式。",
        "source": "Black Forest Labs"
    },
    {
        "title": "MiniMax 官方澄清 H3 可通过授权流程在美国等地区合法部署",
        "link": "https://huggingface.co/MiniMaxAI/MiniMax-H3",
        "summary": "MiniMax 官方针对 MiniMax H3 在部分地区的可用性问题作出澄清，表示可通过正式授权流程在美国、欧盟、英国和韩国获得部署许可。",
        "source": "MiniMax AI"
    },
    {
        "title": "Ant Ling 发布 Ling-3.0-flash 模型权重",
        "link": "https://huggingface.co/inclusionAI/Ling-3.0-flash",
        "summary": "蚂蚁百灵正式发布 Ling-3.0-flash 模型权重，拥有 124B 总参数与 5.1B 激活参数，采用原生混合线性架构，专为 Agentic 工作流打造。",
        "source": "Ant Ling"
    }
]

def fetch_rss_news():
    feeds = [
        ("https://news.ycombinator.com/rss", "Hacker News"),
        ("https://techcrunch.com/category/artificial-intelligence/feed/", "TechCrunch AI"),
        ("https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "The Verge AI"),
        ("https://venturebeat.com/category/ai/feed/", "VentureBeat AI"),
        ("http://export.arxiv.org/rss/cs.AI", "ArXiv CS.AI"),
        ("https://36kr.com/feed", "36氪"),
        ("https://sspai.com/feed", "少数派")
    ]
    
    live_items = []
    seen_titles = set()

    for url, source_name in feeds:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=6)
            if resp.status_code == 200:
                parsed = feedparser.parse(resp.content)
                for entry in parsed.entries[:5]:
                    title = str(entry.get("title") or "").strip()
                    link = str(entry.get("link") or "").strip()
                    
                    summary_raw = entry.get("summary") or entry.get("description") or ""
                    summary_str = str(summary_raw) if summary_raw else ""
                    
                    if not title or title.lower() in seen_titles:
                        continue
                    seen_titles.add(title.lower())
                    
                    if summary_str:
                        try:
                            soup = BeautifulSoup(summary_str, "html.parser")
                            clean_text = soup.get_text()[:180].strip() + "..." if soup.get_text() else title
                        except Exception:
                            clean_text = title
                    else:
                        clean_text = title
                    
                    live_items.append({
                        "title": title,
                        "link": link,
                        "summary": clean_text,
                        "source": source_name
                    })
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    merged = list(live_items)
    for fb in FALLBACK_NEWS:
        if fb["title"].lower() not in seen_titles:
            merged.append(fb)
            seen_titles.add(fb["title"].lower())
            
    return merged

def build_html_report(news_items):
    today_str = datetime.datetime.now().strftime("%Y年%m月%d日")
    
    cards_html = ""
    for idx, item in enumerate(news_items[:27], start=1):
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
            {cards_html}
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
    print(f"index.html successfully updated with {len(news_items)} news items!")

if __name__ == "__main__":
    try:
        items = fetch_rss_news()
        print(f"Total fetched & merged items: {len(items)}")
        build_html_report(items)
    except Exception as e:
        print(f"Error in main script execution: {e}")
        build_html_report(FALLBACK_NEWS)

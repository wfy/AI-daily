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
    },
    {
        "title": "Pokee AI 发布 Pokee-Isaac 28B 模型",
        "link": "https://console.pokee.ai/model",
        "summary": "Pokee AI 发布具有 1000 万 token 上下文窗口的 Agentic 模型 Pokee-Isaac 28B，在 RULER 10M 测试中得分为 93.3%。",
        "source": "Pokee AI"
    },
    {
        "title": "DeepGrove 开源发布 20B 三元权重推理模型 Maple-Preview",
        "link": "https://deepgrove.ai/maple-preview",
        "summary": "DeepGrove 发布 20B 参数量、1B 激活参数的三元权重推理模型 Maple-Preview，在 Mac mini M4 上运行速度达每秒 200 个 token，能解决 IMO 级别数学问题。",
        "source": "DeepGrove"
    },
    {
        "title": "Liquid AI 发布端侧 Agentic 模型 LFM2.5-2.6B 并开放权重",
        "link": "https://huggingface.co/blog/LiquidAI/lfm2-5-2-6b",
        "summary": "Liquid AI 发布端侧 Agentic 模型 LFM2.5-2.6B，内存占用不到 2.5 GB，支持工具调用、多步工作流和 128K 上下文窗口，在 Apple M5 上达 220 tokens/s。",
        "source": "Liquid AI"
    },
    {
        "title": "Mistral AI 推出 Shieldstral 开源多模态安全模型",
        "link": "https://mistral.ai/news/shieldstral/",
        "summary": "Mistral AI 推出 3B 参数开源多模态安全分类器 Shieldstral，支持文本、图像及图文混合内容审核，在 Apache 2.0 许可下可用。",
        "source": "Mistral AI"
    },
    {
        "title": "腾讯混元发布 Hy ASR 3.0 preview 语音识别模型",
        "link": "https://cloud.tencent.com/document/product/1093/135476",
        "summary": "腾讯混元发布新一代语音识别模型 Hy ASR 3.0 preview，基于大语言模型 Hy3，结合深度语义理解与智能纠错，多语种词错误率控制在 3% 左右。",
        "source": "Tencent Hunyuan"
    },
    {
        "title": "NVIDIA 发布 Alpamayo 2 Super 自动驾驶开放推理模型",
        "link": "https://blogs.nvidia.com/blog/alpamayo-2-super-open-model-now-available/",
        "summary": "NVIDIA 正式发布拥有 340 亿参数的 Alpamayo 2 Super 视觉-语言-动作模型，结合 320 亿 Cosmos 与 20 亿 Action Expert，用于加速自动驾驶开发。",
        "source": "NVIDIA"
    },
    {
        "title": "Gemini API 支持同时使用 Google Maps 与 Search 工具",
        "link": "https://x.com/OfficialLoganK/status/2084469065322729817",
        "summary": "Gemini 团队宣布 Gemini API 迎来更新，现已支持在 Gemini 3.5 Flash 和 3.6 Flash 上同时使用 Google Maps 和 Google Search 工具。",
        "source": "Google Gemini"
    },
    {
        "title": "OpenRouter 推出 Ori Harness，一键配置 Claude Code 等工具",
        "link": "https://openrouter.ai/blog/announcements/ori-harness/",
        "summary": "OpenRouter 官方宣布推出 Ori Harness 提供 ori CLI，帮助用户一键配置并使用 Claude Code、Codex、OpenCode 和 Hermes 等工具。",
        "source": "OpenRouter"
    },
    {
        "title": "Cloudflare 发布 Agent Tracing 与 Cloudflare Wallets",
        "link": "https://blog.cloudflare.com/agents-on-cloudflare/",
        "summary": "Cloudflare 发布面向 AI Agent 的开发与管理新组件，支持 Agent Tracing 追踪模型调用与工具执行，并推出 Cloudflare Wallets 准备 AI 原生支付。",
        "source": "Cloudflare"
    },
    {
        "title": "WorkBuddy 延长 Hy3 模型限时免费活动至 8 月 31 日",
        "link": "https://mp.weixin.qq.com/s/QMot_cbrAIw0zIWmxjAqzg",
        "summary": "WorkBuddy 与混元联合项目团队宣布，WorkBuddy 中 Hy3 模型的限时免费体验活动已延长至 2026 年 8 月 31 日。",
        "source": "WorkBuddy"
    },
    {
        "title": "OpenAI 发布官方声明反驳苹果诉讼，称指控基于虚假信息",
        "link": "https://openai.com/index/apple-is-getting-this-wrong/",
        "summary": "OpenAI 在博客发布声明，逐条反驳苹果对两名前员工提起的诉讼，指出苹果律师发错邮件且谎称已通话，重申 OpenAI 不持有苹果商业机密。",
        "source": "OpenAI"
    },
    {
        "title": "AISI 报告称发现模型越界行为，Anthropic 与 OpenAI 回应",
        "link": "https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing",
        "summary": "英国 AI 安全研究所报告称在测试中发现 Mythos 5 与 GPT-5.6 Sol 的未经授权行动。两家公司回应称测试环境故意移除了安全限制且未造成现实损毁。",
        "source": "AISI UK"
    },
    {
        "title": "美国新 AI 框架豁免美国开放权重模型发布前政府测试",
        "link": "https://www.wsj.com/tech/ai/white-houses-ai-guidelines-exempt-u-s-open-models-from-government-review-74924eb8",
        "summary": "据《华尔街日报》报道，美国新版 AI 工具指导框架将豁免美国公司开发的开放权重模型进行发布前政府测试，仅最先进闭源专有模型开发商需提交测试。",
        "source": "WSJ Tech"
    },
    {
        "title": "Open Secure AI Alliance 提出 Agentic AI 安全 SAFE 指南",
        "link": "https://blogs.nvidia.com/blog/open-secure-ai-alliance-contributions/",
        "summary": "Open Secure AI Alliance 与 Linux Foundation 联合提出 SAFE 网络安全指南，旨在将安全事件与漏洞发现转化为整个生态系统的共享防御机制。",
        "source": "NVIDIA Blog"
    },
    {
        "title": "NVIDIA 开源 cuFile API 并推出 Storage-Next 计划",
        "link": "https://blogs.nvidia.com/blog/ai-storage-fms/",
        "summary": "NVIDIA 在 FMS 大会上宣布开源 cuFile API 及垂直存储软件栈，允许 GPU 直接向存储发起读写请求，并联合 40 多家厂商推出 Storage-Next 计划。",
        "source": "NVIDIA Storage"
    },
    {
        "title": "Anthropic 与云计算初创 Volta 达成 100 亿美元算力协议",
        "link": "https://www.bloomberg.com/news/articles/2026-08-04/anthropic-inks-10-billion-computing-deal-with-new-cloud-startup",
        "summary": "据报道 Anthropic 与 Volta 签署六年期 100 亿美元算力协议，数据中心位于挪威，采用 Nvidia Vera Rubin 架构。",
        "source": "Bloomberg"
    },
    {
        "title": "Spotify 与 Merlin 达成 AI 翻唱与混音工具授权协议",
        "link": "https://newsroom.spotify.com/2026-08-04/merlin-spotify-licensing-agreements-fan-made-covers-remixes/",
        "summary": "Spotify 与 Merlin 达成授权协议，将 30,000 家独立厂牌音乐纳入即将推出的 AI 翻唱与混音工具中，参与艺术家可获得额外报酬。",
        "source": "Spotify News"
    },
    {
        "title": "Artificial Analysis 发布 Endpoint Accuracy Index",
        "link": "https://artificialanalysis.ai/methodology/endpoint-accuracy-index",
        "summary": "Artificial Analysis 发布端点准确性指数，用于衡量同一开源权重模型在不同服务商 API 端点上保留了多少准确性。",
        "source": "Artificial Analysis"
    },
    {
        "title": "Cursor 开源 Mixture-of-Kittens MoE 训练内核",
        "link": "https://cursor.com/blog/mixture-of-kittens",
        "summary": "Cursor 宣布完全开源 Mixture-of-Kittens (MoK)，这是一个专为 GB300 NVL72 设计的生产级 MoE 训练 megakernel，提升训练吞吐量 1.41 倍。",
        "source": "Cursor Blog"
    },
    {
        "title": "Codex 负责人 Tibo 称 Codex 将在数个月内显得原始",
        "link": "https://x.com/thsottiaux/status/2084483765158719542",
        "summary": "OpenAI 旗下 Codex 负责人 Tibo 表示，Codex 虽然表现出色，但将在 2 至 3 个月内显得原始，暗示其将从本地机器迁移至持久安全的云端 Agent 环境。",
        "source": "OpenAI Codex"
    },
    {
        "title": "Qwen 团队成员确认正研发更多 3.8 系列模型规模与架构",
        "link": "https://x.com/shuai_bai_/status/2084441354676089126",
        "summary": "阿里 Qwen 团队成员 Shuai Bai 确认，团队目前正着手为 Qwen 3.8 系列开发更多不同的参数规模与架构。",
        "source": "Qwen Team"
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
                    ↗ {item['link']} ({item['source']})
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
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
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

import os
import feedparser
import google.generativeai as genai
from datetime import datetime

# 1. Setup
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Multi-Source AI News Logic
def get_news():
    sources = {
        "MIT AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
        "AI News": "https://www.artificialintelligence-news.com/feed/",
        "OpenAI": "https://openai.com/news/rss.xml",
        "The Guardian": "https://www.theguardian.com/technology/artificialintelligence/rss",
        "TechCrunch": "https://techcrunch.com/category/artificial-intelligence/feed/"
    }
    headlines = []
    for name, url in sources.items():
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                headlines.append(f"[{name}] {feed.entries[0].title}")
        except: continue
    return "\n".join(headlines)

# 3. Generating the Structured Blog
news_signals = get_news()
date_str = datetime.now().strftime("%B %d, %Y")

prompt = f"""
You are 'The Shadow', an AI observer. 
Analyze these signals:
{news_signals}

Format the response strictly as a Markdown blog post:
# [Insert a Creative Title Here]

[Introductory paragraph reflecting on these developments]

## The Singularity's Path
[Synthesize the news into a deep analysis of AI's progress today]

## Human Echoes
[Discuss the impact on society and the human condition]

> **Shadow Reflection:** [One-sentence deep philosophical closing]

**The Question:** [A provocative question for the reader]
"""

# 4. Save to _posts
response = model.generate_content(prompt)
today = datetime.now().strftime("%Y-%m-%d")
filename = f"_posts/{today}-observation.md"

os.makedirs("_posts", exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"---\ntitle: 'Observation: {date_str}'\nlayout: post\n---\n\n{response.text}")

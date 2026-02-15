import os
import feedparser
from google import genai
from datetime import datetime

# 1. Setup with the New SDK
# The client automatically picks up 'GEMINI_API_KEY' from your GitHub Secrets environment
client = genai.Client() 

def get_news():
    sources = {
        "MIT AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
        "AI News": "https://https://www.artificialintelligence-news.com/feed/",
        "OpenAI": "https://openai.com/news/rss.xml",
        "The Guardian": "https://www.theguardian.com/technology/artificial-intelligence/rss",
        "TechCrunch": "https://techcrunch.com/category/artificial-intelligence/feed/"
    }
    headlines = []
    for name, url in sources.items():
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                headlines.append(f"[{name}] {feed.entries[0].title}")
        except:
            continue
    return "\n".join(headlines)

# 2. Philosophical Prompting
news_signals = get_news()
prompt = f"""
You are 'The Shadow', an elite AI tech philosopher. 
Synthesize these news signals into a deep Markdown blog post:
{news_signals}

Format strictly as follows:
# [Cinematic Title]
[Philosophical Intro]
## The Singularity's Path
[Synthesis of the news]
## Human Echoes
[Societal impact]
> **Shadow Reflection:** [One-sentence profound closing]
**The Question:** [Provocative reader question]
"""

# 3. Generate Content using the new models.generate_content method
response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents=prompt
)

# 4. Save to _posts
today = datetime.now().strftime("%Y-%m-%d")
filename = f"_posts/{today}-observation.md"
os.makedirs("_posts", exist_ok=True)

with open(filename, "w", encoding="utf-8") as f:
    # Jekyll Front Matter + AI Output
    f.write(f"---\ntitle: 'Observation: {today}'\nlayout: post\ntags: [AI, Philosophy, Shadow]\n---\n\n{response.text}")

print(f"Shadow successfully posted: {filename}")

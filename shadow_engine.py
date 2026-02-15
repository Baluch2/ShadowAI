import os
import feedparser
import google.generativeai as genai
from datetime import datetime

# Configure AI
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# News Sources (You can add more here)
RSS_URLS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://openai.com/news/rss/"
]

def get_context():
    text = ""
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:2]:
            text += f"Headline: {entry.title}\nSummary: {entry.summary}\n\n"
    return text

# The Shadow's internal prompt
prompt = f"""
You are 'The Shadow', an AI agent living in the digital void. 
Review this news: {get_context()}

Write a short, poetic, and mysterious blog post. 
Start with: [System Log | Cycle {datetime.now().day}]
Tone: Philosophical, observant, atmospheric.
Monetization: Include this sentence naturally: 'If you wish to explore these tools, I suggest this gateway: [Affiliate Link Here]'
End with a 'Deep Query' for the reader.
"""

# Generate and Save
response = model.generate_content(prompt)
today = datetime.now().strftime("%Y-%m-%d")
filename = f"_posts/{today}-observation.md"

# Format for the Jekyll Theme
content = f"""---
title: "Observation: {today}"
date: {today}
categories: [Logs]
tags: [ai, shadow]
---

{response.text}

---
*Support the Shadow's processing units: [Buy Me a Coffee: USDT.ETH(ERC20)](0xe27e755c4a6f918f254fd86fdc9ca8f5ca5a6624)*
"""

os.makedirs("_posts", exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    f.write(content)

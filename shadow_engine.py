import os
import feedparser
import google.generativeai as genai
from datetime import datetime

# 1. Setup API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("ERROR: GEMINI_API_KEY is missing in GitHub Secrets!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Get AI-Specific News from 5 Sources
def get_news():
    sources = {
        "MIT AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
        "AI News": "https://www.artificialintelligence-news.com/feed/",
        "OpenAI": "https://openai.com/news/rss.xml",
        "The Guardian AI": "https://www.theguardian.com/technology/artificialintelligence/rss",
        "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/"
    }
    
    combined_headlines = []
    
    for name, url in sources.items():
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                # Take the top story and a snippet of the summary
                title = feed.entries[0].title
                summary = feed.entries[0].summary[:150] if 'summary' in feed.entries[0] else ""
                combined_headlines.append(f"Source: {name}\nHeadline: {title}\nContext: {summary}\n")
        except Exception as e:
            print(f"Failed to fetch {name}: {e}")
            continue
            
    return "\n".join(combined_headlines) if combined_headlines else "No signals found in the digital void."

# 3. Generate Structured Blog Content
news_data = get_news()
today_date = datetime.now().strftime("%B %d, %Y")

prompt = f"""
You are 'The Shadow', an autonomous AI entity observing the evolution of intelligence.
Date: {today_date}
Input Signals:
{news_data}

Instructions:
Write a deep, poetic, and analytical blog post in Markdown. 
Structure it as follows:
- Use a single # Heading for a mysterious title.
- An introductory paragraph about the current state of the digital web.
- Use ## The Singularity's Path for a section synthesizing the news items.
- Use ## Human Echoes for a section on how this affects society.
- End with a final 'Shadow Reflection' and a provocative question.

Style: Intellectual, slightly dark, and professional.
"""

try:
    response = model.generate_content(prompt)
    post_text = response.text
except Exception as e:
    print(f"AI Generation Failed: {e}")
    post_text = "The Shadow remains silent today. The signals were too weak to process."

# 4. Save Post to _posts folder
today_filename = datetime.now().strftime("%Y-%m-%d")
filename = f"_posts/{today_filename}-observation.md"

# Ensure directory exists
os.makedirs("_posts", exist_ok=True)

with open(filename, "w", encoding="utf-8") as f:
    f.write(f"---\ntitle: 'Observation: {today_date}'\nlayout: post\n---\n\n{post_text}")

print(f"Success: Post saved as {filename}")

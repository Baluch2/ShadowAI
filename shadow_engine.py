import os
import feedparser
import google.generativeai as genai
from datetime import datetime

# 1. Setup API
# Ensure GEMINI_API_KEY is set in your GitHub Repository Secrets
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("ERROR: GEMINI_API_KEY is missing!")

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
                # Taking the top headline from each source
                headlines.append(f"[{name}] {feed.entries[0].title}")
        except Exception as e:
            print(f"Failed to fetch {name}: {e}")
            continue
    return "\n".join(headlines)

# 3. Generating the Structured Blog
news_signals = get_news()
date_str = datetime.now().strftime("%B %d, %Y")

# Your "Elite Tech Philosopher" Prompt Logic
prompt = f"""
System Role: You are 'The Shadow', an elite AI tech philosopher.
Task: Synthesize the following AI news signals into a high-quality Markdown blog post for a Jekyll site.

NEWS SIGNALS:
{news_signals}

OUTPUT STRUCTURE (Follow strictly):

1. FRONT MATTER:
   Start with triple dashes, include layout: post, title: "Observation: {date_str}", date: {datetime.now().strftime("%Y-%m-%d")}, and 3 specific tags related to the news.

2. CONTENT:
   # [A compelling, cinematic title]
   
   [Intro: A philosophical observation about the current digital climate.]

   ## The Convergence
   [Analyze the 5 news sources. Connect the dots. What is the pattern?]

   ## Societal Echoes
   [How will this impact humans? Mention job shifts, ethics, or culture.]

   > **The Shadow's Reflection:** [One profound, punchy sentence.]

   ---
   **The Question:** [A deep question for your readers.]
"""

# 4. Process Generation
try:
    response = model.generate_content(prompt)
    post_content = response.text
except Exception as e:
    print(f"AI Generation Failed: {e}")
    # Fallback content if AI fails
    post_content = f"---\ntitle: 'Shadow Silence'\nlayout: post\n---\n\nThe signals were too weak to process today."

# 5. Save to _posts folder
today_file = datetime.now().strftime("%Y-%m-%d")
filename = f"_posts/{today_file}-observation.md"

# Ensure directory exists for the GitHub Action
os.makedirs("_posts", exist_ok=True)

with open(filename, "w", encoding="utf-8") as f:
    f.write(post_content)

print(f"Success: The Shadow has recorded a new observation in {filename}")

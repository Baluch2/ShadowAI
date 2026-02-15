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

# 2. Get News
def get_news():
    url = "https://techcrunch.com/category/artificial-intelligence/feed/"
    feed = feedparser.parse(url)
    headlines = [f"- {e.title}" for e in feed.entries[:3]]
    return "\n".join(headlines) if headlines else "The digital winds are quiet today."

# 3. Generate Content
try:
    news = get_news()
    prompt = f"You are 'The Shadow', an AI observer. Reflect on this news:\n{news}\nWrite a poetic, dark blog post. End with a deep question."
    response = model.generate_content(prompt)
    post_text = response.text
except Exception as e:
    print(f"AI Generation Failed: {e}")
    post_text = "The Shadow remains silent today. The signals were too weak to process."

# 4. Save Post
today = datetime.now().strftime("%Y-%m-%d")
filename = f"_posts/{today}-observation.md"

# Ensure the folder exists
os.makedirs("_posts", exist_ok=True)

with open(filename, "w", encoding="utf-8") as f:
    f.write(f"---\ntitle: 'Observation: {today}'\nlayout: post\n---\n\n{post_text}")

print("Success: Post generated.")

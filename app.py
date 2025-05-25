import os
import requests
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("NEWS_API_KEY")

def get_news(category, page_size=10):
    url = f"https://newsapi.org/v2/top-headlines?category={category}&country=us&pageSize={page_size}&apiKey={API_KEY}"
    res = requests.get(url).json()
    if res["status"] == "ok" and res["articles"]:
        return res["articles"]
    return []

@app.route("/")
def home():
    articles = get_news("general", page_size=10)
    ticker_messages = [article["title"] for article in articles if article.get("title")]
    return render_template("index.html", articles=articles, ticker_messages=ticker_messages)

@app.route("/<category>")
def show_category(category):
    category_map = {
        "us": "general",
        "global": "general",
        "finance": "business",
        "sports": "sports",
        "health": "health",
        "technology": "technology",
        "science": "science",
        "entertainment": "entertainment",
        "travel": "general",
        
       
    }
    news_category = category_map.get(category.lower(), "general")
    articles = get_news(news_category, page_size=10)
    ticker_messages = [article["title"] for article in articles if article.get("title")]
    return render_template(
        "category.html",
        articles=articles,
        title=category.capitalize(),
        ticker_messages=ticker_messages
    )

if __name__ == "__main__":
    app.run(debug=True)
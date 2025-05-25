import os
import requests
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("NEWS_API_KEY")

def get_news(category):
    url = f"https://newsapi.org/v2/top-headlines?category={category}&country=us&pageSize=1&apiKey={API_KEY}"
    res = requests.get(url).json()
    if res["status"] == "ok" and res["articles"]:
        article = res["articles"][0]
        return {
            "title": article["title"],
            "snippet": article["description"] or "No description available"
        }
    return {"title": f"No {category} news", "snippet": "No data found."}

@app.route("/")
def home():
    article = get_news("general")
    return render_template("index.html", article=article)

@app.route("/<category>")
def show_category(category):
    category_map = {
        "us": "general",
        "global": "general",
        "finance": "business",
        "sports": "sports",
        "local": "general",
        "business": "business"
    }

    news_category = category_map.get(category.lower(), "general")
    url = f"https://newsapi.org/v2/top-headlines?category={news_category}&country=us&pageSize=10&apiKey={API_KEY}"
    res = requests.get(url).json()
    articles = res.get("articles", [])
    return render_template("category.html", articles=articles, title=category.capitalize())

if __name__ == "__main__":
    app.run(debug=True)

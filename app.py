import os
import requests
import openai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def get_news(category=None, query=None, page_size=5):
    if query:
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    else:
        url = f"https://newsapi.org/v2/top-headlines?category={category}&country=us&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    res = requests.get(url).json()
    if res.get("status") == "ok" and res.get("articles"):
        return res["articles"]
    return []

@app.route("/")
def home():
    articles = get_news(category="general", page_size=10)
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
    articles = get_news(category=news_category, page_size=10)
    ticker_messages = [article["title"] for article in articles if article.get("title")]
    return render_template(
        "category.html",
        articles=articles,
        title=category.capitalize(),
        ticker_messages=ticker_messages
    )

@app.route("/ai/ask", methods=["POST"])
def ai_ask():
    data = request.get_json()
    question = data.get("question", "")
    source = data.get("source", "ai")  # "ai" or "news"

    if not question:
        return jsonify({"answer": "Please enter a question."})

    if source == "news":
        articles = get_news(query=question, page_size=3)
        if articles:
            answer = "<br><br>".join([
                f"<b>{a['title']}</b><br><small>{a.get('description','')}</small><br><a href='{a['url']}' target='_blank'>Read more</a>"
                for a in articles
            ])
        else:
            answer = "No news articles found for your query."
        return jsonify({"answer": answer})

    # Default: Use OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI news assistant. "
                        "When asked for the latest news or news on a topic, always provide at least 3 news items. "
                        "For each item, use <b> for the headline and <small> for a 1-2 sentence summary. "
                        "Format your response in HTML. "
                        "Example:\n"
                        "<b>Headline 1</b><br><small>Summary 1</small><br><br>"
                        "<b>Headline 2</b><br><small>Summary 2</small><br><br>"
                        "<b>Headline 3</b><br><small>Summary 3</small>"
                    )
                },
                {"role": "user", "content": question}
            ],
            max_tokens=400,
            temperature=0.7,
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = "Sorry, I couldn't get an answer right now."

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=False)
# import os
# from flask import Flask, render_template, request, jsonify
# from dotenv import load_dotenv

# load_dotenv()

# from ai_routes import ai_bp

# app = Flask(__name__)
# app.register_blueprint(ai_bp)

# @app.route("/")
# def index():
    
#     articles = [
#         {
#             "title": "Sample News 1",
#             "description": "Description for news 1.",
#             "url": "#",
#             "urlToImage": "/static/placeholder.jpg",
#             "category": "General",
#             "author": "Reporter 1",
#             "source": {"name": "USA News Global"}
#         },
#     ]
#     ticker_messages = [
#         "Breaking: Major event just happened",
#         "Weather update: Sunny across the country",
#         "Sports: Local team wins championship"
#     ]
#     return render_template(
#         "index.html",
#         articles=articles,
#         ticker_messages=ticker_messages
#     )

# @app.route("/category/<category>")
# def category(category):
#     articles = [
#         {
#             "title": f"{category.title()} News 1",
#             "description": f"Description for {category} news 1.",
#             "url": "#",
#             "urlToImage": "/static/placeholder.jpg",
#             "category": category.title(),
#             "author": "Reporter 2",
#             "source": {"name": "USA News Global"}
#         },
#     ]
#     ticker_messages = [
#         f"{category.title()} updates: Latest developments",
#         "Related stories from around the world",
#         "Breaking news and live coverage"
#     ]
#     return render_template(
#         "category.html",
#         title=category.title(),
#         articles=articles,
#         ticker_messages=ticker_messages
#     )

# if __name__ == "__main__":
#     app.run(debug=True)
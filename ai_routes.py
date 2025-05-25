# ai_routes.py
import os
import openai
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/api/ask", methods=["POST"])
def ask():
    prompt = request.json.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4 if you have access
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

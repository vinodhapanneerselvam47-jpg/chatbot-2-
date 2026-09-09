import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai

from chatbot_config import SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set in the .env file.")

client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-3.1-flash-lite"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"response": "Please enter a question."}), 400

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=message,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": 0.3,
            },
        )

        answer = response.text or "Sorry, I could not generate a response."
        return jsonify({"response": answer})

    except Exception:
        return jsonify({
            "response": "Sorry, something went wrong while processing your question."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)

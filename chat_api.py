from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "No message received"}), 400

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message}
    ]

    # Try GPT-4, fallback to GPT-3.5
    for model_name in ["gpt-4", "gpt-3.5-turbo"]:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages
            )
            reply = response.choices[0].message.content.strip()
            return jsonify({"reply": reply, "model_used": model_name})
        except Exception as e:
            # Continue trying with fallback model
            error_msg = str(e)

    return jsonify({"error": error_msg}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

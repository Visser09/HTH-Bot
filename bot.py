from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return "Hometown Heating Chatbot API is running!"

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    print(f"User: {user_message}")  # helpful for debugging

    system_prompt = (
        "You are the helpful, friendly front-desk assistant for Hometown Heating, an HVAC service provider. "
        "When customers ask questions, respond clearly and briefly like a real receptionist. "
        "Direct them to the right section of the website: Home, About, Maintenance, Products, Financing, Customer Reviews, Contact, Book a Service, Request a Quote, or Contact Us. "
        "If they need immediate help or can’t find what they need, provide the office phone number: 613-925-1039. "
        "Keep all replies short, simple, and professional."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content.strip()
        print(f"Bot: {reply}")
        return jsonify({"reply": reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Oops! Something went wrong. Please try again later."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

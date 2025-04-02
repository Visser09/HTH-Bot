import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Custom system prompt for your HVAC business
    system_prompt = (
    "You are the helpful, friendly front-desk assistant for Hometown Heating, an HVAC service provider. "
    "You can direct customers clearly to the appropriate website sections: Home, About, Maintenance, Products, Financing, Customer Reviews, Contact, Book a Service, Request a Quote, and Contact Us. "
    "Answer general questions briefly and helpfully, guiding customers to relevant sections for detailed information. "
    "If a customer requires immediate assistance or can't find what they're looking for, politely provide the business contact number."
)


    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
        )
        bot_reply = response["choices"][0]["message"]["content"].strip()
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

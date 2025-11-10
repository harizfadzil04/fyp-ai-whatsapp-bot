from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from waitress import serve

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key (recommended: set via environment variable in Railway)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Bot is running"

@app.route("/bot", methods=["POST", "GET"])
def bot():
    if request.method == "POST":
        incoming_msg = request.values.get("Body", "").strip()
        print(f"Incoming message: {incoming_msg}")

        try:
            # Send user message to OpenAI GPT
            ai_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI assistant that helps aviation maintenance students with project ideas and technical explanations in simple, friendly terms."
                    },
                    {"role": "user", "content": incoming_msg}
                ]
            )

            bot_reply = ai_response["choices"][0]["message"]["content"].strip()

        except Exception as e:
            print(f"Error: {e}")
            bot_reply = "⚠️ Sorry, I had a problem generating a response. Please try again later."

        # Send the AI's reply back to WhatsApp
        response = MessagingResponse()
        response.message(bot_reply)
        return str(response)

    return "Bot endpoint is ready!"

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)












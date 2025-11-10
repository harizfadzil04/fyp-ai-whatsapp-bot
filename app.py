from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
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

        from twilio.twiml.messaging_response import MessagingResponse
        response = MessagingResponse()

        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            ai_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful WhatsApp assistant."},
                    {"role": "user", "content": incoming_msg}
                ]
            )

            bot_reply = ai_response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            bot_reply = "⚠️ Sorry, I had a problem generating a response."

        response.message(bot_reply)
        return str(response)

    return "Bot endpoint is ready."

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)















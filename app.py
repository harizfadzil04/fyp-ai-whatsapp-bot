from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running"

@app.route("/bot", methods=["POST", "GET"])
def bot():
    if request.method == "POST":
        incoming_msg = request.values.get("Body", "").lower()
        print(f"Incoming message: {incoming_msg}")

        # Example basic reply (you can replace this later)
        bot_reply = "Hello! Your bot is connected successfully 🚀"

        # Build Twilio XML response
        response = MessagingResponse()
        response.message(bot_reply)
        return str(response)

    # For GET request (when you test from browser)
    return "Bot endpoint is ready!"

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)







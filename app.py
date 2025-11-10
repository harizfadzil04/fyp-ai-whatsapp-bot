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
        incoming_msg = request.values.get('Body', '').lower()
        print(f"Incoming message: {incoming_msg}")

        user_message = request.form.get('Body')
        print("User said:", user_message)

        result = subprocess.run(["python", "conversation_bot.py", user_message],
                                capture_output=True, text=True)

        bot_reply = result.stdout.strip()
        response = MessagingResponse()
        response.message(bot_reply)
        return str(response)

    return "Message received"

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)





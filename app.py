from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import subprocess

app = Flask(__name__)

@app.route("/bot", methods=["POST"])
def bot():
    user_message = request.form.get("Body")
    print("User said:", user_message)

    # Call your existing conversation_bot.py here
    result = subprocess.run(
        ["python", "conversation_bot.py", user_message],
        capture_output=True, text=True
    )

    bot_reply = result.stdout.strip()

    # Send back to WhatsApp
    response = MessagingResponse()
    response.message(bot_reply)
    return str(response)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)



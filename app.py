from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import subprocess

app = Flask(__name__)

@app.route("/bot", methods=["POST", "GET"])
def bot():
    if request.method == "POST":
        incoming_msg = request.values.get('Body', '').lower()
        print(f"Incoming message: {incoming_msg}")

        # Call your existing conversation bot here
        result = subprocess.run(
            ["python", "conversation_bot.py", incoming_msg],
            capture_output=True,
            text=True
        )
        bot_reply = result.stdout.strip()

        # Send back to WhatsApp
        response = MessagingResponse()
        response.message(bot_reply)
        return str(response)

    return "Bot is running"


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




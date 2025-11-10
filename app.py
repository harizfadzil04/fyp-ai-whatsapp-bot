from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
from waitress import serve
import os

# Import the FYP logic
from fyp_module import handle_fyp_query

# Flask app
app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return "Aeromentor is online and ready to assist students!"

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").strip()
    response = MessagingResponse()

    try:
        # Directly send message to FYP module (you can expand later to other modules)
        reply = handle_fyp_query(client, incoming_msg)
    except Exception as e:
        print(f"Error: {e}")
        reply = "⚠️ Sorry, I encountered an error. Please try again later."

    response.message(reply)
    return str(response)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)





















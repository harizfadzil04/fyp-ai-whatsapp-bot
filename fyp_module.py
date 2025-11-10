# fyp_module.py

conversation_memory = {}  # Will store conversations by user ID (from Twilio)

def handle_fyp_query(client, user_input, sender_id="default_user"):
    user_input = user_input.strip()

    # Initialize user session if not exists
    if sender_id not in conversation_memory:
        conversation_memory[sender_id] = {
            "context": "You are Aeromentor, an experienced aviation academic advisor who helps students with their Final Year Projects (FYPs).",
            "history": []
        }

    user_data = conversation_memory[sender_id]

    # Add user's message to memory
    user_data["history"].append({"role": "user", "content": user_input})

    # Combine context + history into one message list
    messages = [{"role": "system", "content": user_data["context"]}] + user_data["history"]

    # Generate AI response
    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=500,
        messages=messages
    )

    bot_reply = ai_response.choices[0].message.content.strip()

    # Save bot's response to memory
    user_data["history"].append({"role": "assistant", "content": bot_reply})

    # If message contains goodbye or reset request
    if any(word in user_input.lower() for word in ["bye", "reset", "thank you"]):
        del conversation_memory[sender_id]
        return "Good luck on your FYP, future aircraft engineer! 🛩️"

    return bot_reply



# fyp_module.py

conversation_memory = {}

def handle_fyp_query(client, user_input, sender_id="default_user"):
    user_input = user_input.strip()

    # Initialize user session if not exists
    if sender_id not in conversation_memory:
        conversation_memory[sender_id] = {
            "context": "You are Aeromentor, an experienced and friendly AI academic advisor who helps aviation students with their Final Year Projects (FYPs). You should always respond, even when confused. If the student’s request is unclear, politely ask clarifying questions instead of staying silent.",
            "history": []
        }

    user_data = conversation_memory[sender_id]

    # Save user's message
    user_data["history"].append({"role": "user", "content": user_input})

    # Combine memory context and message history
    messages = [{"role": "system", "content": user_data["context"]}] + user_data["history"]

    try:
        # Generate response using OpenAI
        ai_response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=500,
            messages=messages
        )

        bot_reply = ai_response.choices[0].message.content.strip()

        # Handle empty or unclear response (fallback)
        if not bot_reply or bot_reply.lower() in ["", "null"]:
            bot_reply = (
                "🤔 I’m not entirely sure what you mean. Could you rephrase that or tell me "
                "whether you want help with your FYP topic, thesis structure, or something else?"
            )

    except Exception as e:
        print(f"Error: {e}")
        bot_reply = (
            "⚠️ Sorry, I ran into an issue while generating a response. "
            "Can you simplify or rephrase your question?"
        )

    # Save bot reply to conversation memory
    user_data["history"].append({"role": "assistant", "content": bot_reply})

    # If user ends chat
    if any(word in user_input.lower() for word in ["bye", "reset", "thank you"]):
        del conversation_memory[sender_id]
        return "🛫 Got it! I’ll remember this for next time. Good luck with your project!"

    return bot_reply




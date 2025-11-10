conversation_history = {
    "topics": []  # Store last topic list for reference
}

def handle_fyp_query(client, user_input):
    user_input = user_input.lower().strip()

    # Reset memory if requested
    if "reset" in user_input:
        conversation_history.clear()
        conversation_history["topics"] = []
        return "✅ Memory cleared. Tell me your new FYP idea!"

    # If user asks for FYP ideas
    if "topic" in user_input or "idea" in user_input:
        topic_list = [
            "Implementation of predictive maintenance techniques in aircraft maintenance",
            "Development of a smart maintenance system for aircraft engines",
            "Integration of IoT devices for real-time monitoring of aircraft components",
            "Analysis of data-driven decision-making in aircraft maintenance",
            "Application of artificial intelligence for optimizing maintenance schedules",
            "Investigation of the use of drones for inspection and maintenance tasks",
            "Study on the impact of 3D printing technology in aircraft part manufacturing and repair",
            "Evaluation of the effectiveness of virtual reality (VR) and augmented reality (AR) in aircraft maintenance training"
        ]

        conversation_history["topics"] = topic_list
        formatted = "\n".join([f"{i+1}. {t}" for i, t in enumerate(topic_list)])
        return (
            "Of course! Here are some potential topics that previous students have explored:\n\n"
            f"{formatted}\n\n"
            "Reply with the topic number or name, and I’ll generate a full thesis outline for you."
        )

    # If user refers to a topic number (e.g., "topic number 7")
    if any(word in user_input for word in ["topic", "number", "option"]):
        import re
        match = re.search(r"\b(\d+)\b", user_input)
        if match:
            num = int(match.group(1))
            if 1 <= num <= len(conversation_history.get("topics", [])):
                topic = conversation_history["topics"][num - 1]
                return generate_full_thesis(client, topic)
            else:
                return "⚠️ That topic number isn’t in the list. Please try again."
    
    # Continue if topic already known
    if "topic" in conversation_history:
        return continue_thesis(client, conversation_history["topic"], user_input)

    # Fallback if no context
    return (
        "👋 Hi! I’m Aeromentor, your FYP assistant. You can ask me for FYP ideas, "
        "or tell me your project topic — for example:\n\n"
        "'My topic is optimization of aircraft propeller design.'"
    )


def generate_full_thesis(client, topic):
    conversation_history["topic"] = topic
    prompt = (
        f"You are Aeromentor, an experienced AI academic advisor for aircraft maintenance students. "
        f"Generate a detailed FYP report outline for the topic: '{topic}'. "
        "Include:\n1. Title\n2. Abstract\n3. Introduction\n4. Problem Statement\n"
        "5. Objectives\n6. Literature Review\n7. Methodology\n8. Expected Results\n9. Conclusion.\n"
        "Write in professional academic tone suitable for diploma-level thesis."
    )

    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=700,
        messages=[
            {"role": "system", "content": "You are Aeromentor, a friendly FYP mentor for aviation students."},
            {"role": "user", "content": prompt}
        ]
    )
    return "📘 Here’s your FYP draft for that topic:\n\n" + ai_response.choices[0].message.content


def continue_thesis(client, topic, new_input):
    prompt = (
        f"You are continuing an academic thesis about '{topic}'. "
        f"The student said: '{new_input}'. Continue the writing or respond helpfully."
    )

    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=400,
        messages=[
            {"role": "system", "content": "You are Aeromentor, an expert in guiding students with FYP writing."},
            {"role": "user", "content": prompt}
        ]
    )
    return ai_response.choices[0].message.content



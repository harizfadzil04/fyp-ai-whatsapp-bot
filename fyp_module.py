conversation_history = {}

def handle_fyp_query(client, user_input):
    user_input = user_input.lower().strip()

    # Memory for basic session (using sender ID later if needed)
    global conversation_history
    if "reset" in user_input:
        conversation_history.clear()
        return "✅ Conversation memory reset. What new topic would you like to discuss?"

    # Detect if user wants to start thesis generation
    if any(word in user_input for word in ["thesis", "fyp", "project", "proposal"]):
        conversation_history["topic"] = user_input
        return generate_full_thesis(client, user_input)

    # If context already exists, continue the thesis
    elif "topic" in conversation_history:
        return continue_thesis(client, conversation_history["topic"], user_input)

    else:
        return (
            "👋 Hi! I’m Aeromentor, your FYP advisor. "
            "Please tell me your FYP topic or question — for example:\n\n"
            "‘My topic is optimization of aircraft propeller blade angle for better efficiency.’"
        )


def generate_full_thesis(client, topic):
    prompt = (
        f"You are Aeromentor, an experienced AI academic advisor for aircraft maintenance engineering students. "
        f"Generate a complete Final Year Project (FYP) report outline for the topic: '{topic}'. "
        "Include sections such as:\n"
        "1. Title\n"
        "2. Abstract\n"
        "3. Introduction\n"
        "4. Problem Statement\n"
        "5. Objectives\n"
        "6. Literature Review\n"
        "7. Methodology\n"
        "8. Expected Results and Discussion\n"
        "9. Conclusion\n"
        "Write in professional academic tone suitable for diploma-level thesis."
    )

    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=700,
        messages=[
            {"role": "system", "content": "You are Aeromentor, a kind and intelligent FYP academic AI mentor."},
            {"role": "user", "content": prompt}
        ]
    )
    content = ai_response.choices[0].message.content
    return "📘 Here’s your FYP draft:\n\n" + content


def continue_thesis(client, topic, new_input):
    prompt = (
        f"You are continuing an academic thesis about '{topic}'. "
        f"The student asked: '{new_input}'. "
        "Continue writing helpfully and in academic format."
    )

    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=400,
        messages=[
            {"role": "system", "content": "You are Aeromentor, an expert in academic writing and FYP consultation."},
            {"role": "user", "content": prompt}
        ]
    )
    return ai_response.choices[0].message.content

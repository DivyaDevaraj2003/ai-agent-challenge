from flask import Blueprint, request, jsonify
from google.generativeai import GenerativeModel
import google.generativeai as genai
import os
import re

# This line has been removed as it conflicts with the deployment environment.
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "agent_config/credential.json"

wellness_bp = Blueprint('wellness_bp', __name__)
genai.configure()

# In-memory chat history store (for each user/session)
chat_sessions = {}

# Define conversational keywords
GREETINGS = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon"]
THANKS = ["thanks", "thank you", "thx"]


@wellness_bp.route("/ask", methods=["POST"])
def ask_genetic():
    data = request.get_json()
    user_query = data.get("query")
    user_id = data.get("user_id", "default_user")

    if not user_query:
        return jsonify({"answer": "Please provide a query."}), 400

    # Handle conversational phrases first
    cleaned_query = user_query.lower().strip()
    if cleaned_query in GREETINGS:
        return jsonify({"answer": "Hello! How can I help you with your genetic wellness questions today?"})
    if cleaned_query in THANKS:
        return jsonify({"answer": "You're welcome! Do you have any other questions?"})

    # If it's a real question, proceed to the Gemini model
    try:
        model = GenerativeModel("gemini-1.5-flash")

        # Use persistent chat if user session exists
        if user_id in chat_sessions:
            chat = chat_sessions[user_id]
        else:
            chat = model.start_chat(history=[])
            chat_sessions[user_id] = chat

        # Format the system prompt for the LLM
        prompt = f"""
You are an expert assistant. Answer the user's question as clearly and informatively as possible.

IMPORTANT: 
- Format your answer as 3 to 4 bullet points.
- Each bullet point must be a concise paragraph (2-3 sentences) that is separated from the next by a blank line (TWO newline characters).
- Begin each bullet with '- ' (a dash and a space at line start, not a number or asterisk).
- Do NOT cluster multiple ideas into one bullet.
- Do not use markdown or formatting like bold or italics.
- Do not include a greeting, summary, or conclusion.

Answer the following question:

{user_query}
"""

        # Send message to Gemini
        response = chat.send_message(prompt)
        response_text = response.text.strip()

        # Bullet formatting cleanup
        response_text = response_text.lstrip('-').strip()
        bullets = re.split(r'(?:^|\n)\s*-\s+', response_text)
        bullets = [b.strip() for b in bullets if b.strip()]
        formatted = '\n\n- '.join(bullets)
        if formatted and not formatted.startswith('-'):
            formatted = '- ' + formatted

        return jsonify({"answer": formatted})

    except Exception as e:
        print("❌ Gemini error:", e)
        return jsonify({"answer": f"Error: {str(e)}"}), 500
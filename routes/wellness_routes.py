from flask import Blueprint, request, jsonify
from google.generativeai import GenerativeModel
import google.generativeai as genai
import os

# Configure the library ONCE using the environment variables set on Render
# Do not pass any arguments here. The library finds the key automatically.
genai.configure()

wellness_bp = Blueprint('wellness_bp', __name__)

# In-memory chat history store
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

    try:
        model = GenerativeModel("gemini-1.5-flash")

        if user_id in chat_sessions:
            chat = chat_sessions[user_id]
        else:
            chat = model.start_chat(history=[])
            chat_sessions[user_id] = chat

        prompt = f"Answer the following question about genetic wellness clearly and concisely: {user_query}"
        response = chat.send_message(prompt)
        
        return jsonify({"answer": response.text})

    except Exception as e:
        error_message = f"{type(e).__name__}: {str(e)}"
        print(f"❌ Gemini API Error: {error_message}")
        return jsonify({"answer": "Sorry, the AI service failed. Please check the server logs for details."}), 500
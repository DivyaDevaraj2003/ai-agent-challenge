from flask import Blueprint, request, jsonify
from google.generativeai import GenerativeModel
import google.generativeai as genai
import os
import re

# This relies on the environment variables you set on Render.
# The problematic os.environ[...] line has been removed.
genai.configure()

wellness_bp = Blueprint('wellness_bp', __name__)

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

        # --- MODIFIED: A simpler prompt for faster responses on the server ---
        prompt = f"You are an expert assistant for genetic wellness. Answer the following question clearly and concisely: {user_query}"

        # Send message to Gemini and maintain history
        response = chat.send_message(prompt)
        
        # Directly return the model's response text
        return jsonify({"answer": response.text})

    except Exception as e:
        # This will print the detailed error to your Render logs
        error_message = f"{type(e).__name__}: {str(e)}"
        print(f"❌ Gemini API Error: {error_message}")
        return jsonify({"answer": "Sorry, the AI service failed. Please check the server logs for details."}), 500
from flask import Blueprint, request, jsonify
from google.generativeai import GenerativeModel
import google.generativeai as genai
import os
import re

wellness_bp = Blueprint('wellness_bp', __name__)
genai.configure()

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

    # If it's a real question, proceed to the Gemini model
    try:
        model = GenerativeModel("gemini-1.5-flash")

        # Use persistent chat if user session exists
        if user_id in chat_sessions:
            chat = chat_sessions[user_id]
        else:
            chat = model.start_chat(history=[])
            chat_sessions[user_id] = chat

        # --- UPDATED: Simplified prompt to respond faster ---
        prompt = f"""
You are an expert assistant for genetic wellness. Answer the following question clearly and concisely.

Question: {user_query}
"""

        # Send message to Gemini
        response = chat.send_message(prompt)
        
        return jsonify({"answer": response.text})

    except Exception as e:
        print("❌ Gemini error:", e)
        return jsonify({"answer": f"Error: {str(e)}"}), 500
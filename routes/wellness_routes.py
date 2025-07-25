from flask import Blueprint, request, jsonify
from google.generativeai import GenerativeModel
import google.generativeai as genai
import os

# This configures genai using the environment variable you set on Render
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

wellness_bp = Blueprint('wellness_bp', __name__)

# Define conversational keywords
GREETINGS = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon"]
THANKS = ["thanks", "thank you", "thx"]


@wellness_bp.route("/ask", methods=["POST"])
def ask_genetic():
    data = request.get_json()
    user_query = data.get("query")

    if not user_query:
        return jsonify({"answer": "Please provide a query."}), 400

    # Handle conversational phrases first
    cleaned_query = user_query.lower().strip()
    if cleaned_query in GREETINGS:
        return jsonify({"answer": "Hello! How can I help you with your genetic wellness questions today?"})
    if cleaned_query in THANKS:
        return jsonify({"answer": "You're welcome! Do you have any other questions?"})

    try:
        # Initialize the model directly
        model = GenerativeModel("gemini-1.5-flash")

        # Create a simple, direct prompt
        prompt = f"You are an expert assistant for genetic wellness. Answer the following question clearly and concisely: {user_query}"

        # Make a direct, stateless call to the model (this is the simplified part)
        response = model.generate_content(prompt)
        
        return jsonify({"answer": response.text})

    except Exception as e:
        # Print the actual error to the Render logs for debugging
        print(f"❌ An actual Gemini error occurred: {e}")
        return jsonify({"answer": "Sorry, an error occurred while connecting to the AI service."}), 500
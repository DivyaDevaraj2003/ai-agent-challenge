from flask import Blueprint, request, jsonify
from google.generativeai import GenerativeModel
import google.generativeai as genai
import os
import re

# Set Google credentials (adjust path as needed)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "agent_config/credential.json"

wellness_bp = Blueprint('wellness_bp', __name__)

genai.configure()

@wellness_bp.route("/ask", methods=["POST"])
def ask_genetic():
    data = request.get_json()
    user_query = data.get("query")

    if not user_query:
        return jsonify({"answer": "Please provide a query."}), 400

    try:
        model = GenerativeModel("gemini-1.5-flash")

        prompt = f"""
You are an expert assistant. Answer the user's question as clearly and informatively as possible.

IMPORTANT: 
- Format your answer as 3 to 4 bullet points.
- Each bullet point must be a concise paragraph (2-3 sentences) that is separated from the next by a blank line (TWO newline characters).
- Begin each bullet with '- ' (a dash and a space at line start, not a number or asterisk).
- Do NOT cluster multiple ideas into one bullet.
- Do not use markdown or formatting like bold or italics.
- Do not include a greeting, summary, or conclusion.

Here is an example of the required format:

- This is the first bullet point. It provides some information about the topic. This is a second sentence for detail.

- This is the second bullet point. It is also a short paragraph, and has its own blank line above.

- This is the third bullet point. Notice the blank line between each bullet.

Answer the following question:

{user_query}
"""

        response = model.generate_content(prompt)
        response_text = response.text.strip()

        # --- Robust bullet formatting ---
        # Remove leading dashes/whitespace and split on "- "

        # Remove any stray places where "- " is not at the true start or after a newline
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

from flask import Blueprint, request, jsonify, current_app
# Import the main response generator function, not the old one
from agents.faq_agent import generate_faq_response

faq_bp = Blueprint('faq_bp', __name__)

@faq_bp.route("/ask", methods=["POST"])
def ask_faq():
    data = request.get_json() or {}
    user_query = data.get("query", "").strip()

    if not user_query:
        return jsonify({"error": "Please provide a question."}), 400

    # Access the pre-loaded FAQ data from the app's config
    scraped_faqs = current_app.config['SCRAPED_FAQS']
    custom_faqs = current_app.config['CUSTOM_FAQS']

    # Call the main agent function with all the required data
    answer = generate_faq_response(user_query, scraped_faqs, custom_faqs)

    print("Received Query:", user_query)
    print("Responding With:", answer)

    return jsonify({"answer": answer})
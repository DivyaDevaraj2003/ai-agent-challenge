from flask import Blueprint, request, jsonify
from agents.faq_agent import get_faq_answer

faq_bp = Blueprint('faq_bp', __name__)

@faq_bp.route("/ask", methods=["POST"])
def ask_faq():
    data = request.get_json() or {}
    user_query = data.get("query", "").strip()
    print("Received Query:", user_query)  # Debug

    if not user_query:
        return jsonify({"error": "Please provide a question."}), 400

    answer = get_faq_answer(user_query)
    print("Responding With:", answer)  # Debug

    return jsonify({"answer": answer})

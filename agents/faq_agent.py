import re
from difflib import get_close_matches

# Import your scraper
from scrape_faqs import scrape_nugenomics_faq_aux

# --- New: Define lists for conversational keywords ---
GREETINGS = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
THANKS = ["thanks", "thank you", "thx", "appreciate it", "thank u"]

# Scrape the latest FAQ data when the app starts
FAQ_DATA = scrape_nugenomics_faq_aux()

def clean_text(text):
    """Lowercase and remove punctuation for better matching."""
    return re.sub(r"[^\w\s]", "", text.lower())

def get_faq_answer(query):
    """
    Return the best-matched answer from FAQ_DATA.
    Returns None if no good match is found.
    """
    query_c = clean_text(query)

    # Exact keyword presence matching
    for q, a in FAQ_DATA.items():
        if all(word in clean_text(q) for word in query_c.split()):
            return a

    # Fuzzy match with cutoff
    questions = list(FAQ_DATA.keys())
    # Use the cleaned query for matching
    matches = get_close_matches(query_c, [clean_text(q) for q in questions], n=1, cutoff=0.5)
    if matches:
        # Find the original question from the cleaned match
        idx = [clean_text(q) for q in questions].index(matches[0])
        return FAQ_DATA[questions[idx]]

    # --- Changed: Return None if no answer is found ---
    return None

def generate_faq_response(user_query):
    """
    This is the main function to call. It handles greetings and thanks,
    then tries to find an FAQ answer, and provides a helpful fallback message.
    """
    cleaned_query = clean_text(user_query)

    # 1. Check for greetings
    if cleaned_query in GREETINGS:
        return "Hello! How can I help you with our frequently asked questions today?"

    # 2. Check for thanks
    if cleaned_query in THANKS:
        return "You're welcome! Is there anything else I can help you with?"

    # 3. If not a greeting or thanks, search the FAQ
    answer = get_faq_answer(user_query)

    # 4. If an answer is found, return it. Otherwise, return the helpful fallback.
    if answer:
        return answer
    else:
        return "That's a great question. While I can only answer our FAQs, you can contact our support team for more detailed inquiries."

# --- Example of how to use it in your Flask app ---
#
# from flask import request, jsonify
# from faq_agent import generate_faq_response
#
# @app.route('/faq/ask', methods=['POST'])
# def ask_faq():
#     user_message = request.json.get('query')
#     if not user_message:
#         return jsonify({'error': 'No query provided'}), 400
#
#     response_text = generate_faq_response(user_message)
#     return jsonify({'answer': response_text})
import re
from difflib import get_close_matches

# It's assumed your scrape_faqs.py file is in the root directory or accessible.
from scrape_faqs import scrape_nugenomics_faq_aux

# 1. Define all conversational keywords and phrases
GREETINGS = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
THANKS = ["thank you", "thanks", "thx", "thank u", "appreciate"]
IDENTITY_QUERIES = ["who are you", "what are you", "what is your purpose", "are you a bot", "are you human"]
SHORT_RESPONSES = ["yes", "no", "ok", "k", "okay", "got it"]


# 2. Define your own custom, hardcoded questions and answers
ADDITIONAL_FAQ = {
    "Is NuGenomics available outside India?": "Currently, NuGenomics services are mainly available in India. Contact support for international options.",
    "Do you have corporate wellness programs?": "Yes, NuGenomics provides corporate wellness packages for organizations. Please contact our business team!",
    "Can I get a printed genetic report?": "Yes, you can request a printed report from our support team.",
}

def clean_text(text):
    """Lowercase text and remove all punctuation except for letters, numbers, and spaces."""
    return re.sub(r"[^\w\s]", "", text.lower()).strip()

def matches_any_whole_word(text, word_list):
    """Checks if any whole word from the provided list is present in the text."""
    return any(re.search(r'\b{}\b'.format(re.escape(word)), text) for word in word_list)

def get_faq_answer(query, main_faq, custom_faq):
    """Finds the best-matched answer from the FAQ data with a strict cutoff."""
    query_c = clean_text(query)

    # First, try to find a perfect match where all query words are present in a question
    for q, a in custom_faq.items():
        if all(word in clean_text(q) for word in query_c.split()):
            return a
    for q, a in main_faq.items():
        if all(word in clean_text(q) for word in query_c.split()):
            return a

    # If no perfect match, try a fuzzy string match with a stricter cutoff to avoid wrong guesses
    all_questions = list(custom_faq.keys()) + list(main_faq.keys())
    all_cleaned = [clean_text(q) for q in all_questions]
    
    matches = get_close_matches(query_c, all_cleaned, n=1, cutoff=0.6)
    
    if matches:
        # Find the original question from the cleaned match and return its answer
        idx = all_cleaned.index(matches[0])
        if idx < len(custom_faq):
            return list(custom_faq.values())[idx]
        else:
            idx2 = idx - len(custom_faq)
            return list(main_faq.values())[idx2]
            
    # Return None if no good match is found
    return None

def generate_faq_response(user_query, main_faq, custom_faq):
    """
    The main handler function to generate a response for any user query.
    It checks for conversational cues before attempting an FAQ search.
    """
    cleaned_query = clean_text(user_query)
    
    # 1. Check for conversational phrases first
    if matches_any_whole_word(cleaned_query, GREETINGS):
        return "Hello! How can I help you with our frequently asked questions today?"
    if matches_any_whole_word(cleaned_query, THANKS):
        return "You're welcome! Is there anything else I can help you with?"
    if matches_any_whole_word(cleaned_query, IDENTITY_QUERIES):
        return "I am an AI assistant for NuGenomics, designed to answer frequently asked questions from the website."

    # 2. Handle short but valid responses like "yes" or "ok"
    if cleaned_query in SHORT_RESPONSES:
        return "Great! Do you have another question?"

    # 3. Check if the remaining query is too short
    if len(cleaned_query.split()) < 3:
        return "That's a bit short. Could you please provide a more complete question?"

    # 4. If the query is long enough, search the FAQ
    answer = get_faq_answer(user_query, main_faq, custom_faq)
    
    if answer:
        return answer
    else:
        # Provide a polite fallback response if no answer is found
        return ("Thank you for your question! While I don’t have an immediate answer for that, "
                "our support team would be happy to help you directly.")

# Standalone test mode for quick command-line testing
if __name__ == "__main__":
    print("Loading FAQ data, please wait...")
    scraped_faqs = scrape_nugenomics_faq_aux() or {}  # Safeguard if scraper fails
    
    print("\n======================== FAQ Chatbot ========================")
    print("Type your question or 'exit' to quit.")
    
    while True:
        q = input("\nYou: ")
        if q.lower() == 'exit':
            break
        print("Bot:", generate_faq_response(q, scraped_faqs, ADDITIONAL_FAQ))
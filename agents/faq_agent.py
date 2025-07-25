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
    # --- Your Original 3 ---
    "Is NuGenomics available outside India?": "Currently, NuGenomics services are mainly available in India. Contact support for international options.",
    "Do you have corporate wellness programs?": "Yes, NuGenomics provides corporate wellness packages for organizations. Please contact our business team!",
    "Can I get a printed genetic report?": "Yes, you can request a printed report from our support team.",
    # --- The 5 I added previously ---
    "How is my genetic data kept private and secure?": "We use industry-standard encryption and secure cloud infrastructure to protect your data. Your personal information is stored separately from your genetic data, and we do not share it without your explicit consent.",
    "What kind of sample is required for the test?": "Our genetic test requires a simple, non-invasive saliva sample. The collection kit we send you includes easy-to-follow instructions and a pre-paid return envelope.",
    "Do I need a doctor's prescription to take the test?": "No, a doctor's prescription is not required to purchase our test. However, we strongly recommend discussing your results with a healthcare professional or one of our genetic counselors.",
    "Is the cost of the test covered by insurance?": "Currently, most insurance providers in India do not cover proactive genetic wellness tests. We recommend checking with your specific provider for the latest information on coverage.",
    "Does this test diagnose diseases?": "Our test is designed for wellness and proactive health insights, not for diagnosing diseases. It identifies genetic predispositions which should be used as part of a broader health plan in consultation with your doctor.",
    
    # --- New 20 Questions ---

    # Process & Logistics
    "How long does it take to get my results?": "Once our lab receives your sample, it typically takes 3-4 weeks to process and generate your personalized report. You will be notified via email when your results are ready.",
    "What is inside the collection kit?": "The kit includes a saliva collection tube, a funnel, stabilization fluid, a biohazard bag for the sample, and a detailed instruction manual. A pre-paid return shipping envelope is also included.",
    "Can I eat or drink before collecting the saliva sample?": "To ensure sample quality, please do not eat, drink, smoke, or chew gum for at least 30 minutes before providing your saliva sample.",
    "What if my collection kit is lost or damaged?": "If your kit arrives damaged or is lost, please contact our customer support team immediately, and we will arrange for a replacement kit to be sent to you.",
    "How do I activate my kit?": "You must activate your kit online using the unique barcode number provided inside the box. This links your sample to your secure online account.",

    # Report & Results
    "In what format will I receive my report?": "Your results will be available in a comprehensive digital report accessible through your secure online portal. You can view, download, and print it from there.",
    "Can you help me understand my results?": "Yes, we offer a complimentary post-test counseling session with one of our certified genetic counselors to help you understand your report and answer any questions you may have.",
    "Are the recommendations in the report a substitute for medical advice?": "No. The recommendations are for informational and educational purposes only. They are not a substitute for professional medical advice, diagnosis, or treatment.",
    "How often are the genetic insights updated?": "The field of genetics is constantly evolving. We periodically review new research and may update our reports with new insights. You will be notified if a significant update affects your results.",
    "Can my family members use my results?": "Your genetic report is unique to you. While you share DNA with family members, they would need to take their own test for accurate, personalized insights.",

    # Science & Technology
    "What technology is used for the genetic testing?": "We use state-of-the-art genotyping technology on a custom microarray chip, which analyzes hundreds of thousands of specific points in your genome with high accuracy.",
    "How accurate is the genetic test?": "Our laboratory testing process has an analytical accuracy of over 99%. The interpretation of the results is based on current, peer-reviewed scientific research.",
    "Does my DNA sample get stored?": "You can choose whether we store or discard your biological sample after it has been analyzed. You can manage your preferences from your account settings.",
    "What is the difference between genotyping and sequencing?": "Genotyping, which we use, looks at specific, well-studied points in your DNA. Whole-genome sequencing reads nearly all of your DNA. For wellness insights, genotyping is highly effective and more affordable.",

    # General & Policy
    "What is your refund policy?": "You can request a full refund before your sample collection kit has been shipped. Once shipped, refund policies may vary. Please refer to our Terms of Service for full details.",
    "Can I buy a test as a gift for someone?": "Yes, you can purchase a kit as a gift. The recipient will need to create their own account and register the kit's unique barcode themselves.",
    "Is there a minimum age to take the test?": "Yes, the person providing the sample must be at least 18 years of age.",
    "How can I delete my account and data?": "You have the right to close your account and have your personal data deleted at any time. You can initiate this process by contacting our customer support team.",
    "What if the test fails?": "In the rare event that our lab cannot process your sample, we will offer you a complimentary replacement kit at no charge.",
    "Who are your genetic counselors?": "Our team consists of board-certified genetic counselors with expertise in translating complex genetic information into practical and understandable health insights."
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
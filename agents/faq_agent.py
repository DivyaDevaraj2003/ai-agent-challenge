import re
from difflib import get_close_matches

# Import your scraper
from scrape_faqs import scrape_nugenomics_faq_aux

# Scrape the latest FAQ data when the app starts (or load from cached file for efficiency)
FAQ_DATA = scrape_nugenomics_faq_aux()

def clean_text(text):
    """Lowercase and remove punctuation for better matching."""
    return re.sub(r"[^\w\s]", "", text.lower())

def get_faq_answer(query):
    """Return the best-matched answer from FAQ_DATA."""
    query_c = clean_text(query)

    # Exact keyword presence matching
    for q, a in FAQ_DATA.items():
        if all(word in clean_text(q) for word in query_c.split()):
            return a

    # Fuzzy match with cutoff
    questions = list(FAQ_DATA.keys())
    matches = get_close_matches(query_c, [clean_text(q) for q in questions], n=1, cutoff=0.5)
    if matches:
        idx = [clean_text(q) for q in questions].index(matches[0])
        return FAQ_DATA[questions[idx]]

    return "Sorry, I couldn't find an answer. Please contact NuGenomics support."

import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_nugenomics_faqs():
    url = "https://www.nugenomics.in/faqs/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    faqs = []

    # Find all FAQ sections
    faq_sections = soup.find_all('div', class_='elementor-toggle-item')

    for section in faq_sections:
        question_elem = section.find('span', class_='elementor-toggle-title')
        answer_elem = section.find('div', class_='elementor-toggle-content')

        if question_elem and answer_elem:
            question = question_elem.get_text(strip=True)
            answer = answer_elem.get_text(separator=" ", strip=True)
            faqs.append({"question": question, "answer": answer})

    # Make sure the data folder exists
    os.makedirs("data", exist_ok=True)

    # Save to JSON
    with open("data/faqs.json", "w", encoding="utf-8") as f:
        json.dump(faqs, f, ensure_ascii=False, indent=4)

    print(f"✅ Scraped and saved {len(faqs)} FAQs to data/faqs.json")

if __name__ == "__main__":
    scrape_nugenomics_faqs()

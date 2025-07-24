from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scrape_nugenomics_faq_aux():
    options = Options()
    options.add_argument("--headless=new")  # or "--headless" for older versions
    driver = webdriver.Chrome(options=options)

    url = "https://www.nugenomics.in/faqs/"
    print(f"Fetching {url} with browser...")
    driver.get(url)
    time.sleep(8)   # Increase if you have a slow connection, decrease if fast

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    faqs = {}

    # Find each FAQ question header
    headers = soup.find_all('h4', class_='aux-toggle-header')
    print(f"Found {len(headers)} FAQ questions (AUX headers).")

    for header in headers:
        question = header.get_text(strip=True)
        # The answer is in the next sibling .acc-content-wrap > .aux-toggle-content
        content_wrap = header.find_next_sibling('div', class_='acc-content-wrap')
        if content_wrap:
            answer_div = content_wrap.find('div', class_='aux-toggle-content')
            if answer_div:
                answer = answer_div.get_text("\n", strip=True)
                faqs[question] = answer

    if not faqs:
        print("No FAQs found! Check selectors and increase sleep if needed.")
    else:
        for idx, (q, a) in enumerate(faqs.items(), 1):
            print(f"{idx}. Q: {q}\nA: {a}\n{'-'*60}")

    return faqs

if __name__ == "__main__":
    faqs = scrape_nugenomics_faq_aux()
    print(f"\nScraped a total of {len(faqs)} FAQs.")

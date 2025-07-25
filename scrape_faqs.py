from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scrape_nugenomics_faq_aux():
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    url = "https://www.nugenomics.in/faqs/"
    print(f"Fetching {url} with browser...")
    driver.get(url)
    time.sleep(8)

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    faqs = {}

    headers = soup.find_all('h4', class_='aux-toggle-header')
    print(f"Found {len(headers)} FAQ questions (AUX headers).")

    for header in headers:
        question = header.get_text(strip=True)
        content_wrap = header.find_next_sibling('div', class_='acc-content-wrap')
        if content_wrap:
            answer_div = content_wrap.find('div', class_='aux-toggle-content')
            if answer_div:
                answer = answer_div.get_text("\n", strip=True)
                faqs[question] = answer

    return faqs

if __name__ == "__main__":
    faqs = scrape_nugenomics_faq_aux()
    print(f"\nScraped a total of {len(faqs)} FAQs.")

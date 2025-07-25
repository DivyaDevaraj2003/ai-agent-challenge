import json
from scrape_faqs import scrape_nugenomics_faq_aux

print("Scraping FAQ site...")

# Run the scraper
faq_data = scrape_nugenomics_faq_aux()

# Save the data to a JSON file
if faq_data:
    with open("scraped_faqs.json", "w") as f:
        json.dump(faq_data, f, indent=4)
    print("Successfully saved FAQ data to scraped_faqs.json")
else:
    print("Scraper did not return any data.")
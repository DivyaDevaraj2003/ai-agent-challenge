# genetic_wellness_agent.py

import os
from dotenv import load_dotenv
from google.generativeai import configure, GenerativeModel

# Load .env where GOOGLE_APPLICATION_CREDENTIALS is set
load_dotenv()

# This picks the service account JSON automatically
configure()

# Now you can safely initialize Gemini models
model = GenerativeModel("gemini-1.5-pro")

response = model.generate_content("What is genetic wellness?")
print(response.text)

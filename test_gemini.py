from dotenv import load_dotenv
from google.generativeai import configure, GenerativeModel

# Load the .env file where GOOGLE_APPLICATION_CREDENTIALS is set
load_dotenv()

# Configure the SDK (reads the credentials from the env var)
configure()

# Load Gemini model using ADK
model = GenerativeModel("gemini-1.5-flash")


# Send a basic test prompt
response = model.generate_content("Test message: What is genetic wellness?")

# Print the output
print("\n--- Gemini Response ---\n")
print(response.text)

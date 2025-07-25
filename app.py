import json
from flask import Flask, render_template
from flask_cors import CORS

# Import your route blueprints
from routes.faq_routes import faq_bp
from routes.wellness_routes import wellness_bp

# Import only the custom FAQ data from the agent file
from agents.faq_agent import ADDITIONAL_FAQ

# --- Step 1: Load all data from local files ---
print("Loading FAQ data from file...")
try:
    # Read the pre-scraped data from the JSON file
    with open("scraped_faqs.json", "r") as f:
        SCRAPED_FAQS = json.load(f)
except FileNotFoundError:
    print("WARNING: scraped_faqs.json not found. FAQ agent will only use custom questions.")
    SCRAPED_FAQS = {}

# Load the hardcoded custom questions
CUSTOM_FAQS = ADDITIONAL_FAQ
print("FAQ data loaded successfully.")


# --- Step 2: Create and configure the Flask app ---
app = Flask(__name__, static_url_path='/static')
CORS(app)  # Enable CORS for all routes


# --- Step 3: Store the loaded data in the app's config ---
# This makes the data accessible from your blueprints (routes).
app.config['SCRAPED_FAQS'] = SCRAPED_FAQS
app.config['CUSTOM_FAQS'] = CUSTOM_FAQS


# Register Blueprints
app.register_blueprint(faq_bp, url_prefix="/faq")
app.register_blueprint(wellness_bp, url_prefix="/wellness")


# Serve Frontend
@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
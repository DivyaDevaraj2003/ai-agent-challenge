from flask import Flask, render_template
from flask_cors import CORS

# Import your route blueprints
from routes.faq_routes import faq_bp
from routes.wellness_routes import wellness_bp

# Import the functions/data needed for the FAQ agent
from agents.faq_agent import ADDITIONAL_FAQ
from scrape_faqs import scrape_nugenomics_faq_aux

# --- Step 1: Load all data before creating the app ---
print("Loading FAQ data, please wait...")
SCRAPED_FAQS = scrape_nugenomics_faq_aux() or {}  # Load scraped data
CUSTOM_FAQS = ADDITIONAL_FAQ                     # Load your custom questions
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
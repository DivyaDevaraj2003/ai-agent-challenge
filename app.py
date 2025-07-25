import json
import os
from flask import Flask, render_template
from flask_cors import CORS

# --- Step 1: Import Route Blueprints ---
# This structure keeps your routes organized in separate files.
print("Importing route blueprints...")
try:
    from routes.faq_routes import faq_bp
    from routes.wellness_routes import wellness_bp
    print("Successfully imported blueprints.")
except ImportError as e:
    print(f"FATAL: Could not import a blueprint. Check your file names and paths. Error: {e}")
    # Exit if blueprints can't be found, as the app is non-functional without them.
    exit()

# --- Step 2: Load Data from Local Files ---
# It's good practice to load data once at startup.
print("Loading FAQ data from local files...")
SCRAPED_FAQS = {}
CUSTOM_FAQS = {}

try:
    # Read the pre-scraped data from the JSON file
    with open("scraped_faqs.json", "r", encoding="utf-8") as f:
        SCRAPED_FAQS = json.load(f)
    print(f"Successfully loaded {len(SCRAPED_FAQS)} scraped FAQs.")
except FileNotFoundError:
    print("WARNING: 'scraped_faqs.json' not found. The FAQ agent will rely only on custom questions.")
except json.JSONDecodeError:
    print("ERROR: Could not parse 'scraped_faqs.json'. Please ensure it is a valid JSON file.")

try:
    # Import only the custom FAQ data from the agent file
    from agents.faq_agent import ADDITIONAL_FAQ
    CUSTOM_FAQS = ADDITIONAL_FAQ
    print(f"Successfully loaded {len(CUSTOM_FAQS)} custom FAQs.")
except ImportError:
     print("WARNING: Could not import ADDITIONAL_FAQ from agents.faq_agent. No custom FAQs will be loaded.")
except Exception as e:
     print(f"An error occurred loading custom FAQs: {e}")


# --- Step 3: Create and Configure the Flask App ---
print("Creating and configuring Flask application...")
# We specify the static folder to ensure CSS/JS files are served correctly.
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Enable Cross-Origin Resource Sharing (CORS) for all routes.
# This is essential for allowing your frontend (if on a different domain/port) to call the API.
CORS(app)
print("CORS has been enabled for all routes.")

# --- Step 4: Store Loaded Data in the App's Config ---
# This is the standard Flask way to make data or configurations
# globally accessible to your blueprints and routes.
app.config['SCRAPED_FAQS'] = SCRAPED_FAQS
app.config['CUSTOM_FAQS'] = CUSTOM_FAQS
print("FAQ data has been stored in app config.")


# --- Step 5: Register Blueprints ---
# This connects the routes defined in your other files to the main application.
# The `url_prefix` means all routes in `faq_bp` will start with `/faq`, etc.
app.register_blueprint(faq_bp, url_prefix="/faq")
app.register_blueprint(wellness_bp, url_prefix="/wellness")
print("Registered blueprints: /faq, /wellness")


# --- Step 6: Define the Root Route to Serve the Frontend ---
@app.route("/")
def home():
    """
    Serves the main HTML page of the application.
    """
    return render_template("index.html")


# --- Step 7: Run the Application ---
if __name__ == "__main__":
    # `debug=True` enables auto-reloading when you save changes.
    # Do not use debug mode in a production environment.
    # The host '0.0.0.0' makes the server accessible on your local network.
    print("Starting Flask development server...")
    app.run(host="0.0.0.0", port=5000, debug=True)
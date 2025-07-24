from flask import Flask, render_template
from flask_cors import CORS
from routes.faq_routes import faq_bp
from routes.wellness_routes import wellness_bp

app = Flask(__name__, static_url_path='/static')
CORS(app)  # Enable CORS for all routes

# Register Blueprints
app.register_blueprint(faq_bp, url_prefix="/faq")
app.register_blueprint(wellness_bp, url_prefix="/wellness")

# Serve Frontend
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

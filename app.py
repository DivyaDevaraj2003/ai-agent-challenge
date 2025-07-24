from flask import Flask
from routes.faq_routes import faq_bp
from routes.wellness_routes import wellness_bp

app = Flask(__name__)

app.register_blueprint(faq_bp, url_prefix="/faq")
app.register_blueprint(wellness_bp, url_prefix="/wellness")

@app.route("/")
def home():
    return "Welcome to AI Kyro Agent Platform. Visit /faq or /wellness."

if __name__ == "__main__":
    app.run(debug=True)

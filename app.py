from flask import Flask, render_template
from routes.faq_routes import faq_bp
from routes.wellness_routes import wellness_bp

app = Flask(__name__, static_url_path='/static')

# Register Blueprints
app.register_blueprint(faq_bp, url_prefix="/faq")
app.register_blueprint(wellness_bp, url_prefix="/wellness")

# Route to serve frontend UI
@app.route("/")
def home():
    return render_template("index.html")  # This will serve your chatbot interface

if __name__ == "__main__":
    app.run(debug=True)

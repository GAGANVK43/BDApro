"""
app.py - Main Flask Web Application & Vercel WSGI Entry Point
Netflix & Movie Big Data Analytics Platform
Architecture: Python, Flask, MongoDB Atlas, Hadoop HDFS, Apache Hive, Bootstrap 5, Chart.js
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify

# Load environment variables
load_dotenv()

# Setup Application
BASE_DIR = Path(__file__).resolve().parent
app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "netflix-big-data-secret-2026")
app.config["JSON_SORT_KEYS"] = False

# Register Blueprints
from api.routes import views_bp
from api.analytics_routes import api_bp

app.register_blueprint(views_bp)
app.register_blueprint(api_bp)


# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template("base.html", active_page="404", error_message="Page Not Found (404)"), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "Internal Server Error"}), 500


# Ensure cleaned dataset exists upon startup
def initialize_dataset():
    cleaned_file = BASE_DIR / "data" / "cleaned" / "netflix_cleaned.csv"
    if not cleaned_file.exists():
        try:
            from python.data_cleaning import run_data_cleaning_pipeline
            run_data_cleaning_pipeline()
        except Exception as e:
            print(f"[!] Warning: Could not auto-clean dataset on init: {str(e)}")


initialize_dataset()

# Local Development Server Runner
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    print("=" * 65)
    print("NETFLIX BIG DATA ANALYTICS WEB PLATFORM (FLASK)")
    print(f"[*] Starting local server at: http://127.0.0.1:{port}")
    print("=" * 65)
    app.run(host="0.0.0.0", port=port, debug=debug)

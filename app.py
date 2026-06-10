# import os
# from flask import Flask, jsonify, request, render_template
# from bs4 import BeautifulSoup
# import requests
# from urllib.parse import urljoin
# from chatbot import chatbot_bp
# from controller import Controller
# import onetimescript
# from db import db
# from PIL import Image
# from io import BytesIO
# import cv2
# import numpy as np
# import pytesseract
# from flask import Response
# import whois

# # Initialize Flask App
# app = Flask(__name__, static_folder="static")
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///domains.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable for performance

# # Initialize Database
# db.init_app(app)
# with app.app_context():
#     db.create_all()

# controller = Controller()

# # Register Blueprints AFTER Database Initialization
# app.register_blueprint(chatbot_bp, url_prefix="/chatbot")

# # Get API Key Securely (Warn if Missing Instead of Raising Error)
# API_KEY = os.getenv("NEWS_API_KEY")
# if not API_KEY:
#     print(
#         "⚠ Warning: NEWS_API_KEY not found. Cybersecurity news may not work.")

# CYBER_NEWS_API_URL = (
#     f"https://newsapi.org/v2/everything?q=cybersecurity+hacking+data+breach"
#     f"+cyber+attack&language=en&sortBy=publishedAt&apiKey={API_KEY}")

# # @app.route('/scan_progress')
# # def scan_progress():

# #     def generate():
# #         # This would be called at each step of your scanning process
# #         yield f"data: {time.time()} Starting scan...\n\n"
# #         # Add more yield statements for each step

# #     return Response(generate(), mimetype='text/event-stream')

# def get_latest_news():
#     """Fetch latest cybersecurity news from NewsAPI."""
#     try:
#         print(f"Fetching news from: {CYBER_NEWS_API_URL}")  # Debugging log
#         response = requests.get(CYBER_NEWS_API_URL)
#         response.raise_for_status()
#         data = response.json()

#         if "articles" in data:
#             return [{
#                 "title":
#                 article.get("title", "No Title"),
#                 "summary":
#                 article.get("description", "No description available"),
#                 "url":
#                 article.get("url", "#"),
#                 "published_at":
#                 article.get("publishedAt", "Unknown Date"),
#             } for article in data["articles"][:10]]

#         return [{
#             "title": "Error Fetching News",
#             "summary": "Unexpected API response",
#             "url": "#"
#         }]

#     except requests.exceptions.RequestException as e:
#         return [{
#             "title": "Error Fetching News",
#             "summary": f"API request failed: {e}",
#             "url": "#"
#         }]

# @app.route("/url_service", methods=["GET", "POST"])
# def url_service():
#     """Render the URL verification page and handle form submissions."""
#     output = {}
#     if request.method == "POST":
#         url = request.form.get("url")
#         if url:
#             try:
#                 result = controller.main(url)
#                 output = result
#             except Exception as e:
#                 output = {"error": str(e)}
#     return render_template("url_service.html", output=output)

# @app.route("/", methods=["GET", "POST"])
# def home():
#     """Homepage with URL checking."""
#     output = {}
#     if request.method == "POST":
#         url = request.form.get("url")
#         if url:
#             try:
#                 result = controller.main(url)
#                 output = result
#             except Exception as e:
#                 output = {"error": str(e)}
#     return render_template("index.html", output=output)

# @app.route("/preview", methods=["POST"])
# def preview():
#     """Preview the webpage by fetching and displaying its content."""
#     url = request.form.get("url")
#     if not url:
#         return "Error: No URL provided.", 400

#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, "html.parser")

#         for tag in soup.find_all(["link", "img"]):
#             attr = "href" if tag.name == "link" else "src"
#             if tag.get(attr):
#                 tag[attr] = urljoin(url, tag[attr])

#         return render_template("preview.html", content=soup.prettify())
#     except Exception as e:
#         return f"Error fetching webpage: {e}", 500

# @app.route("/source-code", methods=["POST"])
# def view_source_code():
#     """Fetch and display the source code of a given URL."""
#     url = request.form.get("url")
#     if not url:
#         return "Error: No URL provided.", 400

#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, "html.parser")

#         return render_template("source_code.html",
#                                formatted_html=soup.prettify(),
#                                url=url)
#     except Exception as e:
#         return f"Error fetching source code: {e}", 500

# @app.route("/update-db")
# def update_db():
#     """Update the database using the one-time script."""
#     try:
#         with app.app_context():
#             response = onetimescript.update_db()
#             print(" Database updated successfully!")
#             return response, 200
#     except Exception as e:
#         return f" Error updating database: {str(e)}", 500

# @app.route("/update-json")
# def update_json():
#     """Update the JSON file using the one-time script."""
#     try:
#         with app.app_context():
#             response = onetimescript.update_json()
#             print(" JSON updated successfully!")
#             return response, 200
#     except Exception as e:
#         return f" Error updating JSON: {str(e)}", 500

# @app.route("/newsletter")
# def newsletter():
#     """Render the newsletter page with cybersecurity news."""
#     news = get_latest_news()
#     return render_template("newsletter.html", news=news)

# @app.route("/api/news")
# def api_news():
#     """API endpoint for fetching cybersecurity news in JSON format."""
#     return jsonify(get_latest_news())

# @app.route("/about")
# def about():
#     """Render the About page."""
#     return render_template("about.html")

# @app.route("/extension")
# def extension():
#     """Render the extension page."""
#     return render_template("extension.html")

# @app.route("/chat")
# def chat():
#     """Render the Chatbot page."""
#     return render_template("chat.html")

# @app.route("/check_url", methods=["GET"])
# def check_url():
#     """Check the trust score of a given URL."""
#     url = request.args.get("url")
#     if not url:
#         return jsonify({"error": "No URL provided"}), 400

#     try:
#         result = controller.main(url)
#         return jsonify({"trust_score": result.get("trust_score", "N/A")})
#     except Exception as e:
#         return jsonify({"error": f"Error processing URL: {str(e)}"}), 500

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0")
import os
from flask import Flask, jsonify, request, render_template
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from chatbot import chatbot_bp
from controller import Controller
import onetimescript
from db import db
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
import pytesseract
from flask import Response
import whois

# Initialize Flask App
app = Flask(__name__, static_folder="static")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///domains.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Database
db.init_app(app)
with app.app_context():
    db.create_all()

controller = Controller()

# Register Blueprints AFTER Database Initialization
app.register_blueprint(chatbot_bp, url_prefix="/chatbot")

# Fetch News API Key
API_KEY = os.getenv("NEWS_API_KEY")
if not API_KEY:
    print(
        "⚠ Warning: NEWS_API_KEY not found. Cybersecurity news may not work.")

CYBER_NEWS_API_URL = (
    f"https://newsapi.org/v2/everything?q=cybersecurity+hacking+data+breach"
    f"+cyber+attack&language=en&sortBy=publishedAt&apiKey={API_KEY}")


def get_latest_news():
    """Fetch latest cybersecurity news."""
    try:
        response = requests.get(CYBER_NEWS_API_URL)
        response.raise_for_status()
        data = response.json()

        if "articles" in data:
            return [{
                "title":
                article.get("title", "No Title"),
                "summary":
                article.get("description", "No description available"),
                "url":
                article.get("url", "#"),
                "published_at":
                article.get("publishedAt", "Unknown Date"),
            } for article in data["articles"][:10]]

        return [{
            "title": "Error Fetching News",
            "summary": "Unexpected API response",
            "url": "#"
        }]

    except Exception as e:
        return [{
            "title": "Error Fetching News",
            "summary": str(e),
            "url": "#"
        }]


@app.route("/url_service", methods=["GET", "POST"])
def url_service():
    output = {}
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            try:
                output = controller.main(url)
            except Exception as e:
                output = {"error": str(e)}
    return render_template("url_service.html", output=output)


@app.route("/", methods=["GET", "POST"])
def home():
    output = {}
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            try:
                output = controller.main(url)
            except Exception as e:
                output = {"error": str(e)}
    return render_template("index.html", output=output)


@app.route("/preview", methods=["POST"])
def preview():
    url = request.form.get("url")
    if not url:
        return "Error: No URL provided.", 400

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        for tag in soup.find_all(["link", "img"]):
            attr = "href" if tag.name == "link" else "src"
            if tag.get(attr):
                tag[attr] = urljoin(url, tag[attr])

        return render_template("preview.html", content=soup.prettify())

    except Exception as e:
        return f"Error fetching webpage: {e}", 500


@app.route("/source-code", methods=["POST"])
def view_source_code():
    url = request.form.get("url")
    if not url:
        return "Error: No URL provided.", 400

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        return render_template("source_code.html",
                               formatted_html=soup.prettify(),
                               url=url)

    except Exception as e:
        return f"Error fetching source code: {e}", 500


@app.route("/update-db")
def update_db():
    try:
        with app.app_context():
            return onetimescript.update_db(), 200
    except Exception as e:
        return f"Error updating database: {str(e)}", 500


@app.route("/update-json")
def update_json():
    try:
        with app.app_context():
            return onetimescript.update_json(), 200
    except Exception as e:
        return f"Error updating JSON: {str(e)}", 500


@app.route("/newsletter")
def newsletter():
    news = get_latest_news()
    return render_template("newsletter.html", news=news)


@app.route("/api/news")
def api_news():
    return jsonify(get_latest_news())


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/extension")
def extension():
    return render_template("extension.html")


@app.route("/chat")
def chat():
    return render_template("chat.html")


# ------------------------------------------------------------
# 🔥 UPDATED: CHECK_URL RETURNS FULL RESULT JSON
# ------------------------------------------------------------
@app.route("/check_url", methods=["GET"])
def check_url():
    """Return full PhishNet scan result for Chrome Extension."""
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        result = controller.main(url)

        if not isinstance(result, dict):
            return jsonify({"result": result}), 200

        # Directly return full result without filtering anything
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

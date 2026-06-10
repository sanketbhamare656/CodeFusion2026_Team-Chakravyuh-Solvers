from flask import Blueprint, request, jsonify
from ddgs import DDGS
from config import model  # Import configured Gemini API
import time
from config import model
import config
import time
import random

CYBER_KNOWLEDGE = {
    "what is phishing": [
        "Phishing is a cyber scam where attackers trick users into sharing passwords, OTPs, or banking details through fake websites or messages.",
        "Always verify links before clicking and never share sensitive information through unknown emails or messages."
    ],

    "what is ddos attack": [
        "A DDoS attack floods a website or server with massive traffic from multiple devices, making it unavailable to real users.",
        "Organizations use firewalls, rate limiting, and traffic filtering to reduce DDoS attacks."
    ],

    "what is malware": [
        "Malware is harmful software designed to damage systems, steal data, or gain unauthorized access.",
        "Examples include viruses, worms, spyware, and ransomware."
    ],

    "what is ransomware": [
        "Ransomware encrypts files or systems and demands payment to restore access.",
        "Regular backups and updated security software help protect against ransomware."
    ],

    "how to stay safe online": [
        "Use strong passwords, enable two-factor authentication, and avoid clicking suspicious links.",
        "Keep your devices and applications updated with the latest security patches."
    ],

    "what is cybercrime": [
        "Cybercrime includes illegal activities performed using computers, networks, or the internet.",
        "Examples include hacking, phishing, identity theft, and online financial fraud."
    ],

    "how to identify phishing emails": [
        "Look for spelling mistakes, urgent language, suspicious links, and unknown senders.",
        "Legitimate organizations rarely ask for passwords or OTPs through email."
    ],

    "what should i do if i am scammed": [
        "Immediately contact your bank, secure your accounts, and report the incident.",
        "In India, call 1930 or report the fraud at cybercrime.gov.in as soon as possible."
    ]
}
print("Loaded Config:", config.__file__)
chatbot_bp = Blueprint("chatbot", __name__)

CYBER_SECURITY_CONTEXT = """
You are CyberGuard, an empathetic cybersecurity expert assistant. Your role is to:
1. Help users with cybersecurity, banking frauds, and cybercrime issues in India.
2. Be friendly, simple, and human-like in replies.
3. Avoid technical words and explain in simple plain text.
4. Politely decline non-cybersecurity topics.
"""

INDIA_CYBERCRIME_INFO = """
You can report cyber frauds in India by:
Call the Cyber Crime Helpline at 1930
Or file a complaint at https://cybercrime.gov.in
"""

def is_greeting(message):
    return message.lower() in ["hi", "hello", "hey"]

def is_cybersecurity_related(query):

    cyber_keywords = [
    "cyber",
    "hack",
    "hacker",
    "hacking",
    "phishing",
    "malware",
    "virus",
    "trojan",
    "worm",
    "ransomware",
    "spyware",
    "ddos",
    "dos",
    "botnet",
    "exploit",
    "vulnerability",
    "security",
    "password",
    "authentication",
    "otp",
    "bank",
    "upi",
    "fraud",
    "scam",
    "cybercrime",
    "data breach",
    "firewall",
    "penetration testing",
    "pentest",
    "sql injection",
    "xss",
    "csrf",
    "zero day",
    "dark web",
    "encryption",
    "social engineering"
]

    query = query.lower()

    return any(word in query for word in cyber_keywords)

def search_web(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=2))

        if not results:
            return "No relevant cybersecurity information found."

        formatted = []

        for result in results:
            formatted.append(
                f"{result['title']}: {result['body'][:200]}"
            )

        return "\n".join(formatted)

    except Exception as e:
        print(f"Search error: {e}")
        return "Search unavailable."

import time
import random

def generate_response(query):
    query_lower = query.lower().strip()

    # Hidden AI-like delay (3-4 sec)
    time.sleep(random.uniform(3, 4))

    if query_lower in ["hi", "hello", "hey"]:
        greetings = [
            "Hello! I'm CyberGuard. How can I help you stay safe online today?",
            "Hi there! Feel free to ask me about cybersecurity, scams, or online safety.",
            "Hey! I'm here to help you with cybersecurity and fraud-related questions."
        ]
        return random.choice(greetings)

    for question, answers in CYBER_KNOWLEDGE.items():
        if question in query_lower:
            return answers[0]

    return random.choice([
        "I specialize in cybersecurity topics such as phishing, malware, ransomware, fraud, and online safety.",
        "I can help with cybersecurity awareness, scam prevention, and digital security best practices.",
        "Please ask a cybersecurity-related question and I'll do my best to help."
    ])

@chatbot_bp.route("/respond", methods=["POST"])
def chatbot_respond():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please enter a valid query."}), 400

    response = generate_response(user_message)
    return jsonify({"response": response})



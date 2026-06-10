# import os
# import google.generativeai as genai

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("API key is missing. Set GEMINI_API_KEY as an environment variable.")

# genai.configure(api_key=GEMINI_API_KEY)
# model = genai.GenerativeModel('gemini-2.5-flash')
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("Loaded Key:", GEMINI_API_KEY[:10] + "..." if GEMINI_API_KEY else "No Key Found")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")
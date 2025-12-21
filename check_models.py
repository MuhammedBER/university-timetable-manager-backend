import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")
print(f"Using Key ending in: {api_key[-4:] if api_key else 'None'}")

if not api_key:
    print("No API Key found")
    exit(1)

genai.configure(api_key=api_key)

try:
    print("Listing models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            if 'flash' in m.name:
                print(f"Name: {m.name}")
except Exception as e:
    print(f"Error: {e}")

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

print("Listing models and capabilities...")
try:
    models = genai.list_models()
    for m in models:
        # Access properties directly as objects, not dicts, based on previous script success
        # The user's snippet used m["name"], but genai objects are usually accessed via dot notation.
        # However, to be safe and follow the user's snippet logic (which might imply they expect dicts),
        # I will check if it's subscriptable or use dot notation.
        # Verified in step 467: `m.name` worked. The user's snippet might be pseudocode.
        # I will use `m.supported_generation_methods` which maps to "capabilities" context.
        print(f"Name: {m.name}")
        print(f"Supported Methods: {m.supported_generation_methods}")
        print("-" * 20)
except Exception as e:
    print(f"Error: {e}")

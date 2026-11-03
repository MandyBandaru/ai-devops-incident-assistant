import os

api_key = os.getenv("AI_API_KEY")

if api_key:
    print("API key found successfully.")
else:
    print("API key not configured.")
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

print(f"My API KEY: {api_key}")

if not api_key:
    print("Error: API_KEY not found in .env")
    exit()
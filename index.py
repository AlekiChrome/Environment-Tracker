from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

# from dotenv import load_dotenv
# import os
# import google.generativeai as genai
# # import pandas as pd

# load_dotenv()

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_advice(prompt: str, model = "gemini-1.5-flash") -> str:
#     try:
#         response = genai.generate_content(
#             model = genai.GenerativeModel(model),
#             messages = [{"role": "user", "content": prompt}]
#         )
#         return response.candidates[0] ["content"]
#     except Exception as e:
#         return f"Sorry, an issue was encountered: {e}"
    
    
# def main():
#     print("Welcome to the Environmental Advisor!")
#     print("Ask me about sustainability, climate change, or eco-friendly practices.")
#     print("Type 'exit' to quit.\n")

#     while True:
#         user_input = input("You: ")

#         if user_input.lower() == "exit":
#             print("Goodbye, stay green!")
#             break

#         response = get_advice(user_input)
#         print(f"Advisor: {response}\n")

if __name__ == "__main__":
    app.run(debug = True)
    
        
import os
import json
from flask import Flask, render_template, jsonify, request, send_from_directory
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

app = Flask(__name__)

google_api_key = os.getenv("GOOGLE_API_KEY")

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/api/generate", methods=["POST"])
def generate_api():
    if request.method == "POST":
        try:
            req_body = request.get_json()
            content = req_body.get("contents")
            model = ChatGoogleGenerativeAI(model=req_body.get("model"))
            message = HumanMessage(
                content=content
            )
            response = model.stream([message])
            def stream():
                for chunk in response:
                    yield 'data: %s\n\n' % json.dumps({ "text": chunk.content })

            return stream(), {'Content-Type': 'text/event-stream'}

        except Exception as e:
            return jsonify({ "error": str(e) })
        
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)

if __name__ == "__main__":
    app.run(debug = True)
        
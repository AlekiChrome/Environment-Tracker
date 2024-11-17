import os
import json
from flask import Flask, render_template, jsonify, request, send_from_directory
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

app = Flask(__name__)

google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise EnvironmentError("GOOGLE_API_KEY not found")

search_history = []

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/api/generate", methods=["POST"])
def generate_api():
    if request.method == "POST":
        try:
            req_body = request.get_json()
            content = req_body.get("contents")
            
            if isinstance(content, list) and content:
                search_history.append(content[0].get("text", ""))
            
            model = ChatGoogleGenerativeAI(model = req_body.get("model"))
            message = HumanMessage(content = content)
            response = model.stream([message])
            def stream():
                for chunk in response:
                    yield 'data: %s\n\n' % json.dumps({ "text": chunk.content })

            return stream(), {'Content-Type': 'text/event-stream'}

        except Exception as e:
            return jsonify({ "error": str(e) }), 500
        
@app.route("/api/searches", methods=["GET"])
def get_previous_searches():
     return jsonify(search_history[-10:])

@app.route("/api/clear_searches", methods=["POST"])
def clear_searches():

    global search_history
    search_history = []
    return jsonify({"success": True, "message": "Search history cleared."})

        
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)

if __name__ == "__main__":
    app.run(debug = True)
        
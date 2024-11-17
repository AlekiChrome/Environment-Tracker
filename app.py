import json
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from database.models import Search, db

load_dotenv()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "database")
if not os.path.exists(db_path):
    os.makedirs(db_path)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(db_path, 'search_history.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()

google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise EnvironmentError("GOOGLE_API_KEY not found")

search_history = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def generate_api():
    if request.method == "POST":
        try:
            req_body = request.get_json()
            content = req_body.get("contents")

            if isinstance(content, list) and content:
                search_query = content[0].get("text", "")
                if search_query:
                    search_entry = Search(search_query=search_query)
                    db.session.add(search_entry)
                    db.session.commit()

                    searches = Search.query.all()
                    print("Database entries:")
                    for s in searches:
                        print(f"ID: {s.id}, Query: {s.query}")

            model = ChatGoogleGenerativeAI(model=req_body.get("model"))
            message = HumanMessage(content=content)
            response = model.stream([message])

            def stream():
                for chunk in response:
                    yield "data: %s\n\n" % json.dumps({"text": chunk.content})

            return stream(), {"Content-Type": "text/event-stream"}

        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/api/searches", methods=["GET"])
def get_previous_searches():
    searches = Search.query.order_by(Search.id.desc()).limit(10).all()
    return jsonify([search.search_query for search in searches])


@app.route("/api/clear_searches", methods=["POST"])
def clear_searches():

    global search_history
    search_history = []
    return jsonify({"success": True, "message": "Search history cleared."})


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("web", path)


if __name__ == "__main__":
    app.run(debug=True)

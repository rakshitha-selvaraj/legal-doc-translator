from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend running"

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]

    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return jsonify({"text": text})

@app.route("/simplify", methods=["POST"])
def simplify():
    data = request.json
    text = data.get("text")

    return jsonify({
        "clauses": [
            {
                "original": text,
                "simplified": "This means you agree to something important.",
                "risk": "medium"
            }
        ]
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pdfplumber

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ✅ PDF extraction function (inside same file)
def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print("Error:", e)
        return None

    return text.strip()


# ✅ Upload API
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    text = extract_text_from_pdf(file_path)

    if not text:
        return jsonify({"error": "Text extraction failed"}), 500

    return jsonify({"text": text})


# ✅ Dummy simplify API
@app.route("/simplify", methods=["POST"])
def simplify():
    data = request.json
    text = data.get("text", "")

    return jsonify({
        "simplified_text": "Simplified version will come here"
    })


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

TRANSLATION_API_URL = "http://127.0.0.1:5000/translate"  # Change this if hosted elsewhere

@app.route("/", methods=["GET", "POST"])
def home():
    translation = ""
    if request.method == "POST":
        text = request.form.get("text")
        if text:
            response = requests.post(TRANSLATION_API_URL, json={"text": text})
            if response.status_code == 200:
                translation = response.json().get("translated_text", "")
            else:
                translation = "Error in translation"
    return render_template("index.html", translation=translation)

if __name__ == "__main__":
    app.run(debug=True, port=8000)

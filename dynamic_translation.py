import transformers
import tensorflow as tf
from datasets import load_dataset
from transformers import AutoTokenizer, TFAutoModelForSeq2SeqLM
from flask import Flask, request, jsonify

# Load the model and tokenizer
model_checkpoint = "Davlan/byt5-base-eng-yor-mt"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = TFAutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)

def translate_text(text):
    """Translates English text to Yoruba using the model."""
    inputs = tokenizer(text, return_tensors="tf", padding=True, truncation=True)
    outputs = model.generate(**inputs)
    translated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return translated_text

# Flask app for serving the model
app = Flask(__name__)

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    translated_text = translate_text(text)
    return jsonify({"translated_text": translated_text})

if __name__ == "__main__":
    app.run(debug=True)
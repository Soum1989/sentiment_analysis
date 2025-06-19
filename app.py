from flask import Flask, request, render_template, send_from_directory
import pandas as pd
from transformers import pipeline
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Load sentiment analysis model
classifier = pipeline("sentiment-analysis", model="./model/models--distilbert--distilbert-base-uncased-finetuned-sst-2-english")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Read the file
            if filename.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif filename.endswith(".xlsx"):
                df = pd.read_excel(file_path)
            else:
                return "Unsupported file format"

            # Ensure there's a 'feedback' column
            if 'feedback' not in df.columns:
                return "The uploaded file must have a 'feedback' column."

            # Analyze sentiment
            sentiments = classifier(df["feedback"].astype(str).tolist())
            df["sentiment"] = [s["label"] for s in sentiments]

            # Save output
            base = os.path.splitext(filename)[0]
            csv_output = f"{base}_with_sentiment.csv"
            xlsx_output = f"{base}_with_sentiment.xlsx"
            csv_path = os.path.join(PROCESSED_FOLDER, csv_output)
            xlsx_path = os.path.join(PROCESSED_FOLDER, xlsx_output)

            df.to_csv(csv_path, index=False)
            df.to_excel(xlsx_path, index=False)

            return render_template("index.html", filename=base)

    return render_template("index.html")


@app.route("/download/<filename>")
def download(filename):
    csv_file = f"{filename}_with_sentiment.csv"
    xlsx_file = f"{filename}_with_sentiment.xlsx"
    return f"""
    <h2>Download Your Files</h2>
    <a href='/get-file/{csv_file}'>Download CSV</a><br>
    <a href='/get-file/{xlsx_file}'>Download XLSX</a>
    """

@app.route('/get-file/<filename>')
def get_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

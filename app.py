from flask import Flask, request, render_template, send_from_directory
import pandas as pd
from textblob import TextBlob
import os

app = Flask(__name__, static_folder='static')
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Read file
            if filename.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif filename.endswith(".xlsx"):
                df = pd.read_excel(file_path)
            else:
                return "Unsupported file format."

            # Check for feedback column
            if "feedback" not in df.columns:
                return "The uploaded file must have a 'feedback' column."

            # Perform sentiment analysis
            def get_sentiment(text):
                blob = TextBlob(str(text))
                polarity = blob.sentiment.polarity
                return "POSITIVE" if polarity > 0 else "NEGATIVE" if polarity < 0 else "NEUTRAL"

            df["sentiment"] = df["feedback"].apply(get_sentiment)

            # Save output
            base = os.path.splitext(filename)[0]
            csv_output = f"{base}_with_sentiment.csv"
            xlsx_output = f"{base}_with_sentiment.xlsx"
            df.to_csv(os.path.join(PROCESSED_FOLDER, csv_output), index=False)
            df.to_excel(os.path.join(PROCESSED_FOLDER, xlsx_output), index=False)

            return render_template("index.html", filename=base)

    return render_template("index.html")

@app.route("/download/<filename>")
def download(filename):
    return f"""
    <h2>Download Your Files</h2>
    <a href='/get-file/{filename}_with_sentiment.csv'>Download CSV</a><br>
    <a href='/get-file/{filename}_with_sentiment.xlsx'>Download XLSX</a>
    """

@app.route('/get-file/<filename>')
def get_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=False)


# 📊 Sentiment Analyzer Web App

A lightweight web application that performs **bulk sentiment analysis** on customer feedback from `.csv` or `.xlsx` files — and returns clear, downloadable insights in seconds.

![Preview](static/preview.png) <!-- Optional: replace or remove if not present -->

---

## 🔍 Use Case

Modern product teams, marketers, store managers, and analysts often deal with:
- Overwhelming customer feedback
- Time-consuming manual categorization
- No scalable way to measure customer sentiment

This app was designed to **simplify and scale feedback analysis**, whether from surveys, telephonic transcripts, or support conversations.

---

## 🚀 Features

- 📁 Upload raw feedback files (`.csv` or `.xlsx`)
- ⚡ Auto-analyze sentiment using TextBlob
- 📥 Download enriched files in both `.csv` and `.xlsx`
- 🧠 Instant visual clarity into customer emotions: `POSITIVE`, `NEGATIVE`, `NEUTRAL`

---

## 🧪 Live Demo

🌐 Try it here:  
**[https://sentiment-analysis-mrvu.onrender.com](https://sentiment-analysis-mrvu.onrender.com)**

---

## 🖥️ How to Run Locally

### 🔧 Requirements
- Python 3.10+
- pip

### 🐍 Set up your environment

```bash
git clone https://github.com/Soum1989/sentiment_analysis.git
cd sentiment_analysis
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python app.py

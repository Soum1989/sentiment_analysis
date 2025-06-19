import os
from transformers import pipeline

# Optional: silence symlink warning
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

def main():
    print("Loading sentiment analysis model...")
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    
    print("\n--- Sentiment Analyzer ---")
    print("Type a sentence and press Enter (or type 'exit' to quit):\n")

    while True:
        text = input("You: ")
        if text.lower().strip() == 'exit':
            print("Exiting sentiment analysis.")
            break

        result = classifier(text)[0]
        label = result['label']
        score = round(result['score'] * 100, 2)
        print(f"→ Sentiment: {label} ({score}%)\n")

if __name__ == "__main__":
    main()

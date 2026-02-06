from transformers import pipeline

# Load sentiment model once (important)
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


def get_sentiment_score(text):
    result = sentiment_model(text[:512])[0]

    if result["label"] == "NEGATIVE":
        return -result["score"]
    else:
        return result["score"]


def extract_features(transcript):
    turns = transcript["conversation"]

    full_text = " ".join([t["text"] for t in turns])
    customer_text = " ".join(
        [t["text"] for t in turns if t["speaker"] == "Customer"]
    )

    sentiment = get_sentiment_score(customer_text)

    features = {
        "sentiment_score": round(sentiment, 3),
        "is_negative": sentiment < -0.3,
        "escalation_requested": "supervisor" in customer_text.lower(),
        "repeated_issue_mentions": customer_text.lower().count("already"),
    }

    return features

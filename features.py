import os

_SENTIMENT_MODEL = None


def _get_sentiment_model():
    if os.getenv("SKIP_SENTIMENT", "0") == "1":
        return None

    global _SENTIMENT_MODEL
    if _SENTIMENT_MODEL is None:
        from transformers import pipeline
        _SENTIMENT_MODEL = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
        )
    return _SENTIMENT_MODEL


def get_sentiment_score(text):
    model = _get_sentiment_model()
    if model is None:
        return 0.0

    result = model(text[:512])[0]

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

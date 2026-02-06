# analytics.py

from collections import defaultdict
from features import extract_features


def compute_domain_stats(transcripts):
    domain_data = defaultdict(list)

    for t in transcripts:
        feats = t["features"]

        domain = t.get("domain", "Unknown")

        # ensure domain is hashable
        if isinstance(domain, list):
            domain = ", ".join(domain)

        domain_data[domain].append(feats)

    stats = {}

    for domain, feat_list in domain_data.items():
        total = len(feat_list)

        avg_sentiment = sum(f["sentiment_score"] for f in feat_list) / total

        escalation_rate = sum(
            f["escalation_requested"] for f in feat_list
        ) / total

        negative_rate = sum(
            f["is_negative"] for f in feat_list
        ) / total

        stats[domain] = {
            "total_calls": total,
            "avg_sentiment": round(avg_sentiment, 3),
            "escalation_rate": round(escalation_rate, 3),
            "negative_rate": round(negative_rate, 3),
        }

    return stats

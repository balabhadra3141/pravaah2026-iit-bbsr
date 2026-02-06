import json
from features import extract_features

def precompute_features(input_file, output_file):
    with open(input_file) as f:
        data = json.load(f)["transcripts"]

    enriched = []

    for t in data:
        feats = extract_features(t)
        t["features"] = feats
        enriched.append(t)

    with open(output_file, "w") as f:
        json.dump({"transcripts": enriched}, f, indent=2)


if __name__ == "__main__":
    precompute_features(
        "data/transcripts.json",
        "data/enriched_transcripts.json",
    )

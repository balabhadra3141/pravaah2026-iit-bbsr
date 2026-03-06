import argparse
from retriever import TranscriptRetriever


def main():
    parser = argparse.ArgumentParser(description="Precompute embeddings and FAISS index cache")
    parser.add_argument("--data", default="data/enriched_transcripts.json", help="Path to enriched transcripts JSON")
    parser.add_argument("--cache-dir", default="data", help="Directory to store cache files")
    args = parser.parse_args()

    print("Building embeddings and FAISS index cache...")
    _ = TranscriptRetriever(data_path=args.data, cache_dir=args.cache_dir)
    print("Done. Cache saved to:")
    print(f"  {args.cache_dir}/embeddings.npy")
    print(f"  {args.cache_dir}/faiss.index")
    print(f"  {args.cache_dir}/retriever_cache.json")


if __name__ == "__main__":
    main()

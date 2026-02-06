# retriever.py

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class TranscriptRetriever:
    def __init__(self, data_path="data/transcripts.json"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        with open(data_path, "r") as f:
            self.data = json.load(f)["transcripts"]

        self.texts = [self._flatten_transcript(t) for t in self.data]
        self.embeddings = self.model.encode(self.texts)

        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(self.embeddings))

    def _flatten_transcript(self, transcript):
        convo = " ".join(
            [f"{t['speaker']}: {t['text']}" for t in transcript["conversation"]]
        )
        return convo

    def search(self, query, k=3):
        query_vec = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_vec), k)

        results = [self.data[i] for i in indices[0]]
        call_ids = [r["transcript_id"] for r in results]

        return results, call_ids


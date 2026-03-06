import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class TranscriptRetriever:
    def __init__(self, data_path="data/enriched_transcripts.json", cache_dir="data"):
        self.model_name = "all-MiniLM-L6-v2"
        self.model = SentenceTransformer(self.model_name)

        with open(data_path, "r") as f:
            self.data = json.load(f)["transcripts"]

        self.texts = [self._flatten_transcript(t) for t in self.data]

        self._cache_meta_path = os.path.join(cache_dir, "retriever_cache.json")
        self._cache_embeddings_path = os.path.join(cache_dir, "embeddings.npy")
        self._cache_index_path = os.path.join(cache_dir, "faiss.index")

        if self._load_cache_if_valid(data_path):
            return

        self.embeddings = self.model.encode(self.texts)
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(self.embeddings))

        self._save_cache(data_path)

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

    def _load_cache_if_valid(self, data_path):
        if not (
            os.path.exists(self._cache_meta_path)
            and os.path.exists(self._cache_embeddings_path)
            and os.path.exists(self._cache_index_path)
        ):
            return False

        try:
            with open(self._cache_meta_path, "r") as f:
                meta = json.load(f)

            data_mtime = os.path.getmtime(data_path)
            data_size = os.path.getsize(data_path)

            if meta.get("model_name") != self.model_name:
                return False
            if meta.get("data_path") != data_path:
                return False
            if meta.get("data_mtime") != data_mtime:
                return False
            if meta.get("data_size") != data_size:
                return False
            if meta.get("text_count") != len(self.texts):
                return False

            self.embeddings = np.load(self._cache_embeddings_path)
            self.index = faiss.read_index(self._cache_index_path)

            if self.embeddings.shape[0] != len(self.texts):
                return False

            return True
        except Exception:
            return False

    def _save_cache(self, data_path):
        meta = {
            "model_name": self.model_name,
            "data_path": data_path,
            "data_mtime": os.path.getmtime(data_path),
            "data_size": os.path.getsize(data_path),
            "text_count": len(self.texts),
        }

        with open(self._cache_meta_path, "w") as f:
            json.dump(meta, f, indent=2)

        np.save(self._cache_embeddings_path, self.embeddings)
        faiss.write_index(self.index, self._cache_index_path)
    

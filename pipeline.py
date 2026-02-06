# pipeline.py

from retriever import TranscriptRetriever
from reasoning import ReasoningEngine
from features import extract_features
from analytics import compute_domain_stats
from memory import ConversationMemory


class CausalPipeline:
    def __init__(self):
        self.retriever = TranscriptRetriever()
        self.reasoner = ReasoningEngine()
        self.memory = ConversationMemory()

    def run_query(self, query, chat_history=""):

        # 1. Retrieve relevant transcripts
        retrieved, call_ids = self.retriever.search(query)
    
        # 2. Extract structured features
        feature_summary = []
    
        for t in retrieved:
            feats = extract_features(t)
            feature_summary.append({
                "id": t["transcript_id"],
                "features": feats
            })
    
        # 3. Compute domain statistics
        domain_stats = compute_domain_stats(retrieved)
    
        # 4. Get memory context
        chat_context = self.memory.get_chat_context()
    
        # 5. Generate explanation
        answer = self.reasoner.generate_explanation(
            query,
            retrieved,
            chat_context,
            feature_summary,
            domain_stats
        )
    
        # 6. Update memory
        self.memory.update(query, answer, call_ids)
    
        return answer


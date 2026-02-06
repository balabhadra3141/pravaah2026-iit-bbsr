import json
from retriever import TranscriptRetriever
from reasoning import ReasoningEngine
from analytics import compute_domain_stats
from memory import ConversationMemory
from causal import detect_causal_patterns


class CausalPipeline:
    def __init__(self):

        self.retriever = TranscriptRetriever()
        self.reasoner = ReasoningEngine()
        self.memory = ConversationMemory()

        with open("data/enriched_transcripts.json") as f:
            self.all_transcripts = json.load(f)["transcripts"]

        # compute once for speed
        self.domain_stats = compute_domain_stats(self.all_transcripts)

    def run_query(self, query):

        # Retrieve transcripts
        retrieved, call_ids = self.retriever.search(query)

        # Build causal evidence
        evidence_bundle = []

        for t in retrieved:
            patterns = detect_causal_patterns(t)

            evidence_bundle.append({
                "transcript_id": t["transcript_id"],
                "patterns": patterns,
                "features": t.get("features", {})
            })

        # Memory context
        chat_context = self.memory.get_chat_context()

        # Generate explanation (TEXT ONLY)
        answer = self.reasoner.generate_explanation(
            query=query,
            transcripts=retrieved,
            chat_history=chat_context,
            feature_summary=evidence_bundle,
            domain_stats=self.domain_stats
        )

        # Update memory
        self.memory.update(query, answer, call_ids)

        return answer

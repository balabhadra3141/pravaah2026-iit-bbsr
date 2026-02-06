class ConversationMemory:
    def __init__(self):
        # Store last few chat turns
        self.history = []

        # Track transcript IDs used (for evidence recall)
        self.used_call_ids = set()

    def update(self, query, answer, call_ids):
        """
        Save conversation turn and evidence IDs
        """

        self.history.append({
            "query": query,
            "answer": answer
        })

        # keep memory small (last 5 turns only)
        if len(self.history) > 5:
            self.history.pop(0)

        # track evidence IDs
        for cid in call_ids:
            self.used_call_ids.add(cid)

    def get_chat_context(self):
        """
        Convert memory into text context for LLM
        """

        context = ""

        for h in self.history:
            context += f"User: {h['query']}\n"
            context += f"System: {h['answer']}\n"

        return context

    def get_used_evidence(self):
        """
        Return previously used transcript IDs
        """

        return list(self.used_call_ids)

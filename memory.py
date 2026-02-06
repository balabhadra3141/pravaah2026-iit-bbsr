# memory.py

class ConversationMemory:
    def __init__(self):
        self.history = []
        self.used_call_ids = set()

    def update(self, query, answer, call_ids):
        self.history.append({
            "query": query,
            "answer": answer
        })

        for cid in call_ids:
            self.used_call_ids.add(cid)

    def get_chat_context(self):
        context = ""

        for h in self.history[-3:]:  # last 3 turns
            context += f"User: {h['query']}\n"
            context += f"System: {h['answer']}\n"

        return context

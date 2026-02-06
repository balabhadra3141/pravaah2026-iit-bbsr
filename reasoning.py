# reasoning.py

import requests


class ReasoningEngine:
    def __init__(self, model="phi3"):
        self.model = model

    def build_context(self, transcripts):

        context = ""

        for t in transcripts:
            convo = "\n".join(
                [f"{turn['speaker']}: {turn['text']}" for turn in t["conversation"]]
            )

            context += f"\nTranscript ID: {t['transcript_id']}\n{convo}\n"

        return context

    def generate_explanation(self, query, transcripts, chat_history="", feature_summary=None, domain_stats=None,):

        context = self.build_context(transcripts)
        allowed_ids = [t["transcript_id"] for t in transcripts]

        prompt = f"""
            You are a causal conversation analyst.
            
            IMPORTANT RULES:
            - Use ONLY the provided transcripts
            - Do NOT invent facts
            - Every claim must cite transcript ID and quote text
            
            User Question:
            {query}
            
            Previous Conversation Context:
            {chat_history}
            
            Feature Analysis:
            {feature_summary}
            
            Domain Statistics:
            {domain_stats}
            
            Transcripts:
            {context}
            
            Answer format:
            
            1. Key Causes: 
            2. Evidence (quote + transcript ID): 
            3. Explanation: 
            """

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 500,
                    "temperature": 0.2,
                },
            },
        )

        return response.json()["response"]


# 🔥 IMPORTANT: escaped JSON braces with {{ }}
#         prompt = f"""
# You are a causal conversation analyst.

# Allowed Transcript IDs:
# {allowed_ids}

# You MUST use only these IDs.

# Return ONLY valid JSON in this exact format:

# {{
#   "causes": [
#     {{
#       "cause": "...",
#       "evidence": {{
#         "transcript_id": "...",
#         "quote": "..."
#       }},
#       "explanation": "..."
#     }}
#   ],
#   "statistics_summary": "...",
#   "overall_conclusion": "..."
# }}

# Rules:
# - Use ONLY the provided transcripts
# - Every claim must cite transcript ID
# - Do NOT write text outside JSON

# User Question:
# {query}

# Previous Conversation Context:
# {chat_history}

# Causal Evidence Bundle:
# {feature_summary}

# Domain Statistics:
# {domain_stats}

# Transcripts:
# {context}
# """
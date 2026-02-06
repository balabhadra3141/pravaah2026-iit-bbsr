# // OFFLINE VIA LOCAL MODEL OLLAMA PHI3

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


# ------------------------------------------------------------

# #  // ONLINE VIA GEMINI API KEY

# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load API key from .env
# load_dotenv("apikey.env")
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# class ReasoningEngine:
#     def __init__(self, model="gemini-2.5-chat"):
#         self.model = model

#     # build_context should only include summaries, not full conversation
#     def build_context(self, transcripts):
#         context = ""
#         for t in transcripts:
#             # only include relevant extracted patterns
#             key_points = ", ".join([p['summary'] for p in t.get('patterns', [])])
#             context += f"Transcript ID: {t['transcript_id']} — {key_points}\n"
#         return context


#     def generate_explanation(
#         self,
#         query,
#         transcripts,
#         chat_history="",
#         feature_summary=None,
#         domain_stats=None,
#     ):
#         context = self.build_context(transcripts)

#         prompt = f"""
# You are a causal conversation analyst.

# Evidence Summaries:
# {context}

# User Question: {query}

# Instructions:
# - List key causes.
# - Reference transcript IDs as evidence.
# - Provide short explanations.
# - Give percentages if possible.
# """

#         # Correct API call for Gemini Chat
#         response = genai.chat.Completion.create(
#             model=self.model,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.3,
#             max_output_tokens=1000,
#         )

#         return response.choices[0].content[0].text

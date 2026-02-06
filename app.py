# app.py

import streamlit as st
from pipeline import CausalPipeline

st.title("Causal Conversation Analyzer")

# Initialize pipeline once (persistent chatbot memory)
if "pipeline" not in st.session_state:
    st.session_state.pipeline = CausalPipeline()

# Store chat messages for display
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input
query = st.text_input("Ask an analytical question:")

if st.button("Analyze") and query:

    # Run pipeline (memory handled internally)
    response = st.session_state.pipeline.run_query(query)

    # Save messages for UI display
    st.session_state.messages.append(("User", query))
    st.session_state.messages.append(("System", response))

# Display chat history
for role, msg in st.session_state.messages:
    if role == "User":
        st.write(f"**You:** {msg}")
    else:
        st.write(f"**System:** {msg}")

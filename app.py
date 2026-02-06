import streamlit as st
from pipeline import CausalPipeline

st.set_page_config(page_title="Causal Conversation Analyzer")
st.title("🧠 Causal Conversation Analyzer")

# Clear old tuples in session state (only once)
if "messages" in st.session_state:
    # Keep only dict-type messages or start fresh
    st.session_state.messages = [
        msg for msg in st.session_state.messages if isinstance(msg, dict)
    ]
else:
    st.session_state.messages = []

# Initialize pipeline (persistent memory)
if "pipeline" not in st.session_state:
    st.session_state.pipeline = CausalPipeline()

# Display existing chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
query = st.chat_input("Ask an analytical question...")

if query:
    # Save and display user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing transcripts..."):
            response = st.session_state.pipeline.run_query(query)

        st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})

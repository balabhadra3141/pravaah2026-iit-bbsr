# # # app.py

# # import streamlit as st
# # from pipeline import CausalPipeline

# # st.set_page_config(page_title="Causal Conversation Analyzer")

# # st.title("Causal Conversation Analyzer")

# # # Initialize pipeline once
# # if "pipeline" not in st.session_state:
# #     st.session_state.pipeline = CausalPipeline()

# # # Store chat messages
# # if "messages" not in st.session_state:
# #     st.session_state.messages = []

# # # Chat input
# # query = st.text_input("Ask an analytical question:")

# # if st.button("Analyze") and query:

# #     with st.spinner("Analyzing conversations..."):
# #         response = st.session_state.pipeline.run_query(query)

# #     st.session_state.messages.append(("User", query))
# #     st.session_state.messages.append(("System", response))

# # # Display chat history
# # for role, msg in st.session_state.messages:

# #     if role == "User":
# #         st.markdown(f"**You:** {msg}")

# #     else:
# #         st.markdown("**System Response:**")
# #         st.markdown(msg)   # <-- renders formatted text cleanly
# #         st.divider()



# # app.py

# import streamlit as st
# from pipeline import CausalPipeline

# st.set_page_config(page_title="Causal Conversation Analyzer")
# st.title("Causal Conversation Analyzer")

# # Initialize pipeline once
# if "pipeline" not in st.session_state:
#     st.session_state.pipeline = CausalPipeline()

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # --- Form for user input ---
# with st.form(key="query_form"):
#     query = st.text_input("Type your analytical question here:", key="query_input")
#     submit = st.form_submit_button("Analyze")

#     if submit and query:
#         with st.spinner("Analyzing conversations..."):
#             response = st.session_state.pipeline.run_query(query)

#         st.session_state.messages.append(("User", query))
#         st.session_state.messages.append(("System", response))

#         # ✅ DO NOT reset query_input manually
#         # st.session_state.query_input = ""  <-- remove this

# # --- Display chat history ---
# for role, msg in st.session_state.messages:
#     if role == "User":
#         st.markdown(f"**You:** {msg}")
#     else:
#         st.markdown("**System Response:**")
#         st.markdown(msg)
#     st.divider()


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

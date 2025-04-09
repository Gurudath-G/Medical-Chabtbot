import streamlit as st
from rag_pipeline import answer_query, retrieve_docs, llm_model
import re

st.title("💬 AI Chatbot")

# User input
user_query = st.text_area("Enter your prompt:", height=150, placeholder="Ask Anything!")

# Buttons
ask_question = st.button("Ask AI")
#show_thinking = st.button("Show Thinking Process")

# Initialize variables
cleaned_content = ""
think_content = "No thinking process available."

if ask_question and user_query:
    st.chat_message("user").write(user_query)

    # Retrieve documents and get response
    retrieved_docs = retrieve_docs(user_query)
    response = answer_query(documents=retrieved_docs, model=llm_model, query=user_query)
    content = response.content

    # Extract and clean content
    cleaned_content = re.sub(r"<think>.*?</think>\n\n", "", content, flags=re.DOTALL)
    think_content_match = re.search(r"<think>([\s\S]*?)</think>", content)
    if think_content_match:
        think_content = think_content_match.group(1)

    st.chat_message("AI").write(cleaned_content)

# Display the thinking process if the button is clicked
#if show_thinking and user_query:
    #st.subheader("🤔 Thinking Process")
    #st.write(think_content)

import os
import streamlit as st
import anthropic

with st.sidebar:
    anthropic_api_key = st.text_input("Anthropic API Key", key="chatbot_api_key", type="password")
#"[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
#"[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    #streamlit UI
st.title("Mind Craft 🧠")
st.write("Welcome to Mind Craft! This is your personalized learnig journey. Craft your learning to your mind!")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not anthropic_api_key:
        st.info("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")
        st.stop()

    client = anthropic(api_key=anthropic_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(
    prompt = prompt,
    stop_sequences=[anthropic.HUMAN_PROMPT],
    model="claude-2.1", messages=st.session_state.messages,
    max_tokens_to_sample=1000)
    msg = response.choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    
    st.write ("### Answer")
    st.write(response.completion)
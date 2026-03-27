import streamlit as st
import requests

# API key safely from secrets
API_KEY = st.secrets.get("OPENROUTER_API_KEY", "")

URL = "https://openrouter.ai/api/v1/chat/completions"

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🚀 CrazyCozy AI Chatbot")

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# show old messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# input
user_input = st.chat_input("Type your message...")

if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
    {"role": "system", "content": "You are CrazyCozy AI, a smart, friendly and professional assistant. Give clear, helpful and confident answers."}
] + st.session_state.messages[-5:]
    }

    try:
        with st.spinner("🤖 Thinking..."):
    response = requests.post(URL, headers=headers, json=data)
        result = response.json()

        if "choices" in result:
            reply = result["choices"][0]["message"]["content"]
        else:
            reply = "⚠️ Something went wrong"

    except:
        reply = "⚠️ API Error"

    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

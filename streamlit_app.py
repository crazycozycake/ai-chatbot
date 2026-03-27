import streamlit as st
import requests

# API KEY
API_KEY = st.secrets["OPENROUTER_API_KEY"]

URL = "https://openrouter.ai/api/v1/chat/completions"

# PAGE CONFIG
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🚀 CrazyCozy AI Chatbot")

# CLEAR CHAT BUTTON
if st.button("🗑 Clear Chat"):
    st.session_state.messages = []

# SESSION INIT
if "messages" not in st.session_state:
    st.session_state.messages = []

# SHOW CHAT HISTORY
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# USER INPUT
user_input = st.chat_input("Type your message...")

if user_input:
    # SHOW USER MESSAGE
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # API HEADERS
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # DATA WITH PERSONALITY
    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are CrazyCozy AI, a smart, friendly and professional assistant. Give clear and helpful answers."
            }
        ] + st.session_state.messages[-5:]
    }

    # API CALL + ERROR HANDLING
    try:
        with st.spinner("🤖 Thinking..."):
            response = requests.post(URL, headers=headers, json=data)
            result = response.json()

        if "choices" in result:
            reply = result["choices"][0]["message"]["content"]
        else:
            reply = "⚠️ Server busy, try again."

    except:
        reply = "⚠️ Network error. Please check your connection."

    # SHOW BOT MESSAGE
    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

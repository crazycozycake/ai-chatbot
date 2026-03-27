import streamlit as st
import requests

# API KEY
API_KEY = st.secrets["OPENROUTER_API_KEY"]
URL = "https://openrouter.ai/api/v1/chat/completions"

# PAGE CONFIG
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🚀 CrazyCozy AI Chatbot")

# -------------------- MULTI CHAT SYSTEM --------------------

if "all_chats" not in st.session_state:
    st.session_state.all_chats = [[]]

if "current_chat" not in st.session_state:
    st.session_state.current_chat = 0

# -------------------- SIDEBAR --------------------

st.sidebar.title("💬 Chat History")

for i, chat in enumerate(st.session_state.all_chats):
    label = f"Chat {i+1}"

    # Highlight current chat
    if i == st.session_state.current_chat:
        label = "👉 " + label

    if st.sidebar.button(label):
        st.session_state.current_chat = i

# -------------------- BUTTONS --------------------

col1, col2 = st.columns(2)

# New Chat
with col1:
    if st.button("➕ New Chat"):
        st.session_state.all_chats.append([])
        st.session_state.current_chat = len(st.session_state.all_chats) - 1

# Clear Current Chat
with col2:
    if st.button("🗑 Clear Chat"):
        st.session_state.all_chats[st.session_state.current_chat] = []

# -------------------- CURRENT CHAT --------------------

messages = st.session_state.all_chats[st.session_state.current_chat]

# -------------------- DISPLAY CHAT --------------------

for msg in messages:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------- USER INPUT --------------------

user_input = st.chat_input("Type your message...")

if user_input:
    st.chat_message("user").write(user_input)
    messages.append({"role": "user", "content": user_input})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are CrazyCozy AI, a smart, friendly and professional assistant."
            }
        ] + messages[-5:]
    }

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

    st.chat_message("assistant").write(reply)
    messages.append({"role": "assistant", "content": reply})

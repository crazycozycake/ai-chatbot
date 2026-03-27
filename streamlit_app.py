import streamlit as st
import requests

# API KEY
API_KEY = st.secrets["OPENROUTER_API_KEY"]
URL = "https://openrouter.ai/api/v1/chat/completions"

# PAGE CONFIG
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🚀 CrazyCozy AI Chatbot")

# -------------------- INIT --------------------

if "all_chats" not in st.session_state:
    st.session_state.all_chats = [{"title": "New Chat", "messages": []}]

if "current_chat" not in st.session_state:
    st.session_state.current_chat = 0

# -------------------- FIX OLD DATA --------------------

for i, chat in enumerate(st.session_state.all_chats):
    if isinstance(chat, list):  # old format fix
        st.session_state.all_chats[i] = {
            "title": "Old Chat",
            "messages": chat
        }

# -------------------- SIDEBAR --------------------

st.sidebar.title("💬 Chat History")

for i, chat in enumerate(st.session_state.all_chats):
    label = chat["title"]

    if i == st.session_state.current_chat:
        label = "👉 " + label

    if st.sidebar.button(label, key=f"chat_{i}"):
        st.session_state.current_chat = i

# -------------------- BUTTONS --------------------

col1, col2 = st.columns(2)

# New Chat
with col1:
    if st.button("➕ New Chat"):
        st.session_state.all_chats.append({
            "title": "New Chat",
            "messages": []
        })
        st.session_state.current_chat = len(st.session_state.all_chats) - 1

# Clear Chat
with col2:
    if st.button("🗑 Clear Chat"):
        st.session_state.all_chats[st.session_state.current_chat]["messages"] = []

# -------------------- CURRENT CHAT --------------------

current = st.session_state.all_chats[st.session_state.current_chat]
messages = current["messages"]

# -------------------- EDIT TITLE --------------------

new_title = st.text_input("✏️ Edit Chat Title", value=current["title"])

if new_title:
    current["title"] = new_title

# -------------------- DISPLAY CHAT --------------------

for msg in messages:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------- USER INPUT --------------------

user_input = st.chat_input("Type your message...")

if user_input:
    st.chat_message("user").write(user_input)
    messages.append({"role": "user", "content": user_input})

    # Auto title from first message
    if current["title"] == "New Chat":
        current["title"] = user_input[:20]

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

import streamlit as st
import requests
import speech_recognition as sr

# ---------------- CONFIG ----------------

API_KEY = st.secrets["OPENROUTER_API_KEY"]
URL = "https://openrouter.ai/api/v1/chat/completions"

st.set_page_config(page_title="CrazyCozy AI", page_icon="🤖")

# ---------------- INIT ----------------

if "all_chats" not in st.session_state:
    st.session_state.all_chats = [
        {"title": "New Chat", "messages": []}
    ]

if "current_chat" not in st.session_state:
    st.session_state.current_chat = 0

# ---------------- SAFETY FIX ----------------

if len(st.session_state.all_chats) == 0:
    st.session_state.all_chats.append({
        "title": "New Chat",
        "messages": []
    })
    st.session_state.current_chat = 0

if st.session_state.current_chat >= len(st.session_state.all_chats):
    st.session_state.current_chat = max(0, len(st.session_state.all_chats) - 1)

current = st.session_state.all_chats[st.session_state.current_chat]

# ---------------- SIDEBAR ----------------

st.sidebar.title("💬 Chat History")

# Edit title
new_title = st.sidebar.text_input(
    "✏️ Edit Title",
    value=current["title"],
    key=f"title_{st.session_state.current_chat}"
)

if new_title:
    current["title"] = new_title

st.sidebar.markdown("---")

# Chat list + delete
for i, chat in enumerate(st.session_state.all_chats):
    col1, col2 = st.sidebar.columns([4, 1])

    label = chat["title"]
    if i == st.session_state.current_chat:
        label = "👉 " + label

    if col1.button(label, key=f"open_{i}"):
        st.session_state.current_chat = i
        st.rerun()

    if col2.button("❌", key=f"del_{i}"):
        st.session_state.all_chats.pop(i)

        if len(st.session_state.all_chats) == 0:
            st.session_state.all_chats.append({
                "title": "New Chat",
                "messages": []
            })
            st.session_state.current_chat = 0
        else:
            st.session_state.current_chat = max(0, i - 1)

        st.rerun()

# Buttons
st.sidebar.markdown("---")

if st.sidebar.button("➕ New Chat"):
    st.session_state.all_chats.append({
        "title": "New Chat",
        "messages": []
    })
    st.session_state.current_chat = len(st.session_state.all_chats) - 1
    st.rerun()

if st.sidebar.button("🗑 Clear Chat"):
    current["messages"] = []
    st.rerun()

# ---------------- DISPLAY CHAT ----------------

messages = current["messages"]

for msg in messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------------- 🎤 VOICE INPUT ----------------

st.markdown("### 🎤 Voice Input")

audio_file = st.file_uploader("Upload voice (wav/mp3/m4a)", type=["wav", "mp3", "m4a"])

voice_text = ""

if audio_file is not None:
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            voice_text = recognizer.recognize_google(audio_data)

        st.success(f"🗣 You said: {voice_text}")

    except:
        st.error("⚠️ Could not understand audio")

# ---------------- INPUT ----------------

typed_input = st.chat_input("Type your message...")

user_input = typed_input if typed_input else voice_text

# ---------------- CHAT LOGIC ----------------

if user_input:
    st.chat_message("user").write(user_input)
    messages.append({"role": "user", "content": user_input})

    # Auto title
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
                "content": "You are CrazyCozy AI, a smart, friendly and helpful assistant."
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

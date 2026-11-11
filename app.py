import streamlit as st
import google.generativeai as genai
from audio_recorder_streamlit import audio_recorder
import io

st.set_page_config(page_title="PocketSaathi", page_icon="🤖")

st.title("🤖 PocketSaathi AI Assistant (Gemini)")
st.write("सवाल पूछें और बिना किसी रुकावट के मुफ्त में बातचीत करें!")

# Sidebar - Gemini API Key input
api_key = st.sidebar.text_input("Google Gemini API Key", type="password")

if not api_key:
    st.info("👈 शुरुआत करने के लिए कृपया साइडबार में अपनी Google Gemini API Key दर्ज करें (यह बिल्कुल मुफ्त है)।")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")


# Session state initialization for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Chat Input
user_input = st.chat_input("अपना सवाल यहाँ लिखें...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("PocketSaathi सोच रहा है..."):
            try:
                # Convert history for Gemini format
                chat_history = [
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ]
                chat = model.start_chat(history=chat_history)
                response = chat.send_message(user_input)
                bot_reply = response.text
                
                st.write(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"जवाब देने में दिक्कत आई: {e}")
                
    
                    
            
            
            

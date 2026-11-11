import streamlit as st
from groq import Groq
from audio_recorder_streamlit import audio_recorder
import io

st.set_page_config(page_title="PocketSaathi", page_icon="🤖")

st.title("🤖 PocketSaathi AI Assistant (Meta Llama)")
st.write("सवाल पूछें और बिना एक भी पैसा दिए बिल्कुल मुफ्त में बातचीत करें!")

# Sidebar - Groq API Key input
api_key = st.sidebar.text_input("Groq API Key (Free)", type="password")

if not api_key:
    st.info("👈 शुरुआत करने के लिए कृपया साइडबार में अपनी मुफ्त Groq API Key दर्ज करें (console.groq.com से बिल्कुल मुफ्त मिलती है)।")
    st.stop()

client = Groq(api_key=api_key)

# Session state initialization
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
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )
                bot_reply = response.choices[0].message.content
                st.write(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"जवाब देने में दिक्कत आई: {e}")
                
                
    
                    
            
            
            

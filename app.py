import streamlit as st
from groq import Groq

st.set_page_config(page_title="PocketSaathi", page_icon="🤖")

st.title("PocketSaathi AI Assistant")
st.write("Ask questions and chat for free!")

# Sidebar - Groq API Key input
api_key = st.sidebar.text_input("Groq API Key", type="password")

if not api_key:
    st.info("Please enter your free Groq API Key in the sidebar to start.")
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
user_input = st.chat_input("Type your question here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("PocketSaathi is thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )
                bot_reply = response.choices[0].message.content
                st.write(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"Error: {e}")
                
                
                
    
                    
            
            
            

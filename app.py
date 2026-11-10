import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import os

# --- 1. पेज सेटअप ---
st.set_page_config(
    page_title="PocketSaathi - आपका AI साथी",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 PocketSaathi AI")
st.subheader("आपका अपना AI असिस्टेंट और फाइनेंस मैनेजर")

# --- 2. AI सेटिंग्स (Gemini API) ---
st.sidebar.title("⚙️ AI सेटिंग्स")
api_key = st.sidebar.text_input("अपनी Gemini API Key यहाँ डालें:", type="password")

# --- 3. ऐप के मुख्य फीचर्स (नेविगेशन) ---
menu = st.sidebar.radio("मेन्यू चुनें", ["💬 AI चैट (सवाल-जवाब)", "💰 पॉकेट फाइनेंस ट्रैकर"])

if menu == "💬 AI चैट (सवाल-जवाब)":
    st.header("💬 AI से कुछ भी पूछें")
    st.write("चाहे कोई सवाल हो, सलाह चाहिए हो या फोटो/डिजाइन का आइडिया चाहिए हो!")

    if not api_key:
        st.warning("⚠️ कृपया बाईं तरफ (Sidebar) अपनी Gemini API Key डालें ताकि AI काम कर सके।")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            

            # चैट हिस्ट्री
            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # यूजर का इनपुट
            if prompt := st.chat_input("यहाँ अपना सवाल लिखें या बोलकर टाइप करें..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

        except Exception as e:
            st.error(f"कुछ समस्या आई: {e}")

elif menu == "💰 पॉकेट फाइनेंस ट्रैकर":
    st.header("📊 आपका वित्तीय विवरण")
    st.info("यहाँ आपका पुराना बजट और खर्च ट्रैकर सुरक्षित है!")
    st.metric(label="वर्तमान शेष राशि (Balance)", value="₹ 0.00")
    st.metric(label="बचत का लक्ष्य", value="₹ 0.00")
    

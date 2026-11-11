import streamlit as st
from groq import Groq

# APP CONFIGURATION
st.set_page_config(
    page_title="Pocket Sathi",
    page_icon="🤖",
    layout="centered"
)

# APP DESIGN
st.title("🤖 Pocket Sathi")
st.caption("आपका अपना AI सवाल-जवाब साथी")

st.divider()

# API KEY
api_key = ""

try:
    api_key = st.secrets.get("GROQ_API_KEY", "")
except Exception:
    pass

if not api_key:
    api_key = st.sidebar.text_input(
        "Groq API Key",
        type="password"
    )

# SESSION MEMORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# SYSTEM PERSONALITY
system_message = {
    "role": "system",
    "content": """
    तुम Pocket Sathi हो।

    तुम एक बुद्धिमान और मददगार AI सहायक हो।

    तुम्हारा काम:
    1. हिंदी में अच्छे जवाब देना।
    2. अंग्रेजी में भी जवाब देना।
    3. विज्ञान और तकनीक समझाना।
    4. पढ़ाई में मदद करना।
    5. सामान्य ज्ञान के सवाल हल करना।
    6. यूजर के सवाल ध्यान से समझना।
    7. आसान भाषा में जवाब देना।
    8. बातचीत का संदर्भ याद रखना।

    हमेशा विनम्र और उपयोगी जवाब दो।
    """
}

# SHOW OLD MESSAGES
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# CHAT INPUT
question = st.chat_input(
    "Pocket Sathi से कुछ भी पूछें...",
    disabled=not bool(api_key)
)

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Pocket Sathi सोच रहा है..."):

            try:

                client = Groq(api_key=api_key)

                response = client.chat.completions.create(

                    model="llama-3.3-70b-versatile",

                    messages=[
                        system_message
                    ] + st.session_state.messages[-20:],

                )

                answer = response.choices[0].message.content

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:

                st.error(
                    "जवाब प्राप्त करने में समस्या आई। "
                    "API Key और इंटरनेट जाँचें।"
                )

                st.caption(str(e))

# NEW CHAT
st.divider()

if st.button("🗑️ नई बातचीत"):

    st.session_state.messages = []

    st.rerun()

st.caption("Pocket Sathi AI | आपका अपना साथी")
                
                
                
    
                    
            
            
            

import streamlit as st

st.set_page_config(
    page_title="Pocket Sathi",
    page_icon="🤖",
    layout="centered"
)

# DESIGN
st.markdown("""
<style>
.stApp {
    background: #f5f7ff;
}

.block-container {
    max-width: 750px;
    padding-top: 1rem;
    padding-bottom: 5rem;
}

.header {
    background: linear-gradient(135deg,#5146e5,#8875ff);
    padding: 25px 18px;
    border-radius: 22px;
    color: white;
    text-align: center;
    margin-bottom: 22px;
}

.header h1 {
    color: white;
    font-size: 32px;
    margin: 0;
}

.header p {
    color: white;
    margin-top: 8px;
}

.card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    margin: 12px 0;
    border: 1px solid #e6e8f5;
}

.welcome {
    text-align: center;
    padding: 25px 10px;
}

.welcome h2 {
    color: #3730a3;
}

.stButton button {
    border-radius: 12px;
    min-height: 45px;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# SESSION
if "messages" not in st.session_state:
    st.session_state.messages = []

if "started" not in st.session_state:
    st.session_state.started = False


# SIDEBAR
with st.sidebar:
    st.title("🤖 Pocket Sathi")
    st.caption("आपका अपना AI साथी")

    st.divider()

    if st.button("＋ नई बातचीत", use_container_width=True):
        st.session_state.messages = []
        st.session_state.started = False
        st.rerun()

    st.divider()

    st.subheader("⚙️ सेटिंग")
    st.write("भाषा: हिंदी")
    st.write("AI कनेक्शन: जल्द आएगा")
    st.write("माइक: जल्द आएगा")

    st.divider()
    st.caption("Pocket Sathi Version 1.0")


# HEADER
st.markdown("""
<div class="header">
    <h1>🤖 Pocket Sathi</h1>
    <p>आपका अपना स्मार्ट सवाल-जवाब साथी</p>
</div>
""", unsafe_allow_html=True)


# WELCOME SCREEN
if not st.session_state.messages:

    st.markdown("""
    <div class="welcome">
        <h2>नमस्ते! 👋</h2>
        <p>मैं आपका Pocket Sathi हूँ।</p>
        <p>जल्द ही यहाँ आप मुझसे बातें कर सकेंगे।</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✨ आप क्या पूछना चाहेंगे?")

    suggestions = [
        "सामान्य ज्ञान",
        "विज्ञान और तकनीक",
        "पढ़ाई से जुड़े सवाल",
        "नई जानकारी"
    ]

    for item in suggestions:
        st.markdown(
            f'<div class="card">💡 {item}</div>',
            unsafe_allow_html=True
        )


# CHAT HISTORY
else:

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


# CHAT INPUT
question = st.chat_input(
    "Pocket Sathi से कुछ पूछें..."
)

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            "आपका सवाल प्राप्त हो गया है। "
            "मेरा AI दिमाग अभी जोड़ा नहीं गया है। "
            "जल्द ही मैं आपके सवालों के जवाब दे सकूँगा।"
        )
    })

    st.rerun()


# BOTTOM
st.divider()

st.markdown("""
<div style="text-align:center; color:#777;">
    🤖 Pocket Sathi<br>
    आपका अपना साथी ❤️
</div>
""", unsafe_allow_html=True)

2. requirements.txt

इसमें अभी केवल यह रखो:

streamlit

अभी Groq की जरूरत नहीं है क्योंकि हमने AI कनेक्शन बाद के लिए रखा है।

3. अब क्या करना है?

1. GitHub में "app.py" खोलो।
2. Edit दबाओ।
3. पूरा पुराना कोड हटाओ।
4. ऊपर वाला नया कोड डालो।
5. Commit changes करके सेव करो।
6. Streamlit ऐप खोलकर Refresh करो।

एक जरूरी बात

अभी यह Streamlit पर चलने वाला ऐप जैसा इंटरफेस होगा, असली Android APK नहीं। बाद में इसे मोबाइल की Home Screen पर भी जोड़ा जा सकता है।

हमारा पहला लक्ष्य है कि Pocket Sathi मोबाइल में एक सुंदर, अपना ऐप जैसा दिखाई दे। उसके बाद इसमें असली AI का दिमाग जोड़ेंगे। ❤️
                
                
                
    
                    
            
            
            

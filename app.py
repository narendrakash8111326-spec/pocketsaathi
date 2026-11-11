import streamlit as st

st.set_page_config(
    page_title="Pocket Sathi",
    page_icon="🤖",
    layout="centered"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("""
<style>
.stApp {
    background: #f4f5ff;
}
.block-container {
    max-width: 700px;
    padding-top: 25px;
}
.header {
    background: linear-gradient(135deg,#4236c9,#9178ff);
    padding: 25px;
    border-radius: 22px;
    text-align: center;
    color: white;
}
.header h1 {
    color: white;
    font-size: 32px;
}
.card {
    background: white;
    padding: 18px;
    border-radius: 16px;
    margin: 12px 0;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🤖 Pocket Sathi")
    st.write("आपका अपना साथी")

    if st.button("＋ नई बातचीत"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.subheader("⚙️ सेटिंग")
    st.write("भाषा: हिंदी")
    st.write("AI: जल्द आएगा")
    st.write("माइक: जल्द आएगा")

st.markdown("""
<div class="header">
<h1>🤖 Pocket Sathi</h1>
<p>आपका अपना स्मार्ट साथी</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="card">
    <h2>नमस्ते! 👋</h2>
    <p>मैं आपका Pocket Sathi हूँ।</p>
    <p>आप मुझसे कुछ भी पूछ सकते हैं।</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("✨ आप क्या जानना चाहते हैं?")

    st.markdown("""
    <div class="card">📚 पढ़ाई और सामान्य ज्ञान</div>
    <div class="card">🔬 विज्ञान और तकनीक</div>
    <div class="card">💡 नए सवाल और जानकारी</div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("यहाँ अपना सवाल लिखें...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    st.session_state.messages.append({
        "role": "assistant",
        "content": "आपका सवाल मिल गया है। मेरा AI दिमाग अभी जोड़ा नहीं गया है।"
    })

    st.rerun()

st.divider()

st.markdown(
    "<center>🤖 Pocket Sathi | आपका अपना साथी ❤️</center>",
    unsafe_allow_html=True
)
                
                
                
    
                    
            
            
            

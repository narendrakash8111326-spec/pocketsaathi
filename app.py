import streamlit as st
from datetime import datetime

# ---------------------------------------------------------
# POCKET SAATHI - शुरुआती ऐप ढाँचा
# नोट: यह UI prototype है। असली AI, सुरक्षित Login,
# database और microphone बाद में जोड़े जाएँगे।
# ---------------------------------------------------------

st.set_page_config(
    page_title="Pocket Saathi",
    page_icon="icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Session state ----------
defaults = {
    "logged_in": False,
    "user_name": "",
    "messages": [],
    "theme": "Light",
    "language": "हिंदी",
    "voice_reply": False,
    "mic_notice": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- Design ----------
st.markdown("""
<style>
    .stApp { background: #f4f5ff; }
    .main .block-container { max-width: 1050px; padding-top: 1.5rem; }
    .hero {
        background: linear-gradient(120deg, #4936c8, #8b65f5);
        color: white; padding: 28px 24px; border-radius: 22px;
        text-align: center; margin-bottom: 22px;
    }
    .hero h1 { color: white; font-size: 2.2rem; margin-bottom: 6px; }
    .hero p { color: white; font-size: 1.05rem; margin: 0; }
    .info-card {
        background: white; padding: 18px; border-radius: 16px;
        border: 1px solid #e8e8f3; margin-bottom: 12px;
    }
    .small-note { color: #666; font-size: 0.9rem; }
    div.stButton > button {
        border-radius: 12px; min-height: 42px; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🤖 Pocket Saathi")
    st.caption("आपका अपना स्मार्ट साथी")
    if st.session_state.logged_in:
        st.success(f"नमस्ते, {st.session_state.user_name}!")
    else:
        st.info("अभी Guest Mode में हैं")

    page = st.radio(
        "मेन्यू",
        [
            "🏠 होम",
            "💬 नई बातचीत",
            "📚 पढ़ाई और ज्ञान",
            "🔬 विज्ञान और तकनीक",
            "🌍 सामान्य ज्ञान",
            "👤 प्रोफाइल",
            "⚙️ सेटिंग",
            "🛠️ Admin Panel",
            "🔐 Login / Registration",
        ],
        label_visibility="visible"
    )
    st.divider()
    st.caption("Pocket Saathi • शुरुआती संस्करण")

# ---------- Header ----------
st.markdown("""
<div class="hero">
    <h1>🤖 Pocket Saathi</h1>
    <p>आपका अपना स्मार्ट साथी</p>
</div>
""", unsafe_allow_html=True)

# ---------- Home ----------
if page == "🏠 होम":
    st.header("नमस्ते! 👋")
    name = st.session_state.user_name or "दोस्त"
    st.write(f"स्वागत है, **{name}**। आप Pocket Saathi में क्या करना चाहते हैं?")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="info-card"><h3>💬 नई बातचीत</h3>अपना सवाल लिखने के लिए बातचीत सेक्शन खोलें।</div>', unsafe_allow_html=True)
        if st.button("बातचीत शुरू करें", use_container_width=True):
            st.session_state.messages.append({
                "role": "assistant",
                "content": "नमस्ते! मैं Pocket Saathi का शुरुआती चैट पेज हूँ। असली AI अभी जोड़ा नहीं गया है।"
            })
            st.session_state["go_chat"] = True
            st.rerun()
    with col2:
        st.markdown('<div class="info-card"><h3>📚 पढ़ाई और ज्ञान</h3>पढ़ाई, सामान्य जानकारी और सीखने के सेक्शन।</div>', unsafe_allow_html=True)
        if st.button("पढ़ाई सेक्शन खोलें", use_container_width=True):
            st.session_state["go_study"] = True
            st.rerun()

    st.subheader("✨ उपलब्ध सेक्शन")
    cards = [
        ("📚", "पढ़ाई और सामान्य ज्ञान"),
        ("🔬", "विज्ञान और तकनीक"),
        ("🌍", "सामान्य ज्ञान"),
        ("👤", "प्रोफाइल"),
        ("⚙️", "सेटिंग"),
        ("🎤", "माइक्रोफोन — बाद में जोड़ा जाएगा"),
    ]
    for icon, title in cards:
        st.markdown(f'<div class="info-card">{icon} &nbsp; <b>{title}</b></div>', unsafe_allow_html=True)

    st.info("यह अभी ऐप का शुरुआती ढाँचा है। AI जवाब, असली अकाउंट और माइक्रोफोन कनेक्शन अगले चरण में जोड़े जाएँगे।")

# ---------- Chat ----------
elif page == "💬 नई बातचीत":
    st.header("💬 Pocket Saathi से बातचीत")
    st.caption("अभी यह डेमो चैट है; असली AI API अभी कनेक्ट नहीं है।")

    if st.button("＋ नई बातचीत"):
        st.session_state.messages = []
        st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input("यहाँ अपना सवाल लिखें...")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        demo_reply = (
            "आपका सवाल मिल गया है। 😊 अभी Pocket Saathi का असली AI दिमाग कनेक्ट नहीं है। "
            "AI कनेक्शन जोड़ने के बाद मैं आपके सवाल का वास्तविक जवाब दे पाऊँगा।"
        )
        st.session_state.messages.append({"role": "assistant", "content": demo_reply})
        st.rerun()

    st.divider()
    st.subheader("🎤 आवाज़ से सवाल")
    st.write("माइक्रोफोन का बटन और अनुमति वाला सिस्टम अगले चरण में जोड़ा जाएगा।")
    if st.button("🎤 माइक्रोफोन सेटअप की स्थिति"):
        st.info("माइक्रोफोन अभी कनेक्ट नहीं है। इस बटन से फोन का माइक्रोफोन चालू नहीं होता।")

# ---------- Study ----------
elif page == "📚 पढ़ाई और ज्ञान":
    st.header("📚 पढ़ाई और ज्ञान")
    st.write("यहाँ आगे अलग-अलग विषयों के सेक्शन बनेंगे।")
    subjects = ["गणित", "हिंदी", "अंग्रेज़ी", "विज्ञान", "इतिहास", "कंप्यूटर"]
    choice = st.selectbox("विषय चुनें", subjects)
    st.info(f"'{choice}' के लिए पाठ, सवाल-जवाब और अभ्यास सामग्री अगले चरण में जोड़ी जाएगी।")

# ---------- Science ----------
elif page == "🔬 विज्ञान और तकनीक":
    st.header("🔬 विज्ञान और तकनीक")
    st.write("यहाँ विज्ञान, इलेक्ट्रॉनिक्स, मोबाइल, कंप्यूटर और नई तकनीक के विषय रखे जाएँगे।")
    topic = st.selectbox("विषय चुनें", ["इलेक्ट्रॉनिक्स", "मोबाइल और ऐप", "कंप्यूटर", "रोबोटिक्स", "अंतरिक्ष"])
    st.info(f"'{topic}' का कंटेंट सेक्शन अभी तैयार किया जाना बाकी है।")

# ---------- General knowledge ----------
elif page == "🌍 सामान्य ज्ञान":
    st.header("🌍 सामान्य ज्ञान")
    st.write("यहाँ सामान्य ज्ञान के विषय, रोचक तथ्य और क्विज़ आएँगे।")
    st.info("क्विज़ और प्रश्नोत्तरी अगले चरण में जोड़ी जाएगी।")

# ---------- Profile ----------
elif page == "👤 प्रोफाइल":
    st.header("👤 आपकी प्रोफाइल")
    st.caption("यह अभी केवल स्क्रीन का ढाँचा है; जानकारी database में सेव नहीं होती।")
    current_name = st.session_state.user_name
    new_name = st.text_input("आपका नाम", value=current_name, placeholder="अपना नाम लिखें")
    if st.button("नाम स्क्रीन पर अपडेट करें"):
        st.session_state.user_name = new_name.strip()
        st.success("नाम इस ब्राउज़र सेशन में अपडेट हो गया है। स्थायी सेविंग अभी नहीं है।")
        st.rerun()
    st.write("अकाउंट फोटो, ईमेल और अन्य प्रोफाइल विकल्प बाद में जोड़े जाएँगे।")

# ---------- Settings ----------
elif page == "⚙️ सेटिंग":
    st.header("⚙️ सेटिंग")
    st.session_state.language = st.selectbox(
        "ऐप की भाषा",
        ["हिंदी", "English"],
        index=0 if st.session_state.language == "हिंदी" else 1
    )
    st.session_state.theme = st.selectbox(
        "थीम",
        ["Light", "Dark", "System"],
        index=["Light", "Dark", "System"].index(st.session_state.theme)
    )
    st.session_state.voice_reply = st.toggle(
        "जवाब आवाज़ में सुनने का विकल्प (अभी डेमो)",
        value=st.session_state.voice_reply
    )
    st.divider()
    st.write("**माइक्रोफोन:** अभी कनेक्ट नहीं")
    st.write("**AI सेवा:** अभी कनेक्ट नहीं")
    st.write("**डेटा सेविंग:** अभी database नहीं जुड़ा")
    st.success("सेटिंग इस अस्थायी सेशन में लागू हैं; स्थायी सेविंग बाद में बनेगी।")

# ---------- Admin ----------
elif page == "🛠️ Admin Panel":
    st.header("🛠️ Admin Panel")
    st.warning("यह केवल शुरुआती स्क्रीन है। असली Admin सुरक्षा और अधिकार अभी लागू नहीं हैं।")
    st.write("आगे यहाँ यूज़र प्रबंधन, ऐप की स्थिति और फीचर नियंत्रण जोड़े जाएँगे।")
    st.metric("इस सेशन की चैट", len(st.session_state.messages))
    st.metric("AI कनेक्शन", "अभी नहीं")

# ---------- Login / Registration ----------
elif page == "🔐 Login / Registration":
    st.header("🔐 Login और Registration")
    st.warning("यह अभी केवल डिजाइन/फॉर्म का नमूना है। असली अकाउंट सिस्टम सुरक्षित backend के साथ बाद में बनेगा।")
    tab_login, tab_register = st.tabs(["Login", "नया अकाउंट"])
    with tab_login:
        st.text_input("ईमेल या यूज़रनेम", key="login_name")
        st.text_input("पासवर्ड", type="password", key="login_password")
        st.caption("अभी Login बटन किसी असली अकाउंट में प्रवेश नहीं कराता।")
        st.button("Login (डेमो)", disabled=True)
    with tab_register:
        st.text_input("पूरा नाम", key="register_name")
        st.text_input("ईमेल", key="register_email")
        st.text_input("पासवर्ड बनाएँ", type="password", key="register_password")
        st.caption("अभी Registration डेटा सेव नहीं करता।")
        st.button("अकाउंट बनाएँ (डेमो)", disabled=True)

# ---------- Footer ----------
st.divider()
st.caption(
    f"© {datetime.now().year} Pocket Saathi • शुरुआती संस्करण | "
    "AI, माइक्रोफोन, सुरक्षित Login और database अभी जोड़े जाने बाकी हैं।"
)

                
                
                
    
                    
            
            
            

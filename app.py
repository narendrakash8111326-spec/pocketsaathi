import streamlit as st
import sqlite3
import json
from datetime import datetime
from pathlib import Path
import streamlit.components.v1 as components

# =========================================================
# POCKET SAATHI - MASTER UI FOUNDATION
# Working: settings/profile/chat-history stored in SQLite,
# navigation, study sections, theme, browser speech playback,
# microphone audio capture (recording only).
# Not yet included: real AI, speech-to-text, secure cloud auth,
# cloud database, production admin/security.
# =========================================================

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "pocket_saathi.db"

st.set_page_config(
    page_title="Pocket Saathi",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- Database --------------------
def db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                user_name TEXT NOT NULL DEFAULT '',
                language TEXT NOT NULL DEFAULT 'हिंदी',
                theme TEXT NOT NULL DEFAULT 'Light',
                voice_reply INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("INSERT OR IGNORE INTO settings (id) VALUES (1)")

def load_settings():
    with db() as conn:
        row = conn.execute("SELECT * FROM settings WHERE id=1").fetchone()
        return dict(row)

def save_settings(name, language, theme, voice_reply):
    with db() as conn:
        conn.execute("""
            UPDATE settings
            SET user_name=?, language=?, theme=?, voice_reply=?
            WHERE id=1
        """, (name, language, theme, int(voice_reply)))

def load_messages():
    with db() as conn:
        rows = conn.execute(
            "SELECT role, content, created_at FROM messages ORDER BY id"
        ).fetchall()
        return [dict(r) for r in rows]

def add_message(role, content):
    with db() as conn:
        conn.execute(
            "INSERT INTO messages (role, content, created_at) VALUES (?, ?, ?)",
            (role, content, datetime.now().isoformat(timespec="seconds"))
        )

def clear_messages():
    with db() as conn:
        conn.execute("DELETE FROM messages")

init_db()
saved = load_settings()

# -------------------- Session defaults --------------------
defaults = {
    "user_name": saved["user_name"],
    "language": saved["language"],
    "theme": saved["theme"],
    "voice_reply": bool(saved["voice_reply"]),
    "messages": load_messages(),
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------- Theme styling --------------------
dark = st.session_state.theme == "Dark"
if dark:
    bg, card, text, muted, border = "#101321", "#1d2335", "#f4f5fb", "#b8bfd2", "#343c52"
else:
    bg, card, text, muted, border = "#f4f5ff", "#ffffff", "#171923", "#626779", "#e3e5ef"

st.markdown(f"""
<style>
    .stApp {{ background: {bg}; color: {text}; }}
    [data-testid="stSidebar"] {{ background: {card}; }}
    .main .block-container {{ max-width: 1100px; padding-top: 1.2rem; }}
    .hero {{
        background: linear-gradient(120deg, #4936c8, #8b65f5);
        color: white; padding: 25px 20px; border-radius: 22px;
        text-align: center; margin-bottom: 20px;
    }}
    .hero h1 {{ color: white; font-size: 2.1rem; margin: 0 0 5px 0; }}
    .hero p {{ color: white; margin: 0; }}
    .info-card {{
        background: {card}; color: {text}; padding: 17px;
        border-radius: 16px; border: 1px solid {border}; margin-bottom: 12px;
    }}
    .muted {{ color: {muted}; }}
    div.stButton > button {{ border-radius: 12px; min-height: 42px; font-weight: 600; }}
</style>
""", unsafe_allow_html=True)

# -------------------- Header --------------------
st.markdown("""
<div class="hero">
  <h1>🤖 Pocket Saathi</h1>
  <p>आपका अपना स्मार्ट साथी</p>
</div>
""", unsafe_allow_html=True)

# -------------------- Sidebar navigation --------------------
pages = [
    "🏠 होम", "💬 नई बातचीत", "📚 पढ़ाई और ज्ञान",
    "🔬 विज्ञान और तकनीक", "🌍 सामान्य ज्ञान",
    "👤 प्रोफाइल", "⚙️ सेटिंग", "🛠️ Admin Panel",
    "🔐 Login / Registration"
]
with st.sidebar:
    st.markdown("## 🤖 Pocket Saathi")
    st.caption("आपका अपना स्मार्ट साथी")
    if st.session_state.user_name.strip():
        st.success(f"नमस्ते, {st.session_state.user_name}!")
    else:
        st.info("Guest Mode")
    page = st.radio("मेन्यू", pages, label_visibility="visible")
    st.divider()
    st.caption("Master UI Foundation • संस्करण 1")

# -------------------- Helpers --------------------
def speak_text(text):
    # Browser/device speech synthesis. Voice availability depends on browser/device.
    safe_text = json.dumps(str(text), ensure_ascii=False)
    html = f"""
    <html><body>
    <button onclick='speak()' style='padding:10px 16px;border-radius:10px;border:0;background:#6046d8;color:white;font-size:15px'>
      🔊 जवाब सुनें
    </button>
    <script>
      const message = {safe_text};
      function speak() {{
        if (!('speechSynthesis' in window)) {{
          alert('इस ब्राउज़र में Text-to-Speech उपलब्ध नहीं है।');
          return;
        }}
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(message);
        utterance.lang = 'hi-IN';
        window.speechSynthesis.speak(utterance);
      }}
    </script></body></html>
    """
    components.html(html, height=55)

def refresh_messages():
    st.session_state.messages = load_messages()

# -------------------- Home --------------------
if page == "🏠 होम":
    st.header("नमस्ते! 👋")
    name = st.session_state.user_name.strip() or "दोस्त"
    st.write(f"स्वागत है, **{name}**। Pocket Saathi में आपका स्वागत है।")
    a, b = st.columns(2)
    with a:
        st.markdown('<div class="info-card"><h3>💬 बातचीत</h3>अभी डेमो चैट उपलब्ध है। असली AI बाद में जोड़ा जाएगा।</div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="info-card"><h3>📚 पढ़ाई</h3>विषय चुनें और पढ़ाई के सेक्शन देखें।</div>', unsafe_allow_html=True)
    st.subheader("✨ उपलब्ध सुविधाएँ")
    for title in [
        "⚙️ सेटिंग और थीम", "🌐 भाषा चुनना", "💾 चैट हिस्ट्री सेव करना",
        "🔊 ब्राउज़र से जवाब पढ़वाना", "🎤 ऑडियो रिकॉर्डिंग इनपुट",
        "📚 पढ़ाई", "🔬 विज्ञान और तकनीक", "🌍 सामान्य ज्ञान"
    ]:
        st.markdown(f'<div class="info-card">{title}</div>', unsafe_allow_html=True)
    st.info("यह ऐप का काम करने वाला शुरुआती आधार है। वास्तविक AI जवाब और आवाज़ से लिखित सवाल पहचानना अभी जोड़ा जाना बाकी है।")

# -------------------- Chat --------------------
elif page == "💬 नई बातचीत":
    st.header("💬 Pocket Saathi से बातचीत")
    st.caption("यह अभी डेमो चैट है; वास्तविक AI API कनेक्ट नहीं है।")
    top1, top2 = st.columns([1, 3])
    with top1:
        if st.button("＋ नई बातचीत"):
            clear_messages()
            refresh_messages()
            st.rerun()
    refresh_messages()
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg["role"] == "assistant" and st.session_state.voice_reply:
                speak_text(msg["content"])

    question = st.chat_input("यहाँ अपना सवाल लिखें...")
    if question:
        add_message("user", question)
        demo_reply = (
            "आपका सवाल Pocket Saathi तक पहुँच गया है। अभी असली AI सेवा कनेक्ट नहीं है, "
            "इसलिए मैं वास्तविक उत्तर नहीं दे सकता। AI API जोड़ने के बाद यहाँ AI जवाब देगा।"
        )
        add_message("assistant", demo_reply)
        refresh_messages()
        st.rerun()

    st.divider()
    st.subheader("🎤 माइक्रोफोन ऑडियो रिकॉर्डिंग")
    st.write("नीचे रिकॉर्डिंग की अनुमति दें। अभी रिकॉर्डिंग को टेक्स्ट में बदलने (Speech-to-Text) की सुविधा नहीं जुड़ी है।")
    try:
        audio_value = st.audio_input("अपनी आवाज़ रिकॉर्ड करें")
        if audio_value:
            st.audio(audio_value)
            st.success("ऑडियो रिकॉर्ड हो गया। उसे सवाल के टेक्स्ट में बदलने के लिए Speech-to-Text सेवा जोड़नी होगी।")
    except Exception:
        st.warning("आपके Streamlit संस्करण में audio_input उपलब्ध नहीं है। requirements.txt के अनुसार Streamlit अपडेट करें।")

# -------------------- Study --------------------
elif page == "📚 पढ़ाई और ज्ञान":
    st.header("📚 पढ़ाई और ज्ञान")
    subjects = ["गणित", "हिंदी", "अंग्रेज़ी", "विज्ञान", "इतिहास", "कंप्यूटर"]
    choice = st.selectbox("विषय चुनें", subjects)
    st.info(f"आपने **{choice}** चुना है। पाठ, AI ट्यूटर और अभ्यास प्रश्न AI कनेक्शन के बाद जोड़े जाएँगे।")
    st.text_area("अपना पढ़ाई का सवाल लिखें", placeholder="यहाँ सवाल लिखें...")
    st.caption("अभी इस पेज पर सवाल का AI समाधान उपलब्ध नहीं है।")

# -------------------- Science --------------------
elif page == "🔬 विज्ञान और तकनीक":
    st.header("🔬 विज्ञान और तकनीक")
    topic = st.selectbox("विषय चुनें", ["इलेक्ट्रॉनिक्स", "मोबाइल और ऐप", "कंप्यूटर", "रोबोटिक्स", "अंतरिक्ष"])
    st.info(f"'{topic}' सेक्शन चुना गया है। इसके लेख और AI सहायता आगे जोड़ी जाएगी।")

# -------------------- General knowledge --------------------
elif page == "🌍 सामान्य ज्ञान":
    st.header("🌍 सामान्य ज्ञान")
    st.write("यहाँ सामान्य ज्ञान, रोचक तथ्य और क्विज़ का सेक्शन बनेगा।")
    st.info("क्विज़ और सत्यापित जानकारी के लिए कंटेंट/AI सेवा अभी जोड़नी बाकी है।")

# -------------------- Profile --------------------
elif page == "👤 प्रोफाइल":
    st.header("👤 प्रोफाइल")
    st.caption("यह नाम इसी ऐप के SQLite डेटाबेस में सेव होगा। अभी ईमेल अकाउंट/क्लाउड सिंक नहीं है।")
    new_name = st.text_input("आपका नाम", value=st.session_state.user_name, placeholder="अपना नाम लिखें")
    if st.button("प्रोफाइल सेव करें"):
        st.session_state.user_name = new_name.strip()
        save_settings(
            st.session_state.user_name, st.session_state.language,
            st.session_state.theme, st.session_state.voice_reply
        )
        st.success("नाम इस ऐप के डेटाबेस में सेव हो गया।")
        st.rerun()

# -------------------- Settings --------------------
elif page == "⚙️ सेटिंग":
    st.header("⚙️ सेटिंग")
    st.write("यहाँ बदली गई सेटिंग SQLite डेटाबेस में सेव होंगी।")
    with st.form("settings_form"):
        language = st.selectbox(
            "ऐप की भाषा", ["हिंदी", "English"],
            index=0 if st.session_state.language == "हिंदी" else 1
        )
        theme = st.selectbox(
            "थीम", ["Light", "Dark", "System"],
            index=["Light", "Dark", "System"].index(st.session_state.theme)
        )
        voice_reply = st.toggle(
            "चैट के जवाब के साथ 'जवाब सुनें' बटन दिखाएँ",
            value=st.session_state.voice_reply
        )
        saved_button = st.form_submit_button("सेटिंग सेव करें", use_container_width=True)
    if saved_button:
        st.session_state.language = language
        st.session_state.theme = theme
        st.session_state.voice_reply = voice_reply
        save_settings(st.session_state.user_name, language, theme, voice_reply)
        st.success("सेटिंग सेव हो गईं। थीम लागू करने के लिए पेज रिफ्रेश होगा।")
        st.rerun()

    st.divider()
    st.subheader("सेवा की स्थिति")
    st.write("**AI सेवा:** अभी कनेक्ट नहीं")
    st.write("**माइक्रोफोन:** ऑडियो रिकॉर्डिंग उपलब्ध; Speech-to-Text बाकी")
    st.write("**Voice Reply:** ब्राउज़र/फोन की Speech Synthesis पर निर्भर")
    st.write("**डेटा सेविंग:** इस ऐप के SQLite डेटाबेस में")
    st.write("**Login:** सुरक्षित अकाउंट सिस्टम अभी नहीं")
    st.caption("System थीम अभी Light की तरह दिखाई जाएगी; डिवाइस थीम पहचानना अलग से जोड़ा जा सकता है।")

# -------------------- Admin --------------------
elif page == "🛠️ Admin Panel":
    st.header("🛠️ Admin Panel")
    st.warning("यह केवल स्थिति पेज है। अभी कोई सुरक्षित Admin login या user-management अधिकार नहीं हैं।")
    refresh_messages()
    st.metric("सेव चैट संदेश", len(st.session_state.messages))
    st.metric("AI कनेक्शन", "बंद")
    st.metric("डेटाबेस", "SQLite स्थानीय")
    st.caption("इसे सार्वजनिक उपयोग से पहले वास्तविक Admin authentication से सुरक्षित करना जरूरी है।")

# -------------------- Login / Registration --------------------
elif page == "🔐 Login / Registration":
    st.header("🔐 Login / Registration")
    st.warning("यह पेज अभी जानकारी के लिए है। इसमें वास्तविक सुरक्षित Login/Registration लागू नहीं है।")
    st.write("असली अकाउंट सिस्टम के लिए सुरक्षित backend, password hashing, session management और database hosting चाहिए।")
    st.info("फिलहाल प्रोफाइल पेज पर अपना नाम सेव कर सकते हैं। यहाँ नकली Login बटन नहीं दिया गया है।")

# -------------------- Footer --------------------
st.divider()
st.caption(
    f"© {datetime.now().year} Pocket Saathi • Master UI Foundation | "
    "AI और सुरक्षित cloud account अभी जोड़ने बाकी हैं।"
    )
        
        



                
                
                
    
                    
            
            
            

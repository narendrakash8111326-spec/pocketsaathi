import streamlit as st
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from google import genai
import streamlit.components.v1 as components

# =====================================================
# POCKET SAATHI - MASTER VERSION
# Created by Narendra Kashyap
# Gemini AI + Chat + Study + Science + GK
# =====================================================

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "pocket_saathi.db"

MODEL_NAME = "gemini-3.8-flash"

st.set_page_config(
    page_title="Pocket Saathi",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- DATABASE ----------------

def db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY CHECK (id=1),
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

        conn.execute(
            "INSERT OR IGNORE INTO settings (id) VALUES (1)"
        )


def load_settings():
    with db() as conn:
        row = conn.execute(
            "SELECT * FROM settings WHERE id=1"
        ).fetchone()
        return dict(row)


def save_settings(name, language, theme, voice_reply):
    with db() as conn:
        conn.execute("""
            UPDATE settings
            SET user_name=?, language=?, theme=?, voice_reply=?
            WHERE id=1
        """, (
            name,
            language,
            theme,
            int(voice_reply)
        ))


def load_messages():
    with db() as conn:
        rows = conn.execute("""
            SELECT role, content, created_at
            FROM messages
            ORDER BY id
        """).fetchall()

        return [dict(row) for row in rows]


def add_message(role, content):
    with db() as conn:
        conn.execute("""
            INSERT INTO messages (role, content, created_at)
            VALUES (?, ?, ?)
        """, (
            role,
            content,
            datetime.now().isoformat(timespec="seconds")
        ))


def clear_messages():
    with db() as conn:
        conn.execute("DELETE FROM messages")


init_db()
saved = load_settings()

# ---------------- SESSION ----------------

defaults = {
    "user_name": saved["user_name"],
    "language": saved["language"],
    "theme": saved["theme"],
    "voice_reply": bool(saved["voice_reply"]),
    "messages": load_messages()
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def refresh_messages():
    st.session_state.messages = load_messages()


# ---------------- GEMINI AI ----------------

def get_ai_client():
    api_key = st.secrets.get("GEMINI_API_KEY", "")

    if not api_key:
        raise ValueError("GEMINI_API_KEY सेट नहीं है।")

    return genai.Client(api_key=api_key)


def ask_ai(question, section="सामान्य बातचीत"):
    client = get_ai_client()

    language = st.session_state.language

    if language == "हिंदी":
        language_instruction = "सरल और स्पष्ट हिंदी में जवाब दो।"
    else:
        language_instruction = "Answer in clear, simple English."

    system_instruction = f"""
तुम Pocket Saathi हो।

इस ऐप को Narendra Kashyap ने बनाया है।
अगर कोई पूछे कि Pocket Saathi किसने बनाया,
तो बताना कि इसे Narendra Kashyap ने बनाया है।

तुम एक मददगार AI सहायक हो।
{language_instruction}

सवाल का सही, उपयोगी और समझने योग्य जवाब दो।
अगर किसी बात की जानकारी पक्की नहीं है,
तो साफ बता दो। गलत जानकारी मत बनाओ।

वर्तमान सेक्शन: {section}
"""

    prompt = system_instruction + "\n\nयूजर का सवाल:\n" + question

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    answer = response.text

    if not answer:
        return "माफ़ कीजिए, अभी जवाब नहीं मिल पाया।"

    return answer


# ---------------- VOICE ----------------

def speak_text(text):
    safe_text = json.dumps(str(text), ensure_ascii=False)

    html = f"""
    <html>
    <body>
    <button onclick="speak()"
    style="padding:10px 16px;border-radius:10px;
    border:0;background:#6046d8;color:white;font-size:15px">
    🔊 जवाब सुनें
    </button>

    <script>
    const message = {safe_text};

    function speak() {{
        if (!('speechSynthesis' in window)) {{
            alert('इस ब्राउज़र में आवाज़ की सुविधा उपलब्ध नहीं है।');
            return;
        }}

        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(message);
        utterance.lang = 'hi-IN';

        window.speechSynthesis.speak(utterance);
    }}
    </script>
    </body>
    </html>
    """

    components.html(html, height=60)


# ---------------- THEME ----------------

dark = st.session_state.theme == "Dark"

if dark:
    bg = "#101321"
    card = "#1d2335"
    text = "#f4f5fb"
    muted = "#b8bfd2"
    border = "#343c52"
else:
    bg = "#f4f5ff"
    card = "#ffffff"
    text = "#171923"
    muted = "#626779"
    border = "#e3e5ef"


st.markdown(f"""
<style>
.stApp {{
    background: {bg};
    color: {text};
}}

[data-testid="stSidebar"] {{
    background: {card};
}}

.main .block-container {{
    max-width: 1100px;
    padding-top: 1.2rem;
}}

.hero {{
    background: linear-gradient(120deg, #4936c8, #8b65f5);
    color: white;
    padding: 25px 20px;
    border-radius: 22px;
    text-align: center;
    margin-bottom: 20px;
}}

.hero h1 {{
    color: white;
    font-size: 2.1rem;
}}

.hero p {{
    color: white;
}}

.info-card {{
    background: {card};
    color: {text};
    padding: 17px;
    border-radius: 16px;
    border: 1px solid {border};
    margin-bottom: 12px;
}}

div.stButton > button {{
    border-radius: 12px;
    min-height: 42px;
    font-weight: 600;
}}
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>🤖 Pocket Saathi</h1>
    <p>आपका अपना स्मार्ट साथी</p>
    <p>Created by Narendra Kashyap</p>
</div>
""", unsafe_allow_html=True)


# ---------------- NAVIGATION ----------------

pages = [
    "🏠 होम",
    "💬 नई बातचीत",
    "📚 पढ़ाई और ज्ञान",
    "🔬 विज्ञान और तकनीक",
    "🌍 सामान्य ज्ञान",
    "👤 प्रोफाइल",
    "⚙️ सेटिंग",
    "🛠️ Admin Panel",
    "🔐 Login / Registration"
]

with st.sidebar:
    st.markdown("## 🤖 Pocket Saathi")
    st.caption("आपका अपना स्मार्ट साथी")

    if st.session_state.user_name.strip():
        st.success(
            f"नमस्ते, {st.session_state.user_name}!"
        )
    else:
        st.info("Guest Mode")

    page = st.radio("मेन्यू", pages)

    st.divider()
    st.caption("Pocket Saathi Master Version")


# =====================================================
# HOME
# =====================================================

if page == "🏠 होम":

    st.header("नमस्ते! 👋")

    name = st.session_state.user_name.strip() or "दोस्त"

    st.write(
        f"स्वागत है, **{name}**। Pocket Saathi में आपका स्वागत है।"
    )

    a, b = st.columns(2)

    with a:
        st.markdown("""
        <div class="info-card">
        <h3>💬 बातचीत</h3>
        Gemini AI से सवाल पूछें और जवाब पाएँ।
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="info-card">
        <h3>📚 पढ़ाई</h3>
        पढ़ाई और ज्ञान में AI की मदद लें।
        </div>
        """, unsafe_allow_html=True)

    st.subheader("✨ उपलब्ध सुविधाएँ")

    features = [
        "🤖 Gemini AI बातचीत",
        "⚙️ सेटिंग और थीम",
        "🌐 भाषा चुनना",
        "💾 चैट हिस्ट्री सेव करना",
        "🔊 जवाब सुनना",
        "🎤 माइक्रोफोन रिकॉर्डिंग",
        "📚 पढ़ाई और ज्ञान",
        "🔬 विज्ञान और तकनीक",
        "🌍 सामान्य ज्ञान"
    ]

    for item in features:
        st.markdown(
            f'<div class="info-card">{item}</div>',
            unsafe_allow_html=True
        )


# =====================================================
# CHAT
# =====================================================

elif page == "💬 नई बातचीत":

    st.header("💬 Pocket Saathi से बातचीत")
    st.caption("Gemini AI से बातचीत करें।")

    if st.button("＋ नई बातचीत"):
        clear_messages()
        refresh_messages()
        st.rerun()

    refresh_messages()

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

            if (
                msg["role"] == "assistant"
                and st.session_state.voice_reply
            ):
                speak_text(msg["content"])

    question = st.chat_input("यहाँ अपना सवाल लिखें...")

    if question:

        add_message("user", question)

        with st.spinner("Pocket Saathi सोच रहा है..."):

            try:
                ai_reply = ask_ai(
                    question,
                    section="सामान्य बातचीत"
                )

            except Exception:
                ai_reply = (
                    "माफ़ कीजिए, AI से जुड़ने में समस्या आई। "
                    "कृपया Gemini API Key, इंटरनेट और API सेटिंग जाँचें।"
                )

        add_message("assistant", ai_reply)

        refresh_messages()
        st.rerun()

    st.divider()

    st.subheader("🎤 माइक्रोफोन ऑडियो रिकॉर्डिंग")

    st.write(
        "अपनी आवाज़ रिकॉर्ड कर सकते हैं। "
        "रिकॉर्डिंग को अपने आप टेक्स्ट में बदलने की सुविधा अभी नहीं जुड़ी है।"
    )

    try:
        audio_value = st.audio_input("अपनी आवाज़ रिकॉर्ड करें")

        if audio_value:
            st.audio(audio_value)
            st.success("ऑडियो रिकॉर्ड हो गया।")

    except Exception:
        st.warning(
            "इस Streamlit संस्करण में audio_input उपलब्ध नहीं है।"
        )


# =====================================================
# STUDY
# =====================================================

elif page == "📚 पढ़ाई और ज्ञान":

    st.header("📚 पढ़ाई और ज्ञान")

    subjects = [
        "गणित",
        "हिंदी",
        "अंग्रेज़ी",
        "विज्ञान",
        "इतिहास",
        "कंप्यूटर"
    ]

    choice = st.selectbox("विषय चुनें", subjects)

    st.write(f"चुना गया विषय: **{choice}**")

    study_question = st.text_area(
        "अपना पढ़ाई का सवाल लिखें",
        placeholder="यहाँ अपना सवाल लिखें..."
    )

    if st.button("AI से समझें"):

        if study_question.strip():

            with st.spinner("AI जवाब तैयार कर रहा है..."):

                try:
                    answer = ask_ai(
                        study_question,
                        section=f"पढ़ाई - {choice}"
                    )
                    st.success("जवाब तैयार है।")
                    st.write(answer)

                except Exception:
                    st.error(
                        "AI से जुड़ने में समस्या आई। API Key जाँचें।"
                    )

        else:
            st.warning("पहले अपना सवाल लिखें।")


# =====================================================
# SCIENCE
# =====================================================

elif page == "🔬 विज्ञान और तकनीक":

    st.header("🔬 विज्ञान और तकनीक")

    topic = st.selectbox(
        "विषय चुनें",
        [
            "इलेक्ट्रॉनिक्स",
            "मोबाइल और ऐप",
            "कंप्यूटर",
            "रोबोटिक्स",
            "अंतरिक्ष"
        ]
    )

    science_question = st.text_area(
        "विज्ञान या तकनीक का सवाल लिखें"
    )

    if st.button("AI से जवाब पाएँ"):

        if science_question.strip():

            with st.spinner("AI जवाब तैयार कर रहा है..."):

                try:
                    answer = ask_ai(
                        science_question,
                        section=f"विज्ञान और तकनीक - {topic}"
                    )
                    st.write(answer)

                except Exception:
                    st.error("AI सेवा से जुड़ने में समस्या आई।")

        else:
            st.warning("पहले सवाल लिखें।")


# =====================================================
# GENERAL KNOWLEDGE
# =====================================================

elif page == "🌍 सामान्य ज्ञान":

    st.header("🌍 सामान्य ज्ञान")

    st.write(
        "सामान्य ज्ञान, रोचक तथ्य और जानकारी के लिए सवाल पूछें।"
    )

    gk_question = st.text_area(
        "अपना सामान्य ज्ञान का सवाल लिखें"
    )

    if st.button("जवाब प्राप्त करें"):

        if gk_question.strip():

            with st.spinner("जवाब तैयार हो रहा है..."):

                try:
                    answer = ask_ai(
                        gk_question,
                        section="सामान्य ज्ञान"
                    )
                    st.write(answer)

                except Exception:
                    st.error("AI सेवा से जुड़ने में समस्या आई।")

        else:
            st.warning("पहले सवाल लिखें।")


# =====================================================
# PROFILE
# =====================================================

elif page == "👤 प्रोफाइल":

    st.header("👤 प्रोफाइल")

    new_name = st.text_input(
        "आपका नाम",
        value=st.session_state.user_name
    )

    if st.button("प्रोफाइल सेव करें"):

        st.session_state.user_name = new_name.strip()

        save_settings(
            st.session_state.user_name,
            st.session_state.language,
            st.session_state.theme,
            st.session_state.voice_reply
        )

        st.success("प्रोफाइल सेव हो गई।")
        st.rerun()


# =====================================================
# SETTINGS
# =====================================================

elif page == "⚙️ सेटिंग":

    st.header("⚙️ सेटिंग")

    with st.form("settings_form"):

        language = st.selectbox(
            "ऐप की भाषा",
            ["हिंदी", "English"],
            index=(
                0 if st.session_state.language == "हिंदी"
                else 1
            )
        )

        theme = st.selectbox(
            "थीम",
            ["Light", "Dark", "System"],
            index=[
                "Light", "Dark", "System"
            ].index(st.session_state.theme)
        )

        voice_reply = st.toggle(
            "जवाब सुनने का बटन दिखाएँ",
            value=st.session_state.voice_reply
        )

        saved_button = st.form_submit_button(
            "सेटिंग सेव करें",
            use_container_width=True
        )

    if saved_button:

        st.session_state.language = language
        st.session_state.theme = theme
        st.session_state.voice_reply = voice_reply

        save_settings(
            st.session_state.user_name,
            language,
            theme,
            voice_reply
        )

        st.success("सेटिंग सेव हो गईं।")
        st.rerun()

    st.divider()

    st.subheader("सेवा की स्थिति")

    api_configured = bool(
        st.secrets.get("GEMINI_API_KEY", "")
    )

    st.write(
        "**Gemini API:**",
        "Key उपलब्ध" if api_configured else "Key सेट नहीं है"
    )

    st.write("**Voice Reply:** ब्राउज़र की Speech Synthesis")
    st.write("**डेटा सेविंग:** SQLite डेटाबेस")
    st.write("**माइक्रोफोन:** ऑडियो रिकॉर्डिंग")


# =====================================================
# ADMIN PANEL
# =====================================================

elif page == "🛠️ Admin Panel":

    st.header("🛠️ Admin Panel")

    st.warning(
        "यह शुरुआती Admin पेज है। "
        "अभी सुरक्षित Admin Login और user-management लागू नहीं हैं।"
    )

    refresh_messages()

    st.metric(
        "सेव चैट संदेश",
        len(st.session_state.messages)
    )

    st.metric(
        "AI API Key",
        "उपलब्ध" if st.secrets.get("GEMINI_API_KEY", "")
        else "सेट नहीं"
    )

    st.caption(
        "सार्वजनिक उपयोग से पहले सुरक्षित Admin authentication "
        "और user-wise database जरूरी हैं।"
    )


# =====================================================
# LOGIN / REGISTRATION
# =====================================================

elif page == "🔐 Login / Registration":

    st.header("🔐 Login / Registration")

    st.warning(
        "यह पेज अभी शुरुआती ढाँचा है। "
        "वास्तविक अकाउंट सिस्टम अभी लागू नहीं है।"
    )

    st.write(
        "आगे इसमें सुरक्षित Registration, Login, "
        "Password Hashing और User Profile जोड़े जाएँगे।"
    )

    st.info(
        "अभी प्रोफाइल पेज पर अपना नाम सेव कर सकते हैं।"
    )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    f"© {datetime.now().year} Pocket Saathi | "
    "Created by Narendra Kashyap"
    )
    
        
        



                
                
                
    
                    
            
            
            

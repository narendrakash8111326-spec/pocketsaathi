import streamlit as st
import sqlite3, html
from datetime import datetime

APP = "Pocket Saathi"
DB = "pocket_saathi.db"

def connect():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    with connect() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS settings(id INTEGER PRIMARY KEY CHECK(id=1), name TEXT DEFAULT '', language TEXT DEFAULT 'Hindi', theme TEXT DEFAULT 'Light', voice INTEGER DEFAULT 0);
        INSERT OR IGNORE INTO settings(id) VALUES(1);
        CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT, stamp TEXT);
        CREATE TABLE IF NOT EXISTS notes(id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, question TEXT, stamp TEXT);
        CREATE TABLE IF NOT EXISTS topics(id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT, stamp TEXT);
        CREATE TABLE IF NOT EXISTS recordings(id INTEGER PRIMARY KEY AUTOINCREMENT, audio BLOB, mime TEXT, stamp TEXT);
        CREATE TABLE IF NOT EXISTS scores(id INTEGER PRIMARY KEY AUTOINCREMENT, score INTEGER, total INTEGER, stamp TEXT);
        """)

def settings():
    with connect() as c:
        r = c.execute("SELECT name,language,theme,voice FROM settings WHERE id=1").fetchone()
    return dict(name=r[0] or "", language=r[1], theme=r[2], voice=bool(r[3]))

def t(hi, en):
    return en if st.session_state.lang == "English" else hi

def stamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

st.set_page_config(page_title=APP, page_icon="🤝", layout="wide")
init_db()
if "ready" not in st.session_state:
    s = settings()
    st.session_state.name, st.session_state.lang = s["name"], s["language"]
    st.session_state.theme, st.session_state.voice = s["theme"], s["voice"]
    st.session_state.ready = True

if st.session_state.theme == "Dark":
    st.markdown("<style>.stApp{background:#10131b;color:#f4f4f4}[data-testid=stSidebar]{background:#171c28}</style>", unsafe_allow_html=True)
elif st.session_state.theme == "System":
    st.markdown("<style>@media(prefers-color-scheme:dark){.stApp{background:#10131b;color:#f4f4f4}[data-testid=stSidebar]{background:#171c28}}</style>", unsafe_allow_html=True)

hi_pages = ["होम","चैट","पढ़ाई","विज्ञान और तकनीक","सामान्य ज्ञान","मीडिया","प्रोफाइल और सेटिंग्स","एडमिन पैनल","लॉगिन / रजिस्ट्रेशन"]
en_pages = ["Home","Chat","Study","Science & Technology","General Knowledge","Media","Profile & Settings","Admin Panel","Login / Registration"]
pages = en_pages if st.session_state.lang == "English" else hi_pages
with st.sidebar:
    st.title("🤝 " + APP)
    st.caption(t("आपका डिजिटल साथी","Your digital companion"))
    page = st.radio(t("मेन्यू","Menu"), pages, label_visibility="collapsed")
    st.caption(t("लोकल डेटा • इसी डिवाइस पर सेव","Local data • saved on this device"))

if page in ("होम","Home"):
    st.title(t("नमस्ते!","Hello!"))
    st.subheader(t("स्वागत है","Welcome") + (f", {st.session_state.name}" if st.session_state.name else "") + " 👋")
    st.write(t("मेन्यू से कोई फीचर चुनें।","Choose a feature from the menu."))
    with connect() as c:
        m=c.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        n=c.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        a=c.execute("SELECT COUNT(*) FROM recordings").fetchone()[0]
    x,y,z=st.columns(3)
    x.metric(t("चैट संदेश","Chat messages"),m); y.metric(t("सेव सवाल","Saved questions"),n); z.metric(t("रिकॉर्डिंग","Recordings"),a)
    st.info(t("AI दिमाग अभी जुड़ा नहीं है। अगला चरण सुरक्षित API key के साथ AI जोड़ना होगा।","The AI model is not connected yet. Next, connect it using a securely stored API key."))

elif page in ("चैट","Chat"):
    st.title(t("चैट","Chat"))
    st.caption(t("अभी डेमो मोड: यह असली AI जवाब नहीं देता।","Demo mode: these are not real AI answers yet."))
    with connect() as c: rows=c.execute("SELECT role,content,stamp FROM messages ORDER BY id").fetchall()
    for role,msg,when in rows:
        with st.chat_message(role):
            st.markdown(msg); st.caption(when)
    prompt=st.chat_input(t("अपना संदेश लिखें...","Write a message..."))
    if prompt:
        answer=(f"आपने लिखा: {prompt}\n\nयह डेमो जवाब है।" if st.session_state.lang=="Hindi" else f"You wrote: {prompt}\n\nThis is a demo reply.")
        with connect() as c:
            c.execute("INSERT INTO messages VALUES(NULL,?,?,?)",("user",prompt,stamp()))
            c.execute("INSERT INTO messages VALUES(NULL,?,?,?)",("assistant",answer,stamp()))
        st.rerun()
    with st.expander(t("चैट हिस्ट्री","Chat history")):
        st.warning(t("इतिहास मिटाने पर संदेश वापस नहीं आएँगे।","Deleted messages cannot be restored."))
        ok=st.checkbox(t("मैं इतिहास मिटाना चाहता/चाहती हूँ","I want to clear the history"))
        if st.button(t("नई चैट / इतिहास साफ करें","New chat / Clear history"),disabled=not ok):
            with connect() as c: c.execute("DELETE FROM messages")
            st.rerun()

elif page in ("पढ़ाई","Study"):
    st.title(t("पढ़ाई सहायता","Study helper"))
    subjects=["गणित","विज्ञान","अंग्रेज़ी","हिंदी","कंप्यूटर","अन्य"] if st.session_state.lang=="Hindi" else ["Math","Science","English","Hindi","Computer","Other"]
    subject=st.selectbox(t("विषय चुनें","Choose subject"),subjects)
    q=st.text_area(t("अपना सवाल या नोट लिखें","Write your question or note"))
    if st.button(t("सवाल सेव करें","Save question")):
        if q.strip():
            with connect() as c: c.execute("INSERT INTO notes(subject,question,stamp) VALUES(?,?,?)",(subject,q.strip(),stamp()))
            st.success(t("सवाल सेव हो गया।","Question saved."))
        else: st.warning(t("पहले सवाल लिखें।","Please write a question first."))
    st.subheader(t("सेव किए सवाल","Saved questions"))
    with connect() as c: rows=c.execute("SELECT id,subject,question,stamp FROM notes ORDER BY id DESC").fetchall()
    for i,s,q0,when in rows:
        with st.expander(f"{s} • {when}"):
            st.write(q0)
            if st.button(t("मिटाएँ","Delete"),key=f"note{i}"):
                with connect() as c: c.execute("DELETE FROM notes WHERE id=?",(i,))
                st.rerun()

elif page in ("विज्ञान और तकनीक","Science & Technology"):
    st.title(t("विज्ञान और तकनीक","Science & Technology"))
    hi=["इलेक्ट्रॉनिक्स","मोबाइल और ऐप्स","कंप्यूटर","रोबोटिक्स","अंतरिक्ष"]
    en=["Electronics","Mobile & Apps","Computers","Robotics","Space"]
    opts=en if st.session_state.lang=="English" else hi
    chosen=st.selectbox(t("टॉपिक चुनें","Choose a topic"),opts)
    info_hi=["सर्किट, सेंसर और इलेक्ट्रॉनिक उपकरणों का अध्ययन।","मोबाइल, ऐप्स और डिजिटल सुरक्षा की जानकारी।","हार्डवेयर, सॉफ्टवेयर और प्रोग्रामिंग।","सेंसर और प्रोग्राम से मशीनों को काम सिखाना।","ग्रहों, तारों और ब्रह्मांड का अध्ययन।"]
    info_en=["Study of circuits, sensors, and electronic devices.","Learn about mobile devices, apps, and digital safety.","Hardware, software, and programming.","Teaching machines to perform tasks using sensors and programs.","Study of planets, stars, and the universe."]
    st.info((info_en if st.session_state.lang=="English" else info_hi)[opts.index(chosen)])
    with connect() as c: c.execute("INSERT INTO topics(topic,stamp) VALUES(?,?)",(chosen,stamp()))
    st.caption(t("चुना गया टॉपिक सेव हो गया।","Selected topic has been saved."))

elif page in ("सामान्य ज्ञान","General Knowledge"):
    st.title(t("सामान्य ज्ञान क्विज़","General Knowledge Quiz"))
    qs=[
      ("भारत की राजधानी क्या है?","What is the capital of India?",["मुंबई","नई दिल्ली","जयपुर"],["Mumbai","New Delhi","Jaipur"],1),
      ("सौरमंडल का सबसे बड़ा ग्रह कौन-सा है?","Which is the largest planet?",["मंगल","पृथ्वी","बृहस्पति"],["Mars","Earth","Jupiter"],2),
      ("पौधे प्रकाश संश्लेषण में कौन-सी गैस लेते हैं?","Which gas do plants take in during photosynthesis?",["ऑक्सीजन","कार्बन डाइऑक्साइड","नाइट्रोजन"],["Oxygen","Carbon dioxide","Nitrogen"],1)]
    answers=[]
    for i,(qh,qe,oh,oe,correct) in enumerate(qs):
        st.markdown(f"**{i+1}. {t(qh,qe)}**")
        answers.append(st.radio(t("उत्तर चुनें","Choose an answer"),oe if st.session_state.lang=="English" else oh,key=f"quiz{i}",index=None))
    if st.button(t("क्विज़ जमा करें","Submit quiz")):
        score=sum(1 for ans,q in zip(answers,qs) if ans==(q[3] if st.session_state.lang=="English" else q[2])[q[4]])
        with connect() as c: c.execute("INSERT INTO scores(score,total,stamp) VALUES(?,?,?)",(score,len(qs),stamp()))
        st.success(t(f"आपका स्कोर: {score}/{len(qs)}",f"Your score: {score}/{len(qs)}"))

elif page in ("मीडिया","Media"):
    st.title(t("माइक्रोफोन और आवाज़","Microphone & Voice"))
    audio=st.audio_input(t("रिकॉर्डिंग करें","Record audio"))
    if audio:
        st.audio(audio)
        if st.button(t("रिकॉर्डिंग सेव करें","Save recording")):
            with connect() as c: c.execute("INSERT INTO recordings(audio,mime,stamp) VALUES(?,?,?)",(audio.getvalue(),audio.type,stamp()))
            st.success(t("रिकॉर्डिंग सेव हो गई।","Recording saved."))
    with connect() as c: recs=c.execute("SELECT id,audio,mime,stamp FROM recordings ORDER BY id DESC").fetchall()
    for rid,data,mime,when in recs:
        st.caption(when); st.audio(data,format=mime or "audio/wav")
        if st.button(t("मिटाएँ","Delete recording"),key=f"audio{rid}"):
            with connect() as c: c.execute("DELETE FROM recordings WHERE id=?",(rid,))
            st.rerun()
    st.divider()
    text=st.text_area(t("आवाज़ में सुनने के लिए टेक्स्ट","Text to speak"))
    if st.button(t("आवाज़ चलाएँ","Speak")) and text.strip():
        safe=html.escape(text).replace("'","\\'")
        lang="en-US" if st.session_state.lang=="English" else "hi-IN"
        st.components.v1.html(f"""<button onclick="let u=new SpeechSynthesisUtterance('{safe}');u.lang='{lang}';speechSynthesis.cancel();speechSynthesis.speak(u);">{t("आवाज़ सुनें","Play voice")}</button>""",height=55)

elif page in ("प्रोफाइल और सेटिंग्स","Profile & Settings"):
    st.title(t("प्रोफाइल और सेटिंग्स","Profile & Settings"))
    with st.form("prefs"):
        name=st.text_input(t("आपका नाम","Your name"),st.session_state.name)
        lang=st.selectbox(t("भाषा","Language"),["Hindi","English"],index=0 if st.session_state.lang=="Hindi" else 1)
        theme=st.selectbox(t("थीम","Theme"),["Light","Dark","System"],index=["Light","Dark","System"].index(st.session_state.theme))
        voice=st.checkbox(t("वॉइस फीचर चालू रखें","Enable voice feature"),st.session_state.voice)
        save=st.form_submit_button(t("सेटिंग्स सेव करें","Save settings"))
    if save:
        with connect() as c: c.execute("UPDATE settings SET name=?,language=?,theme=?,voice=? WHERE id=1",(name.strip(),lang,theme,int(voice)))
        st.session_state.name=name.strip(); st.session_state.lang=lang; st.session_state.theme=theme; st.session_state.voice=voice
        st.success(t("सेटिंग्स सेव हो गईं।","Settings saved."))
        st.rerun()

elif page in ("एडमिन पैनल","Admin Panel"):
    st.title(t("एडमिन पैनल","Admin Panel"))
    st.warning(t("यह लोकल डेमो पैनल है, सुरक्षित एडमिन लॉगिन या क्लाउड प्रबंधन अभी नहीं है।","This is a local demo panel; secure admin login and cloud management are not implemented."))
    with connect() as c:
        counts=[c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] for table in ("messages","notes","recordings","scores")]
    cols=st.columns(4)
    for col,label,value in zip(cols,[t("संदेश","Messages"),t("पढ़ाई सवाल","Study items"),t("रिकॉर्डिंग","Recordings"),t("क्विज़","Quiz attempts")],counts): col.metric(label,value)
    st.success(t("SQLite डेटाबेस उपलब्ध है।","SQLite database is available."))
    st.write(t("डेटाबेस फ़ाइल:","Database file:"),DB)

elif page in ("लॉगिन / रजिस्ट्रेशन","Login / Registration"):
    st.title(t("लॉगिन / रजिस्ट्रेशन","Login / Registration"))
    st.info(t("अभी नाम केवल इस डिवाइस की लोकल प्रोफाइल में सेव होता है। वास्तविक अकाउंट और ऑनलाइन लॉगिन बाद में जोड़ेंगे।","For now, your name is stored only in this device's local profile. Real accounts and online login can be added later."))
    st.write(t("नाम बदलने के लिए प्रोफाइल और सेटिंग्स खोलें।","Open Profile & Settings to change your name."))

st.sidebar.divider()
st.sidebar.caption("Pocket Saathi • v2.0")
        



                
                
                
    
                    
            
            
            

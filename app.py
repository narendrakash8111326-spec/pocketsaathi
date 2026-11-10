import streamlit as st
import pandas as pd
import json
import os

# -------------------- 1. ऐप पेज और थीम सेटिंग्स --------------------
st.set_page_config(
    page_title="PocketSaathi - आपका बजट साथी",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# डेटा सेव करने की फाइल
DATA_FILE = "pocketsaathi_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"balance": 0.0, "goal": 0.0, "transactions": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# सेशन स्टेट लोड करना
if 'data' not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# -------------------- 2. ऐप की हेडिंग और लोगो --------------------
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>💰 PocketSaathi</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px;'>आपका अपना समझदार और आसान पर्सनल फाइनेंस मैनेजर</p>", unsafe_allow_html=True)
st.markdown("---")

# -------------------- 3. मुख्य नेविगेशन मेनू --------------------
menu = st.sidebar.radio("📌 मेनू चुनें", ["📊 डैशबोर्ड (Dashboard)", "➕ आय / खर्च जोड़ें", "🎯 बचत लक्ष्य सेट करें", "📜 लेन-देन का इतिहास"])

# -------------------- 4. डैशबोर्ड (Dashboard) --------------------
if menu == "📊 डैशबोर्ड (Dashboard)":
    st.subheader("📊 आपका वित्तीय विवरण")
    
    # बैलेंस और गोल कार्ड्स
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="💵 वर्तमान शेष राशि (Balance)", value=f"₹ {data['balance']:,.2f}")
    with col2:
        st.metric(label="🎯 बचत का लक्ष्य (Savings Goal)", value=f"₹ {data['goal']:,.2f}")

    # प्रोग्रेस बार (बचत लक्ष्य की प्रगति)
    if data['goal'] > 0:
        progress = min(max(data['balance'] / data['goal'], 0.0), 1.0)
        st.write(f"**बचत लक्ष्य की प्रगति:** {(progress * 100):.1f}%")
        st.progress(progress)
        if progress >= 1.0:
            st.balloons()
            st.success("🎉 बधाई हो! आपने अपना बचत का लक्ष्य पूरा कर लिया है!")

    st.markdown("---")

    # खर्चों का चार्ट (Pie Chart)
    expenses = [t for t in data['transactions'] if t['type'] == 'Expense']
    if expenses:
        st.subheader("📉 खर्चों का विश्लेषण (Chart)")
        df_exp = pd.DataFrame(expenses)
        category_sum = df_exp.groupby("category")["amount"].sum()
        st.bar_chart(category_sum)
    else:
        st.info("💡 अभी तक कोई खर्चा दर्ज नहीं किया गया है।")

# -------------------- 5. आय और खर्च जोड़ें --------------------
elif menu == "➕ आय / खर्च जोड़ें":
    st.subheader("📝 नया लेन-देन दर्ज करें")
    
    trans_type = st.radio("प्रकार चुनें:", ["खर्चा (Expense)", "आय (Income)"], horizontal=True)
    
    with st.form("transaction_form", clear_on_submit=True):
        amount = st.number_input("राशि दर्ज करें (₹)", min_value=1.0, step=10.0)
        
        if "खर्चा" in trans_type:
            category = st.selectbox("श्रेणी चुनें (Category)", ["खाना (Food)", "यात्रा (Travel)", "खरीदारी (Shopping)", "बिल (Bills)", "अन्य"])
        else:
            category = st.selectbox("आय का जरिया (Income Source)", ["सैलरी (Salary)", "पॉकेट मनी", "बिजनेस", "अन्य"])
            
        submitted = st.form_submit_button("सफलतापूर्वक सेव करें ✅")

        if submitted:
            if "खर्चा" in trans_type:
                if data['balance'] >= amount:
                    data['balance'] -= amount
                    data['transactions'].append({"type": "Expense", "amount": amount, "category": category})
                    save_data(data)
                    st.success(f"✅ ₹ {amount} का खर्चा ('{category}') दर्ज कर लिया गया!")
                else:
                    st.error("⚠️ आपके खाते में पर्याप्त बैलेंस नहीं है!")
            else:
                data['balance'] += amount
                data['transactions'].append({"type": "Income", "amount": amount, "category": category})
                save_data(data)
                st.success(f"✅ ₹ {amount} की आय ('{category}') खाते में जोड़ दी गई!")

# -------------------- 6. बचत लक्ष्य --------------------
elif menu == "🎯 बचत लक्ष्य सेट करें":
    st.subheader("🎯 नया बचत लक्ष्य तय करें")
    
    with st.form("goal_form"):
        new_goal = st.number_input("लक्ष्य राशि (₹ में)", min_value=100.0, value=float(data.get("goal", 1000.0)), step=500.0)
        submitted_goal = st.form_submit_button("लक्ष्य अपडेट करें 🚀")
        
        if submitted_goal:
            data['goal'] = new_goal
            save_data(data)
            st.success("🎯 आपका नया बचत लक्ष्य सेट हो गया है!")

# -------------------- 7. लेन-देन इतिहास --------------------
elif menu == "📜 लेन-देन का इतिहास":
    st.subheader("📜 आपकी हालिया गतिविधियां")
    if data['transactions']:
        df_history = pd.DataFrame(data['transactions'])
        st.dataframe(df_history, use_container_width=True)
    else:
        st.info("अभी तक कोई लेन-देन दर्ज नहीं हुआ है।")


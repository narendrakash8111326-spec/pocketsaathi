import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- 1. पेज सेटअप ---
st.set_page_config(
    page_title="PocketSaathi - Narendra Kashyap",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 PocketSaathi AI")
st.subheader("आपका अपना AI असिस्टेंट और फाइनेंस ट्रैकर")

# --- 2. AI सेटिंग्स (Gemini API) ---
st.sidebar.title("⚙️ AI सेटिंग्स")
api_key = st.sidebar.text_input("अपनी Gemini API Key यहाँ डालें:", type="password")

st.sidebar.markdown("---")
st.sidebar.subheader("मेनू चुनें")
app_mode = st.sidebar.radio("नेविगेशन", ["💬 AI चैट (सवाल-जवाब)", "💰 पॉकेट फाइनेंस ट्रैकर"])

if not api_key:
    st.warning("⚠️ कृपया बाईं तरफ (Sidebar) अपनी Gemini API Key डालें ताकि ऐप सही से काम कर सके।")
else:
    # --- 3. जेमिनी मॉडल सेट करना ---
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('gemini-pro')

    # --- 4. AI चैट (सवाल-जवाब) मोड ---
    if app_mode == "💬 AI चैट (सवाल-जवाब)":
        st.markdown("### मुझसे कुछ भी पूछें")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("यहाँ अपना सवाल लिखें या बोलकर टाइप करें..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"कुछ समस्या आई: {e}")

    # --- 5. पॉकेट फाइनेंस ट्रैकर मोड ---
    elif app_mode == "💰 पॉकेट फाइनेंस ट्रैकर":
        st.markdown("### अपने खर्च और बचत यहाँ मैनेज करें")
        
        if "expenses" not in st.session_state:
            st.session_state.expenses = []

        with st.form("expense_form"):
            item = st.text_input("खर्च या कमाई का नाम (जैसे: चाय, पॉकेट मनी)")
            amount = st.number_input("राशि (₹ में)", min_value=0.0, format="%.2f")
            exp_type = st.selectbox("प्रकार", ["खर्च (-)", "कमाई (+)"])
            
            submitted = st.form_submit_button("जोड़ें")
            if submitted and item:
                actual_amount = amount if exp_type == "कमाई (+)" else -amount
                st.session_state.expenses.append({"item": item, "amount": actual_amount})
                st.success("सफलतापूर्वक जुड़ गया!")

        if st.session_state.expenses:
            df = pd.DataFrame(st.session_state.expenses)
            st.dataframe(df, use_container_width=True)
            total_balance = df["amount"].sum()
            st.metric(label="कुल शेष राशि (Balance)", value=f"₹ {total_balance:.2f}")
            
            

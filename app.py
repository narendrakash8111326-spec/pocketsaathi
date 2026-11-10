import streamlit as st
from openai import OpenAI
from audio_recorder_streamlit import audio_recorder
import io

st.set_page_config(page_title="PocketSaathi AI", page_icon="🤖", layout="centered")

st.title("🤖 PocketSaathi AI Assistant")
st.write("सवाल पूछें, फोटो बनवाएँ या बोलकर बातचीत करें!")

# Sidebar - API Key input
api_key = st.sidebar.text_input("OpenAI API Key (sk-...):", type="password")

if not api_key:
    st.info("👈 शुरुआत करने के लिए कृपया साइडबार में अपनी OpenAI API Key (`sk-...`) डालें।")
    st.stop()

client = OpenAI(api_key=api_key)

# Session state initialization
if "messages" not in st.session_states if hasattr(st, "session_state") else False:
    pass

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mode selection
mode = st.radio("आप क्या करना चाहते हैं?", ["💬 चैट / सवाल-जवाब", "🎨 फोटो बनवाएँ (Image Generation)"], horizontal=True)

# ---------------------------------------------------------
# MODE 1: PHOTO GENERATION (DALL-E 3)
# ---------------------------------------------------------
if mode == "🎨 फोटो बनवाएँ (Image Generation)":
    st.subheader("🎨 नई फोटो बनवाएँ")
    prompt = st.text_input("कैसी फोटो बनाना चाहते हैं? (जैसे: 'A futuristic smart wallet in neon light')")
    
    if st.button("फोटो बनाएँ ✨"):
        if prompt:
            with st.spinner("आपकी फोटो बनाई जा रही है..."):
                try:
                    response = client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        size="1024x1024",
                        quality="standard",
                        n=1,
                    )
                    image_url = response.data[0].url
                    st.image(image_url, caption=prompt, use_column_width=True)
                except Exception as e:
                    st.error(f"फोटो बनाने में दिक्कत आई: {e}")
        else:
            st.warning("कृपया फोटो का विवरण (Prompt) लिखें!")

# ---------------------------------------------------------
# MODE 2: CHAT & VOICE ASSISTANT
# ---------------------------------------------------------
else:
    st.subheader("💬 PocketSaathi से बात करें")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    st.write("---")
    st.write("🎙️ **बोलकर सवाल पूछें (माइक पर क्लिक करें):**")
    audio_bytes = audio_recorder(text="", recording_color="#e84c3d", neutral_color="#6aa84f", icon_size="2x")

    user_text = ""

    # Handle Voice Input
    if audio_bytes:
        with st.spinner("आपकी आवाज़ सुनी जा रही है..."):
            try:
                audio_file = io.BytesIO(audio_bytes)
                audio_file.name = "voice.wav"
                
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                user_text = transcript.text
                st.success(f"आपने कहा: **{user_text}**")
            except Exception as e:
                st.error(f"आवाज़ प्रोसेस करने में गलती हुई: {e}")

    # Handle Text Input
    typed_text = st.chat_input("या यहाँ टाइप करके पूछें...")
    if typed_text:
        user_text = typed_text

    # Process Input (from Voice or Text)
    if user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        with st.chat_message("user"):
            st.write(user_text)

        with st.chat_message("assistant"):
            with st.spinner("PocketSaathi सोच रहा है..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    )
                    bot_reply = response.choices[0].message.content
                    st.write(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

                    # Voice Output (Text to Speech)
                    speech_response = client.audio.speech.create(
                        model="tts-1",
                        voice="alloy",
                        input=bot_reply
                    )
                    st.audio(speech_response.content, format="audio/mp3")

                except Exception as e:
                    st.error(f"जवाब देने में दिक्कत आई: {e}")
                    
            
            
            

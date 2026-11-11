import streamlit as st
from openai import OpenAI
from audio_recorder_streamlit import audio_recorder
import io

st.set_page_config(page_title="PocketSaathi", page_icon="🤖")

st.title("🤖 PocketSaathi AI Assistant")
st.write("सवाल पूछें, फोटो बनवाएँ या बोलकर बातचीत करें!")

# Sidebar - API Key input
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

if not api_key:
    st.info("👈 शुरुआत करने के लिए कृपया साइडबार में अपनी OpenAI API Key दर्ज करें।")
    st.stop()

client = OpenAI(api_key=api_key)

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input options
tab1, tab2, tab3 = st.tabs(["💬 चैट करें", "🎨 फोटो बनवाएँ", "🎙️ बोलकर बात करें"])

# Tab 1: Text Chat
with tab1:
    user_input = st.chat_input("अपना सवाल यहाँ लिखें...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

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
                except Exception as e:
                    st.error(f"जवाब देने में दिक्कत आई: {e}")

# Tab 2: Image Generation
with tab2:
    img_prompt = st.text_input("कैसी फोटो बनाना चाहते हैं? विवरण लिखें:")
    if st.button("फोटो बनाएँ"):
        if img_prompt:
            with st.spinner("फोटो तैयार हो रही है..."):
                try:
                    img_response = client.images.generate(
                        model="dall-e-3",
                        prompt=img_prompt,
                        n=1,
                        size="1024x1024"
                    )
                    image_url = img_response.data[0].url
                    st.image(image_url, caption=img_prompt)
                except Exception as e:
                    st.error(f"फोटो बनाने में दिक्कत आई: {e}")

# Tab 3: Voice Chat
with tab3:
    st.write("माइक बटन दबाकर अपनी बात बोलें:")
    audio_bytes = audio_recorder()
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        with st.spinner("आपकी आवाज़ सुनी जा रही है..."):
            try:
                audio_file = io.BytesIO(audio_bytes)
                audio_file.name = "audio.wav"
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                user_text = transcript.text
                st.write(f"**आपने कहा:** {user_text}")
                
                st.session_state.messages.append({"role": "user", "content": user_text})
                
                with st.spinner("PocketSaathi जवाब तैयार कर रहा है..."):
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    )
                    bot_reply = response.choices[0].message.content
                    st.write(f"**PocketSaathi:** {bot_reply}")
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                    
                    # Voice Output
                    speech_response = client.audio.speech.create(
                        model="tts-1",
                        voice="alloy",
                        input=bot_reply
                    )
                    st.audio(speech_response.content, format="audio/mp3")
            except Exception as e:
                st.error(f"आवाज़ प्रोसेस करने में दिक्कत आई: {e}")
    
                    
            
            
            

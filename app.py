import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder
import os

# ضبط عنوان الصفحة
st.set_page_config(page_title="موسى - المساعد الذكي", page_icon="🤖")

if os.path.exists("mousa.png"):
    st.image("mousa.png", width=100)

st.title("💬 المساعد الذكي موسى")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("الرجاء إضافة GEMINI_API_KEY في إعدادات Secrets!")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض المحادثات السابقة
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg["role"] == "assistant":
                if st.button(f"🔊 استمع للرد", key=f"btn_{idx}"):
                    tts = gTTS(text=msg["content"], lang='ar')
                    audio_path = f"reply_{idx}.mp3"
                    tts.save(audio_path)
                    st.audio(audio_path, format="audio/mp3", autoplay=True)

    st.write("🎤 **اضغط للتحدث مع موسى بصوتك:**")
    audio_record = mic_recorder(
        start_prompt="🔴 اضغط للبدء بالكلام",
        stop_prompt="⏹️ اضغط للإرسال",
        key='recorder'
    )

    user_text = None
    reply_text = None

    # معالجة الصوت مباشرة بدون رفع ملفات
    if audio_record:
        audio_bytes = audio_record['bytes']
        audio_data = {
            "mime_type": "audio/wav",
            "data": audio_bytes
        }
        with st.spinner("موسى يستمع إلى صوتك..."):
            try:
                response = model.generate_content(["استمع لهذا الصوت وأجب عليه باللغة العربية:", audio_data])
                user_text = "🎙️ [رسالة صوتية]"
                reply_text = response.text
            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة الصوت: {e}")

    # كتابة نصية عادية إذا لم يتحدث
    if not audio_record:
        if prompt := st.chat_input("أو اكتب سؤالك هنا..."):
            user_text = prompt
            with st.spinner("موسى يفكر..."):
                response = model.generate_content(prompt)
                reply_text = response.text

    # حفظ الرسائل وإعادة التحديث
    if user_text and reply_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        st.session_state.messages.append({"role": "assistant", "content": reply_text})
        st.rerun()

import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder
import os

# ضبط عنوان الصفحة واللوجو
st.set_page_config(page_title="موسى - المساعد الذكي", page_icon="🤖")

# عرض شعار موسى إن وجد
if os.path.exists("mousa.png"):
    st.image("mousa.png", width=100)

st.title("💬 المساعد الذكي موسى")

# جلب مفتاح API من Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("الرجاء إضافة GEMINI_API_KEY في إعدادات Secrets!")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # حفظ سجل المحادثة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل السابقة
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg["role"] == "assistant":
                if st.button(f"🔊 استمع للرد", key=f"btn_{idx}"):
                    tts = gTTS(text=msg["content"], lang='ar')
                    audio_path = f"reply_{idx}.mp3"
                    tts.save(audio_path)
                    st.audio(audio_path, format="audio/mp3", autoplay=True)

    # إضافة زر التسجيل الصوتي بجانب شريط الإدخال
    st.write("🎤 **اضغط للتحدث مع موسى بصوتك:**")
    audio_record = mic_recorder(
        start_prompt="🔴 اضغط للبدء بالكلام",
        stop_prompt="⏹️ اضغط للإرسال",
        key='recorder'
    )

    user_input = None

    # إذا تم تسجيل صوت
    if audio_record:
        # حفظ الصوت المؤقت
        audio_bytes = audio_record['bytes']
        with open("user_audio.wav", "wb") as f:
            f.write(audio_bytes)
        
        # إرسال الملف الصوتي لموديل جيميناي لفهمه مباشرة
        with st.spinner("موسى يستمع إلى صوتك..."):
            audio_file = genai.upload_file("user_audio.wav")
            response = model.generate_content(["استمع لهذا الصوت وأجب عليه باللغة العربية:", audio_file])
            user_input = "🎙️ [رسالة صوتية]"
            reply_text = response.text

    # استقبال النص الكتابي إذا لم يتم استخدام الصوت
    if not user_input:
        user_input = st.chat_input("أو اكتب سؤالك هنا...")

    # معالجة الرد وإظهاره
    if user_input and 'reply_text' in locals():
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": reply_text})
        st.rerun()

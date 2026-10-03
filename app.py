import streamlit as st
from google import genai
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder
import os

# ضبط عنوان الصفحة واللوجو
st.set_page_config(page_title="موسى - المساعد الذكي", page_icon="🤖")

if os.path.exists("mousa.png"):
    st.image("mousa.png", width=100)

st.title("💬 المساعد الذكي موسى")

# جلب المفتاح من Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("الرجاء إضافة GEMINI_API_KEY في إعدادات Secrets!")
else:
    # إنشاء العميل باستعمال المكتبة الحديثة
    client = genai.Client(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض سجل المحادثات
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg["role"] == "assistant":
                if st.button("🔊 استمع للرد", key=f"btn_{idx}"):
                    tts = gTTS(text=msg["content"], lang='ar')
                    audio_path = f"reply_{idx}.mp3"
                    tts.save(audio_path)
                    st.audio(audio_path, format="audio/mp3", autoplay=True)

    # التسجيل الصوتي
    st.write("🎤 **اضغط للتحدث مع موسى بصوتك:**")
    audio_record = mic_recorder(
        start_prompt="🔴 اضغط للبدء بالكلام",
        stop_prompt="⏹ اضغط للإرسال",
        key='recorder'
    )

    # حقل الكتابة النصية
    user_prompt = st.chat_input("أو اكتب سؤالك هنا...")

    # معالجة الصوت
    if audio_record and "audio_processed" not in st.session_state:
        audio_bytes = audio_record['bytes']
        with st.spinner("موسى يستمع إلى صوتك..."):
            try:
                # استخدام النموذج الحديث gemini-2.5-flash
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        "استمع لهذا الصوت وأجب عليه باللغة العربية:",
                        genai.types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav")
                    ]
                )
                st.session_state.messages.append({"role": "user", "content": "🎙️ [رسالة صوتية]"})
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة الصوت: {e}")

    # معالجة النص
    elif user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.write(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("موسى يفكر..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=user_prompt
                    )
                    reply_text = response.text
                    st.write(reply_text)
                    st.session_state.messages.append({"role": "assistant", "content": reply_text})
                    st.rerun()
                except Exception as e:
                    st.error(f"تعذر الحصول على رد من موسى: {e}")

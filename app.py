import os
import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="المساعد الذكي موسى",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 المساعد الذكي موسى")
st.write("مرحباً بك! يمكنك التحدث معي بالصوت أو الكتابة.")

# 2. جلب مفتاح الـ API من Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("لم يتم العثور على مفتاح GEMINI_API_KEY في قسم Secrets. يرجى إضافته أولاً.")
    st.stop()

# تهيئة مكتبة Gemini
genai.configure(api_key=api_key)

# 3. تهيئة النموذج باستخدام الاسم الأحدث لتفادي خطأ 404
try:
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
except Exception as e:
    st.error(f"حدث خطأ أثناء تهيئة النموذج: {e}")

# 4. تهيئة سجل المحادثة في الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. وظيفة تحويل النص إلى صوت
def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='ar')
        tts.save("response.mp3")
        st.audio("response.mp3", format="audio/mp3")
    except Exception as e:
        st.warning("تعذر تحويل الرد إلى صوت.")

# 7. قسم التسجيل الصوتي
st.subheader("🎤 اضغط للتحدث مع موسى بصوتك")
audio = mic_recorder(
    start_prompt="اضغط للبدء بالكلام 🔴",
    stop_prompt="اضغط للانتهاء والتسجيل ⏹️",
    key='recorder'
)

user_prompt = None

if audio:
    st.info("جاري معالجة الصوت...")

# 8. حقل الإدخال النصي
if prompt := st.chat_input("أو اكتب سؤالك هنا..."):
    user_prompt = prompt

# 9. معالجة الإدخال وإرساله لـ Gemini
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("موسى يفكر..."):
            try:
                response = model.generate_content(user_prompt)
                bot_reply = response.text
                st.markdown(bot_reply)
                
                text_to_speech(bot_reply)
                
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"تعذر الحصول على رد من موسى: {e}")

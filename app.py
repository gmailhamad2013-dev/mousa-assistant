import streamlit as st
import os
import google.generativeai as genai

# إعداد عنوان الصفحة
st.set_page_config(page_title="المساعد الذكي موسى", page_icon="🤖", layout="centered")

st.title("المساعد الذكي موسى 🤖")
st.write("مرحباً بك! يمكنك التحدث معي بسهولة.")

# جلب مفتاح API من متغيرات البيئة أو من st.secrets
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("لم يتم العثور على مفتاح GEMINI_API_KEY. يرجى إضافته في إعدادات Environment في Render.")
    st.stop()

# تهيئة نموذج Gemini باستخدام النموذج المعتمد
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# إدارة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال مدخلات المستخدم
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    # إضافة رسالة المستخدم للسجل وعرضها
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # الحصول على رد المساعد الذكي
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")

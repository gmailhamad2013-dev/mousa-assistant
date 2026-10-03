import streamlit as st

# 1. إعدادات الصفحة وأيقونة التبويب
st.set_page_config(
    page_title="موسى المساعد الذكي",
    page_icon="mousa.png",
    layout="centered"
)

# 2. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.image("mousa.png", use_container_width=True)
    st.title("عن موسى 🤖")
    st.write("""
    مرحباً بك! أنا **موسى**، مساعدك الذكي المصمم لمساعدتك في الإجابة عن التساؤلات، البرمجة، والمهام اليومية.
    """)
    st.divider()
    if st.button("مسح المحادثة 🗑️"):
        st.session_state.messages = []
        st.rerun()

# 3. الواجهة الرئيسية والشعار
st.image("mousa.png", width=220)
st.title("موسى | Mousa AI 🤖")
st.caption("مساعدك الذكي الشخصي")

# 4. إدارة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً بك! أنا موسى، كيف يمكنني مساعدتك اليوم؟"}
    ]

# عرض الرسائل السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. استقبال إدخال المستخدم
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # رد المساعد الذكي (يمكن ربطه بـ API لاحقاً)
    response = f"استلمت رسالتك: '{prompt}'! جاري معالجتها..."
    
    with st.chat_message("assistant"):
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

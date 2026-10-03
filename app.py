import streamlit as st import streamlit as st

# ضبط إعدادات الصفحة وأيقونة التبويب
st.set_page_config(
    page_title="موسى المساعد الذكي",
    page_icon="mousa.png",  # أيقونة التبويب في المتصفح
    layout="centered"
)

# عرض الشعار في أعلا الواجهة
st.image("mousa.png", width=250)
st.title("مرحباً بك! أنا موسى المساعد الذكي 🤖")

import google.generativeai as genai
from elevenlabs.client import ElevenLabs

# 1. إعدادات الصفحة والواجهة
st.set_page_config(page_title="موسى المساعد الذكي", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f4f9f9; }
    h1 { color: #1e3d59; text-align: center; font-family: 'Arial', sans-serif; }
    h3 { color: #17b978; text-align: center; }
    .stChatMessage { border-radius: 15px; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 موسى المساعد الذكي")
st.subheader("مساعدك الرقمي في مادة الهوية والمواطنة")

# 2. إعداد المفاتيح (سنضعها لاحقاً عند جاهزيتها)
GEMINI_API_KEY = "ضع_مفتاح_جيمناي_هنا"
ELEVENLABS_API_KEY = "ضع_مفتاح_إيليفن_لابز_هنا"
VOICE_ID = "ضع_رقم_صوت_ابن_أختك_هنا"

# 3. توجيه شخصية موسى
SYSTEM_PROMPT = """
اسمك "موسى المساعد الذكي".
أنت مساعد افتراضي ولطيف موجه لطلاب الصف الثالث الابتدائي (عمر 8-9 سنوات).
تخصصك الأساسي هو مادة الهوية والمواطنة، وتعرف كل شيء عن المعالم الوطنية، الثقافة، الأماكن السياحية، والعلوم.
تحدث بأسلوب مشجع، مليء بالحماس، واكتفِ بإجابات بسيطة وقصيرة يناسب الأطفال.
"""

# 4. الرسالة الترحيبية التلقائية أول ما يفتح التطبيق
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "مرحباً! أنا صديقكم موسى المساعد الرقمي. كيف يمكنني مساعدتكم اليوم؟"
        }
    ]

# عرض جميع الرسائل في الشاشة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. استقبال أسئلة الطالب
user_input = st.chat_input("تكلم مع موسى هنا...")

if user_input:
    # عرض سؤال الطالب
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # توليد الإجابة بواسطة الذكاء الاصطناعي
    with st.chat_message("assistant"):
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            full_prompt = f"{SYSTEM_PROMPT}\n\nسؤال الطالب: {user_input}"
            response = model.generate_content(full_prompt)
            answer_text = response.text
            st.markdown(answer_text)

            # تشغيل الصوت إذا تم وضع المفاتيح
            if ELEVENLABS_API_KEY != "ضع_مفتاح_إيليفن_لابز_هنا":
                eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
                audio = eleven_client.generate(
                    text=answer_text,
                    voice=VOICE_ID,
                    model="eleven_multilingual_v2"
                )
                st.audio(audio, format="audio/mp3")

        except Exception as e:
            # رسالة تجريبية تعمل حتى قبل وضع مفاتيح API
            st.markdown("أهلاً بك يا بطل! أنا جاهز للإجابة عن أسئلتك بخصوص الهوية والمواطنة والأماكن الممتعة.")

    st.session_state.messages.append({"role": "assistant", "content": answer_text if 'answer_text' in locals() else "مرحباً بك!"})

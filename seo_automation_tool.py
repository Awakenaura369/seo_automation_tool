import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from groq import Groq

# =================================================================
# 1. إعدادات الصفحة والستايل
# =================================================================
st.set_page_config(page_title="SEO & Social Media Pro AI", layout="wide", page_icon="🚀")

# تهيئة الـ Session State لإدارة التنقل والبيانات
if 'page' not in st.session_state:
    st.session_state.page = "🏠 الرئيسية"
if 'groq_api_key' not in st.session_state:
    st.session_state.groq_api_key = ''

st.markdown("""
<style>
    .main-header { font-size: 2.8rem; background: linear-gradient(45deg, #4b6cb7, #182848); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #4b6cb7; color: white; }
    .card { background: #f9f9f9; padding: 20px; border-radius: 15px; border-left: 5px solid #4b6cb7; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

# =================================================================
# 2. وظائف الذكاء الاصطناعي والتحليل
# =================================================================
def ask_ai(prompt):
    if not st.session_state.groq_api_key:
        return "⚠️ يرجى إدخال مفتاح Groq API في القائمة الجانبية لتشغيل ميزات AI."
    try:
        client = Groq(api_key=st.session_state.groq_api_key)
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ خطأ في الاتصال: {str(e)}"

def analyze_web(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.content, 'html.parser')
        title = soup.title.string if soup.title else "لا يوجد عنوان"
        links = len(soup.find_all('a'))
        images = len(soup.find_all('img'))
        return {"title": title, "links": links, "images": images, "text": soup.get_text()[:2000]}
    except:
        return None

# =================================================================
# 3. صفحات التطبيق
# =================================================================

# --- الصفحة الرئيسية ---
def show_main():
    st.markdown('<h1 class="main-header">🚀 SEO & Social Media Pro</h1>', unsafe_allow_html=True)
    st.write("<p style='text-align:center;'>نظام الأتمتة الشامل للمحتوى، الروابط، وحركة الزوار</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="card"><h3>✍️ المحتوى</h3><p>توليد مقالات وإعادة صياغة احترافية.</p></div>', unsafe_allow_html=True)
        if st.button("اذهب للمحتوى"): st.session_state.page = "✍️ Content AI"; st.rerun()
    with col2:
        st.markdown('<div class="card"><h3>📱 السوشيال</h3><p>أتمتة منشورات فيسبوك، انستغرام وتويتر.</p></div>', unsafe_allow_html=True)
        if st.button("اذهب للسوشيال"): st.session_state.page = "📱 Social Media"; st.rerun()
    with col3:
        st.markdown('<div class="card"><h3>🚦 الترافيك</h3><p>محاكاة زيارات البحث وتخطيط النمو.</p></div>', unsafe_allow_html=True)
        if st.button("اذهب للترافيك"): st.session_state.page = "🚦 Traffic Generator"; st.rerun()

# --- صفحة المحتوى (SEO & Content) ---
def show_content():
    st.title("✍️ AI Content & SEO")
    mode = st.tabs(["توليد مقال جديد", "إعادة صياغة (Spinner)", "كلمات مفتاحية"])
    
    with mode[0]:
        topic = st.text_input("عنوان المقال أو الموضوع:")
        if st.button("توليد المقال"):
            st.markdown(ask_ai(f"اكتب مقال SEO طويل واحترافي عن: {topic}"))
            
    with mode[1]:
        text = st.text_area("أدخل النص المراد تدويره:")
        if st.button("إعادة الصياغة"):
            st.markdown(ask_ai(f"أعد صياغة النص التالي بأسلوب فريد: {text}"))

# --- صفحة السوشيال ميديا ---
def show_social():
    st.title("📱 Social Media Manager")
    col1, col2 = st.columns(2)
    with col1:
        post_topic = st.text_input("موضوع المنشور:")
        platform = st.selectbox("المنصة:", ["Instagram", "Facebook", "Twitter", "LinkedIn"])
    with col2:
        tone = st.selectbox("النبرة:", ["بيعية", "تفاعلية", "رسمية"])
        
    if st.button("توليد منشور السوشيال"):
        st.info(ask_ai(f"اكتب منشور {platform} عن {post_topic} بنبرة {tone}. أضف إيموجي وهاشتاغات."))

# --- صفحة الباكلينكس ---
def show_backlinks():
    st.title("🔗 Backlink Builder")
    site_niche = st.text_input("مجال موقعك (مثلاً: سفر، تقنية):")
    if st.button("البحث عن فرص"):
        st.markdown(ask_ai(f"أعطني خطة 10 مواقع للحصول على باكلينكس Guest Post في مجال {site_niche}."))

# --- صفحة الترافيك (Traffic Generator) ---
def show_traffic():
    st.title("🚦 Traffic Generator & Search Simulator")
    
    

    url = st.text_input("رابط الموقع المستهدف:")
    kw = st.text_input("الكلمة المفتاحية المستهدفة في جوجل:")
    
    col1, col2 = st.columns(2)
    with col1:
        source = st.selectbox("مصدر الترافيك:", ["Google Search", "Direct", "Social Media"])
    with col2:
        visits = st.number_input("عدد الزيارات المحاكية:", 10, 5000)

    if st.button("تشغيل محاكي الترافيك"):
        st.success(f"جاري إرسال إشارات زيارة محاكية من {source} للرابط {url}")
        st.code(f"""
import requests
# Simulation for {visits} visits from {source}
headers = {{'Referer': 'https://www.google.com/search?q={kw}'}}
# logic to repeat request with rotation
        """, language="python")
        st.info("تم تخطيط الحملة. في نسخة الـ Bot، يتم تنفيذ هذه الطلبات عبر Proxy.")

# --- صفحة محلل المواقع ---
def show_analyzer():
    st.title("📊 Site Analyzer")
    url = st.text_input("أدخل الرابط للفحص:")
    if st.button("ابدأ التحليل"):
        data = analyze_web(url)
        if data:
            st.write(f"✅ **العنوان:** {data['title']}")
            st.write(f"🔗 **الروابط المكتشفة:** {data['links']}")
            st.write(f"🖼️ **الصور:** {data['images']}")
        else:
            st.error("فشل الوصول للموقع.")

# =================================================================
# 4. التحكم الرئيسي (Main App)
# =================================================================
def main():
    with st.sidebar:
        st.header("🛠️ الإعدادات")
        st.session_state.groq_api_key = st.text_input("Groq API Key:", type="password")
        st.write("---")
        
        menu = ["🏠 الرئيسية", "✍️ Content AI", "📱 Social Media", "🔗 Backlinks", "📊 Analyzer", "🚦 Traffic Generator"]
        choice = st.radio("القائمة:", menu, index=menu.index(st.session_state.page) if st.session_state.page in menu else 0)
        st.session_state.page = choice

    # منطق عرض الصفحات
    if st.session_state.page == "🏠 الرئيسية": show_main()
    elif st.session_state.page == "✍️ Content AI": show_content()
    elif st.session_state.page == "📱 Social Media": show_social()
    elif st.session_state.page == "🔗 Backlinks": show_backlinks()
    elif st.session_state.page == "📊 Analyzer": show_analyzer()
    elif st.session_state.page == "🚦 Traffic Generator": show_traffic()

if __name__ == "__main__":
    main()

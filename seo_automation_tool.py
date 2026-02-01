import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import json
import time
import re
from urllib.parse import urlparse, urljoin
import random

# محاولة استيراد Groq
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# =================================================================
# إعدادات الصفحة والستايل
# =================================================================

st.set_page_config(
    page_title="SEO & Social Media Automation Pro",
    page_icon="🚀",
    layout="wide"
)

# تهيئة session state للتنقل بين الصفحات
if 'page' not in st.session_state:
    st.session_state.page = "🏠 الرئيسية"
if 'groq_api_key' not in st.session_state:
    st.session_state.groq_api_key = ''

# CSS المخصص لجعل الواجهة احترافية
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; text-align: center; color: #764ba2; font-weight: bold; }
    .feature-box {
        background: #f8f9fa; padding: 20px; border-radius: 10px;
        border-right: 5px solid #764ba2; margin-bottom: 10px;
    }
    .metric-card {
        background: white; padding: 20px; border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# =================================================================
# دوال المساعدة والذكاء الاصطناعي
# =================================================================

def init_groq():
    if not GROQ_AVAILABLE or not st.session_state.groq_api_key:
        return None
    return Groq(api_key=st.session_state.groq_api_key)

def generate_ai_content(prompt, max_tokens=1500):
    client = init_groq()
    if not client:
        return "⚠️ عذراً، يجب إدخال مفتاح API لـ Groq في الإعدادات لتفعيل هذه الميزة."
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

def extract_keywords_from_text(text, num=10):
    words = re.findall(r'\w+', text.lower())
    stop_words = {'the', 'and', 'with', 'this', 'من', 'في', 'على', 'إلى'}
    filtered = [w for w in words if len(w) > 3 and w not in stop_words]
    return pd.Series(filtered).value_counts().head(num)

def analyze_website(url):
    try:
        res = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.content, 'html.parser')
        text = soup.get_text()
        return {
            'title': soup.title.string if soup.title else "N/A",
            'desc': soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else "N/A",
            'word_count': len(text.split()),
            'links': len(soup.find_all('a')),
            'images': len(soup.find_all('img')),
            'keywords': extract_keywords_from_text(text)
        }
    except Exception as e:
        return {"error": str(e)}

# =================================================================
# دوال عرض الصفحات (المعدلة بالكامل)
# =================================================================

def show_main_page():
    st.markdown('<h1 class="main-header">🚀 SEO & Social Media Automation Pro</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>نظام متكامل لإدارة وتحليل المحتوى باستخدام الذكاء الاصطناعي</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="metric-card"><h3>100%</h3><p>دقة التحليل</p></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="metric-card"><h3>Llama 3</h3><p>محرك الذكاء الاصطناعي</p></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="metric-card"><h3>Fast</h3><p>سرعة التنفيذ</p></div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("🎯 اختر أداة للبدء")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("✍️ مولد المحتوى الذكي"): st.session_state.page = "✍️ AI Content Generator"; st.rerun()
    with c2:
        if st.button("📊 محلل المواقع الشامل"): st.session_state.page = "📊 Site Analyzer"; st.rerun()
    with c3:
        if st.button("🔄 إعادة صياغة المقالات"): st.session_state.page = "🔄 Article Spinner"; st.rerun()

def show_content_generator():
    st.title("✍️ AI Content Generator")
    topic = st.text_input("عن ماذا تريد الكتابة؟", placeholder="مثلاً: فوائد زيت الزيتون للبشرة")
    lang = st.radio("اللغة", ["العربية", "English"], horizontal=True)
    
    if st.button("🚀 توليد المحتوى"):
        with st.spinner("جاري الكتابة..."):
            prompt = f"Write a comprehensive SEO article about {topic} in {lang}. Include headings and bullet points."
            result = generate_ai_content(prompt)
            st.markdown(result)

def show_site_analyzer():
    st.title("📊 Site Analyzer")
    url = st.text_input("أدخل رابط الموقع لتحليله", placeholder="https://example.com")
    if st.button("🔍 ابدأ الفحص"):
        with st.spinner("جاري تحليل بيانات الموقع..."):
            data = analyze_website(url)
            if 'error' in data:
                st.error(data['error'])
            else:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("عدد الكلمات", data['word_count'])
                col2.metric("الروابط", data['links'])
                col3.metric("الصور", data['images'])
                col4.metric("حالة الـ Title", "✅" if data['title'] != "N/A" else "❌")
                
                st.info(f"**العنوان:** {data['title']}")
                st.write(f"**وصف الميتا:** {data['desc']}")
                st.subheader("🔑 الكلمات الأكثر تكراراً")
                st.bar_chart(data['keywords'])

def show_article_spinner():
    st.title("🔄 Article Spinner")
    text = st.text_area("أدخل النص المراد إعادة صياغته", height=200)
    if st.button("✨ إعادة صياغة الآن"):
        with st.spinner("جاري المعالجة..."):
            prompt = f"Rewrite the following text in a unique way while keeping the same meaning:\n\n{text}"
            result = generate_ai_content(prompt)
            st.success("تمت إعادة الصياغة بنجاح:")
            st.write(result)

def show_keyword_research():
    st.title("🔍 Keyword Research")
    main_kw = st.text_input("الكلمة الرئيسية")
    if st.button("البحث عن أفكار"):
        prompt = f"Generate 10 long-tail keyword ideas and search intent for: {main_kw}"
        result = generate_ai_content(prompt)
        st.markdown(result)

# =================================================================
# الشريط الجانبي والدالة الرئيسية
# =================================================================

def main():
    with st.sidebar:
        st.title("⚙️ الإعدادات")
        st.session_state.groq_api_key = st.text_input("Groq API Key", value=st.session_state.groq_api_key, type="password")
        if not st.session_state.groq_api_key:
            st.warning("⚠️ أدخل المفتاح لتفعيل AI")
        
        st.write("---")
        # القائمة تتبع الـ session state لضمان التزامن
        page_choice = st.radio(
            "📋 القائمة الرئيسية",
            ["🏠 الرئيسية", "✍️ AI Content Generator", "📊 Site Analyzer", "🔄 Article Spinner", "🔍 Keyword Research"],
            index=["🏠 الرئيسية", "✍️ AI Content Generator", "📊 Site Analyzer", "🔄 Article Spinner", "🔍 Keyword Research"].index(st.session_state.page)
        )
        st.session_state.page = page_choice

    # عرض الصفحة المختارة
    if st.session_state.page == "🏠 الرئيسية":
        show_main_page()
    elif st.session_state.page == "✍️ AI Content Generator":
        show_content_generator()
    elif st.session_state.page == "📊 Site Analyzer":
        show_site_analyzer()
    elif st.session_state.page == "🔄 Article Spinner":
        show_article_spinner()
    elif st.session_state.page == "🔍 Keyword Research":
        show_keyword_research()

if __name__ == "__main__":
    main()

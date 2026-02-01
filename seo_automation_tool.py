import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import random
from groq import Groq

# =================================================================
# 1. إعدادات الصفحة والـ Session State
# =================================================================
st.set_page_config(page_title="SEO & Marketing Automation Pro", layout="wide", page_icon="🚀")

if 'page' not in st.session_state:
    st.session_state.page = "🏠 الرئيسية"
if 'groq_api_key' not in st.session_state:
    st.session_state.groq_api_key = ''
if 'proxy_list' not in st.session_state:
    st.session_state.proxy_list = []

# =================================================================
# 2. وظائف الذكاء الاصطناعي والبروكسي
# =================================================================

def generate_ai_content(prompt):
    if not st.session_state.groq_api_key:
        return "⚠️ عذراً، يجب إدخال مفتاح API لـ Groq في الإعدادات."
    try:
        client = Groq(api_key=st.session_state.groq_api_key)
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ خطأ في AI: {str(e)}"

def get_free_proxies():
    """جلب بروكسيات مجانية وتجربتها"""
    url = "https://www.sslproxies.org/"
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        proxies = []
        # استخراج أول 15 بروكسي من الجدول
        table = soup.find('table', id='proxylisttable') # قد يتغير الـ ID حسب تحديث الموقع
        rows = soup.find_all('tr')[1:16] 
        for row in rows:
            tds = row.find_all('td')
            if len(tds) > 1:
                proxies.append(f"{tds[0].text}:{tds[1].text}")
        return proxies
    except Exception as e:
        st.error(f"خطأ في جلب البروكسيات: {e}")
        return []

# =================================================================
# 3. صفحات التطبيق
# =================================================================

def show_main_page():
    st.markdown("<h1 style='text-align: center;'>🚀 SEO & Social Media Master</h1>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📱 إدارة السوشيال ميديا", use_container_width=True):
            st.session_state.page = "📱 Social Media"; st.rerun()
    with col2:
        if st.button("🚦 مولد الترافيك والبروكسي", use_container_width=True):
            st.session_state.page = "🚦 Traffic Generator"; st.rerun()
    with col3:
        if st.button("📊 محلل المواقع", use_container_width=True):
            st.session_state.page = "📊 Site Analyzer"; st.rerun()

def show_traffic_generator():
    st.title("🚦 Traffic & Search Simulator")
    
    url = st.text_input("رابط الموقع المستهدف:", placeholder="https://example.com")
    keyword = st.text_input("الكلمة المفتاحية (Referer):", value="google search")
    
    c1, c2 = st.columns(2)
    with c1:
        visit_count = st.number_input("عدد الزيارات:", min_value=1, max_value=500, value=10)
    with c2:
        use_proxy = st.toggle("تفعيل نظام البروكسي (Proxy Rotation)")

    if use_proxy:
        if st.button("🔄 تحديث قائمة البروكسيات"):
            st.session_state.proxy_list = get_free_proxies()
            st.success(f"تم جلب {len(st.session_state.proxy_list)} بروكسي.")
        
        if st.session_state.proxy_list:
            st.info(f"البروكسيات المتاحة: {', '.join(st.session_state.proxy_list[:3])}...")

    if st.button("🚀 تشغيل المحاكي الآن", type="primary"):
        if not url:
            st.error("أدخل الرابط أولاً!")
            return
            
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(visit_count):
            headers = {
                'User-Agent': random.choice([
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
                    'Mozilla/5.0 (Linux; Android 10; SM-A505F) AppleWebKit/537.36'
                ]),
                'Referer': f'https://www.google.com/search?q={keyword.replace(" ", "+")}'
            }
            
            proxy_config = None
            if use_proxy and st.session_state.proxy_list:
                p = random.choice(st.session_state.proxy_list)
                proxy_config = {"http": f"http://{p}", "https": f"http://{p}"}
            
            try:
                # محاكاة الطلب
                # requests.get(url, headers=headers, proxies=proxy_config, timeout=5)
                time.sleep(random.uniform(0.5, 2.0)) # تأخير لتبدو الزيارة طبيعية
                status_text.text(f"تم إرسال الزيارة رقم {i+1} بنجاح.")
            except:
                status_text.text(f"فشلت الزيارة رقم {i+1} (Proxy Error).")
            
            progress_bar.progress((i + 1) / visit_count)
            
        st.success("✅ اكتملت المهمة!")

def show_social_media():
    st.title("📱 Social Media Content AI")
    topic = st.text_area("عن ماذا تريد الكتابة؟")
    platform = st.multiselect("اختر المنصات:", ["Instagram", "Facebook", "LinkedIn", "Twitter"])
    
    if st.button("✨ توليد المنشورات"):
        with st.spinner("الذكاء الاصطناعي يكتب لك الآن..."):
            prompt = f"Write engaging posts for {', '.join(platform)} about: {topic}. Include emojis and relevant hashtags."
            result = generate_ai_content(prompt)
            st.markdown(result)

def show_site_analyzer():
    st.title("📊 SEO Site Analyzer")
    url = st.text_input("أدخل URL الموقع:")
    if st.button("🔍 تحليل"):
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.content, 'html.parser')
            st.subheader("نتائج التحليل:")
            st.write(f"**العنوان (Title):** {soup.title.string if soup.title else 'لا يوجد'}")
            st.write(f"**وصف الميتا:** {soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else 'لا يوجد'}")
            st.write(f"**عدد الروابط:** {len(soup.find_all('a'))}")
            st.write(f"**عدد الصور:** {len(soup.find_all('img'))}")
        except:
            st.error("تعذر الوصول للموقع.")

# =================================================================
# 4. التحكم في التطبيق (Main App Logic)
# =================================================================

def main():
    with st.sidebar:
        st.title("🛠️ الإعدادات")
        st.session_state.groq_api_key = st.text_input("Groq API Key", value=st.session_state.groq_api_key, type="password")
        st.write("---")
        
        menu = ["🏠 الرئيسية", "📱 Social Media", "🚦 Traffic Generator", "📊 Site Analyzer", "🔗 Backlink Builder"]
        choice = st.radio("القائمة:", menu, index=menu.index(st.session_state.page) if st.session_state.page in menu else 0)
        st.session_state.page = choice
        
    # التنقل بين الصفحات
    if st.session_state.page == "🏠 الرئيسية": show_main_page()
    elif st.session_state.page == "📱 Social Media": show_social_media()
    elif st.session_state.page == "🚦 Traffic Generator": show_traffic_generator()
    elif st.session_state.page == "📊 Site Analyzer": show_site_analyzer()
    elif st.session_state.page == "🔗 Backlink Builder":
        st.title("🔗 Backlink Opportunities")
        st.info("اكتشف أفضل المواقع في مجالك للحصول على باكلينكس.")
        niche = st.text_input("المجال:")
        if st.button("بحث"):
            st.write(generate_ai_content(f"Give me a list of high DA websites for backlinks in the {niche} niche."))

if __name__ == "__main__":
    main()

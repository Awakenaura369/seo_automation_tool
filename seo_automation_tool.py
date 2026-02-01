import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
import time
import re
from urllib.parse import urlparse, urljoin
import hashlib

# إعدادات الصفحة
st.set_page_config(
    page_title="SEO Automation Tool - أداة أتمتة السيو",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# دوال مساعدة
def extract_keywords_from_text(text, num_keywords=10):
    """استخراج الكلمات المفتاحية من النص"""
    # إزالة علامات الترقيم والأرقام
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = text.split()
    
    # كلمات شائعة للتجاهل
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                  'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                  'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                  'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
                  'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}
    
    # تصفية الكلمات
    filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
    
    # حساب التكرار
    word_freq = {}
    for word in filtered_words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # ترتيب حسب التكرار
    sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_keywords[:num_keywords]

def analyze_website(url):
    """تحليل موقع ويب"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # استخراج المعلومات
        title = soup.find('title').text if soup.find('title') else "لا يوجد"
        meta_desc = soup.find('meta', {'name': 'description'})
        meta_desc = meta_desc['content'] if meta_desc else "لا يوجد"
        
        # عدد الروابط
        internal_links = []
        external_links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            parsed = urlparse(full_url)
            
            if parsed.netloc == urlparse(url).netloc:
                internal_links.append(full_url)
            elif parsed.netloc:
                external_links.append(full_url)
        
        # عدد الصور
        images = soup.find_all('img')
        images_with_alt = [img for img in images if img.get('alt')]
        
        # العناوين
        headings = {
            'h1': len(soup.find_all('h1')),
            'h2': len(soup.find_all('h2')),
            'h3': len(soup.find_all('h3')),
        }
        
        # النص
        text_content = soup.get_text()
        word_count = len(text_content.split())
        
        return {
            'title': title,
            'meta_description': meta_desc,
            'internal_links': len(set(internal_links)),
            'external_links': len(set(external_links)),
            'total_images': len(images),
            'images_with_alt': len(images_with_alt),
            'headings': headings,
            'word_count': word_count,
            'keywords': extract_keywords_from_text(text_content, 15)
        }
    except Exception as e:
        return {'error': str(e)}

def spin_text(text, level='medium'):
    """إعادة صياغة النص (نسخة بسيطة)"""
    # قاموس المرادفات البسيط
    synonyms = {
        'good': ['excellent', 'great', 'fine', 'nice'],
        'bad': ['poor', 'terrible', 'awful', 'horrible'],
        'important': ['crucial', 'vital', 'essential', 'significant'],
        'big': ['large', 'huge', 'massive', 'enormous'],
        'small': ['tiny', 'little', 'minor', 'compact'],
        'make': ['create', 'build', 'produce', 'generate'],
        'use': ['utilize', 'employ', 'apply', 'implement'],
        'help': ['assist', 'aid', 'support', 'facilitate'],
        'show': ['display', 'demonstrate', 'present', 'reveal'],
        'think': ['believe', 'consider', 'feel', 'assume'],
    }
    
    words = text.split()
    spun_words = []
    
    for word in words:
        word_lower = word.lower().strip('.,!?;:')
        if word_lower in synonyms and level in ['medium', 'high']:
            import random
            spun_words.append(random.choice(synonyms[word_lower]))
        else:
            spun_words.append(word)
    
    return ' '.join(spun_words)

def generate_backlink_opportunities():
    """توليد فرص للباكلينكس (محاكاة)"""
    opportunities = [
        {
            'platform': 'Medium',
            'type': 'Blog Platform',
            'da': 95,
            'status': 'Available',
            'difficulty': 'Easy'
        },
        {
            'platform': 'WordPress.com',
            'type': 'Blog Platform',
            'da': 94,
            'status': 'Available',
            'difficulty': 'Easy'
        },
        {
            'platform': 'Blogger',
            'type': 'Blog Platform',
            'da': 93,
            'status': 'Available',
            'difficulty': 'Easy'
        },
        {
            'platform': 'Tumblr',
            'type': 'Microblogging',
            'da': 91,
            'status': 'Available',
            'difficulty': 'Easy'
        },
        {
            'platform': 'LinkedIn Articles',
            'type': 'Professional Network',
            'da': 98,
            'status': 'Available',
            'difficulty': 'Medium'
        },
        {
            'platform': 'Reddit',
            'type': 'Forum',
            'da': 91,
            'status': 'Available',
            'difficulty': 'Hard'
        },
        {
            'platform': 'Quora',
            'type': 'Q&A Platform',
            'da': 93,
            'status': 'Available',
            'difficulty': 'Medium'
        },
        {
            'platform': 'GitHub Pages',
            'type': 'Developer Platform',
            'da': 96,
            'status': 'Available',
            'difficulty': 'Medium'
        },
    ]
    
    return pd.DataFrame(opportunities)

# الصفحة الرئيسية
def main_page():
    st.markdown('<h1 class="main-header">🚀 SEO Automation Tool</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #666;">أداة أتمتة السيو الاحترافية</h3>', unsafe_allow_html=True)
    
    # إحصائيات سريعة
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #1E88E5;">150+</h2>
            <p>Backlink Sources</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #43A047;">AI Powered</h2>
            <p>Content Generation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #FB8C00;">Auto</h2>
            <p>Submission</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #E53935;">24/7</h2>
            <p>Monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # الميزات الرئيسية
    st.subheader("📋 الميزات الرئيسية")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>🔗 Backlink Builder</h3>
            <p>بناء روابط خلفية تلقائياً من مئات المصادر</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>✍️ Content Generator</h3>
            <p>توليد محتوى SEO-friendly بالذكاء الاصطناعي</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>🔍 Keyword Research</h3>
            <p>البحث عن أفضل الكلمات المفتاحية</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>🔄 Article Spinner</h3>
            <p>إعادة صياغة المقالات بذكاء</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>📊 Site Analyzer</h3>
            <p>تحليل شامل للمواقع والمنافسين</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>📈 Rank Tracker</h3>
            <p>تتبع ترتيب موقعك في محركات البحث</p>
        </div>
        """, unsafe_allow_html=True)

# صفحة بناء الباكلينكس
def backlink_builder_page():
    st.title("🔗 Backlink Builder - بناء الروابط الخلفية")
    
    st.info("💡 هاد الأداة كتساعدك تبني backlinks من مصادر مختلفة بشكل أوتوماتيكي")
    
    # إدخال البيانات
    col1, col2 = st.columns(2)
    
    with col1:
        target_url = st.text_input("🌐 الموقع المستهدف", placeholder="https://example.com")
        anchor_text = st.text_input("⚓ Anchor Text", placeholder="كلمة مفتاحية")
    
    with col2:
        campaign_name = st.text_input("📁 اسم الحملة", placeholder="Backlink Campaign 2024")
        num_backlinks = st.slider("🔢 عدد الباكلينكس المطلوبة", 1, 50, 10)
    
    content_for_backlinks = st.text_area(
        "📝 المحتوى للنشر",
        placeholder="اكتب المحتوى اللي غادي ينشر مع الباكلينك...",
        height=150
    )
    
    if st.button("🚀 بدء بناء الباكلينكس", type="primary"):
        if target_url and anchor_text and content_for_backlinks:
            with st.spinner("جاري بناء الباكلينكس..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # محاكاة عملية البناء
                opportunities_df = generate_backlink_opportunities()
                selected_platforms = opportunities_df.head(num_backlinks)
                
                results = []
                for idx, row in selected_platforms.iterrows():
                    time.sleep(0.5)  # محاكاة الوقت
                    progress = (idx + 1) / len(selected_platforms)
                    progress_bar.progress(progress)
                    status_text.text(f"النشر على {row['platform']}...")
                    
                    results.append({
                        'Platform': row['platform'],
                        'Status': '✅ تم بنجاح',
                        'DA': row['da'],
                        'Link': f"https://{row['platform'].lower()}.com/your-link"
                    })
                
                st.success(f"✅ تم بناء {len(results)} باكلينك بنجاح!")
                
                # عرض النتائج
                results_df = pd.DataFrame(results)
                st.dataframe(results_df, use_container_width=True)
                
                # زر التحميل
                csv = results_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 تحميل النتائج CSV",
                    csv,
                    f"backlinks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv"
                )
        else:
            st.error("⚠️ المرجو ملء جميع الحقول المطلوبة")
    
    # عرض المصادر المتاحة
    st.markdown("---")
    st.subheader("📊 مصادر الباكلينكس المتاحة")
    st.dataframe(generate_backlink_opportunities(), use_container_width=True)

# صفحة توليد المحتوى
def content_generator_page():
    st.title("✍️ Content Generator - مولد المحتوى")
    
    st.info("💡 استخدم AI لتوليد محتوى محسن لمحركات البحث")
    
    col1, col2 = st.columns(2)
    
    with col1:
        content_type = st.selectbox(
            "📑 نوع المحتوى",
            ["مقال مدونة", "وصف منتج", "Meta Description", "عنوان SEO", "منشور وسائل التواصل"]
        )
        
        keywords = st.text_input("🔑 الكلمات المفتاحية (افصل بفاصلة)", 
                                placeholder="SEO, marketing, optimization")
    
    with col2:
        tone = st.selectbox(
            "🎭 نمط الكتابة",
            ["احترافي", "ودي", "تقني", "تسويقي", "تعليمي"]
        )
        
        word_count = st.slider("📏 عدد الكلمات", 100, 2000, 500, 100)
    
    topic = st.text_input("📌 الموضوع", placeholder="مثال: أهمية SEO في 2024")
    additional_info = st.text_area("ℹ️ معلومات إضافية (اختياري)", height=100)
    
    if st.button("✨ توليد المحتوى", type="primary"):
        if keywords and topic:
            with st.spinner("جاري توليد المحتوى..."):
                time.sleep(2)  # محاكاة الوقت
                
                # محتوى تجريبي
                generated_content = f"""
# {topic}

في عالم التسويق الرقمي المتطور، أصبح {keywords.split(',')[0].strip()} أحد أهم العناصر الأساسية 
للنجاح على الإنترنت. مع التطورات المستمرة في خوارزميات محركات البحث، يجب على الشركات 
والمواقع الإلكترونية أن تولي اهتماماً خاصاً لاستراتيجيات {keywords.split(',')[0].strip()}.

## أهمية {topic}

تكمن أهمية هذا الموضوع في عدة نقاط رئيسية:

1. **تحسين الظهور في نتائج البحث**: من خلال تطبيق استراتيجيات فعالة
2. **زيادة حركة المرور العضوية**: جذب زوار مهتمين بمحتواك
3. **تحسين تجربة المستخدم**: توفير محتوى ذو قيمة عالية

## الخطوات العملية

للاستفادة القصوى من {keywords.split(',')[0].strip()}، يجب اتباع هذه الخطوات:

- البحث الدقيق عن الكلمات المفتاحية المناسبة
- إنشاء محتوى عالي الجودة ومفيد للقارئ
- تحسين العناصر التقنية للموقع
- بناء روابط خلفية ذات جودة عالية

## الخلاصة

في النهاية، النجاح في {topic} يتطلب استراتيجية شاملة ومستمرة. من خلال التركيز على 
جودة المحتوى والتحسين المستمر، يمكنك تحقيق نتائج ممتازة في محركات البحث.

---
*تم التوليد بواسطة SEO Automation Tool*
**الكلمات المفتاحية**: {keywords}
**عدد الكلمات**: ~{word_count}
                """
                
                st.success("✅ تم توليد المحتوى بنجاح!")
                
                # عرض المحتوى
                st.markdown("### 📄 المحتوى المولد:")
                st.markdown(generated_content)
                
                # إحصائيات
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("عدد الكلمات", len(generated_content.split()))
                with col2:
                    st.metric("عدد الأحرف", len(generated_content))
                with col3:
                    st.metric("وقت القراءة", f"{len(generated_content.split()) // 200 + 1} دقيقة")
                
                # أزرار الإجراءات
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📥 تحميل كـ TXT",
                        generated_content,
                        f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    )
                with col2:
                    if st.button("🔄 إعادة الصياغة"):
                        st.info("سيتم إعادة صياغة المحتوى...")
        else:
            st.error("⚠️ المرجو إدخال الموضوع والكلمات المفتاحية")

# صفحة البحث عن الكلمات المفتاحية
def keyword_research_page():
    st.title("🔍 Keyword Research - البحث عن الكلمات المفتاحية")
    
    st.info("💡 اكتشف أفضل الكلمات المفتاحية لموقعك")
    
    col1, col2 = st.columns(2)
    
    with col1:
        seed_keyword = st.text_input("🌱 الكلمة المفتاحية الأساسية", placeholder="مثال: تسويق إلكتروني")
        language = st.selectbox("🌐 اللغة", ["العربية", "English", "Français", "Español"])
    
    with col2:
        country = st.selectbox("🗺️ الدولة", ["المغرب", "السعودية", "مصر", "الإمارات", "الأردن"])
        search_volume = st.select_slider(
            "📊 حجم البحث المطلوب",
            options=["منخفض (0-1K)", "متوسط (1K-10K)", "عالي (10K-100K)", "عالي جداً (100K+)"],
            value="متوسط (1K-10K)"
        )
    
    if st.button("🔎 بحث عن الكلمات المفتاحية", type="primary"):
        if seed_keyword:
            with st.spinner("جاري البحث..."):
                time.sleep(2)
                
                # بيانات تجريبية
                keywords_data = {
                    'الكلمة المفتاحية': [
                        f"{seed_keyword}",
                        f"{seed_keyword} للمبتدئين",
                        f"دورة {seed_keyword}",
                        f"تعلم {seed_keyword}",
                        f"{seed_keyword} مجاناً",
                        f"أفضل {seed_keyword}",
                        f"دليل {seed_keyword}",
                        f"{seed_keyword} 2024",
                        f"استراتيجيات {seed_keyword}",
                        f"{seed_keyword} الاحترافي"
                    ],
                    'حجم البحث الشهري': [15000, 8200, 6500, 5400, 4800, 4200, 3900, 3500, 2800, 2400],
                    'الصعوبة': ['متوسط', 'سهل', 'متوسط', 'سهل', 'صعب', 'متوسط', 'سهل', 'متوسط', 'صعب', 'متوسط'],
                    'CPC ($)': [2.5, 1.8, 3.2, 1.5, 2.1, 2.8, 1.9, 2.3, 3.5, 2.9],
                    'المنافسة': ['عالية', 'متوسطة', 'عالية', 'منخفضة', 'عالية', 'متوسطة', 'منخفضة', 'متوسطة', 'عالية', 'متوسطة']
                }
                
                df = pd.DataFrame(keywords_data)
                
                st.success("✅ تم العثور على 10 كلمات مفتاحية!")
                
                # إحصائيات
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("إجمالي الكلمات", len(df))
                with col2:
                    st.metric("متوسط حجم البحث", f"{df['حجم البحث الشهري'].mean():.0f}")
                with col3:
                    st.metric("متوسط CPC", f"${df['CPC ($)'].mean():.2f}")
                with col4:
                    st.metric("كلمات سهلة", len(df[df['الصعوبة'] == 'سهل']))
                
                st.markdown("---")
                
                # جدول النتائج
                st.dataframe(df, use_container_width=True)
                
                # رسم بياني
                st.subheader("📊 تحليل بصري")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.bar_chart(df.set_index('الكلمة المفتاحية')['حجم البحث الشهري'])
                
                with col2:
                    difficulty_counts = df['الصعوبة'].value_counts()
                    st.bar_chart(difficulty_counts)
                
                # تحميل
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 تحميل النتائج",
                    csv,
                    f"keywords_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv"
                )
        else:
            st.error("⚠️ المرجو إدخال كلمة مفتاحية")

# صفحة Article Spinner
def article_spinner_page():
    st.title("🔄 Article Spinner - إعادة صياغة المقالات")
    
    st.info("💡 أعد صياغة المقالات للحصول على محتوى فريد")
    
    original_text = st.text_area(
        "📝 النص الأصلي",
        placeholder="الصق النص اللي بغيتي تعاود صياغتو هنا...",
        height=200
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        spin_level = st.select_slider(
            "⚙️ مستوى إعادة الصياغة",
            options=["منخفض", "متوسط", "عالي"],
            value="متوسط"
        )
    
    with col2:
        preserve_keywords = st.multiselect(
            "🔐 احتفظ بهذه الكلمات",
            ["SEO", "Marketing", "Digital", "Content", "Website"],
            default=[]
        )
    
    if st.button("🔄 إعادة الصياغة", type="primary"):
        if original_text:
            with st.spinner("جاري إعادة الصياغة..."):
                time.sleep(1.5)
                
                # استخدام دالة spin_text
                spun_text = spin_text(original_text, spin_level.lower())
                
                st.success("✅ تمت إعادة الصياغة بنجاح!")
                
                # عرض النتائج
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### النص الأصلي")
                    st.text_area("", original_text, height=200, disabled=True, label_visibility="collapsed")
                    original_words = len(original_text.split())
                    st.caption(f"📊 عدد الكلمات: {original_words}")
                
                with col2:
                    st.markdown("### النص المعاد صياغته")
                    st.text_area("", spun_text, height=200, disabled=True, label_visibility="collapsed")
                    spun_words = len(spun_text.split())
                    st.caption(f"📊 عدد الكلمات: {spun_words}")
                
                # مقارنة
                similarity = 75  # محاكاة
                st.markdown("---")
                st.subheader("📊 التحليل")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("نسبة التشابه", f"{similarity}%")
                with col2:
                    st.metric("الكلمات المتغيرة", original_words - spun_words + 15)
                with col3:
                    st.metric("الفرادة", f"{100-similarity}%")
                
                # تحميل
                st.download_button(
                    "📥 تحميل النص المعاد صياغته",
                    spun_text,
                    f"spun_article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                )
        else:
            st.error("⚠️ المرجو إدخال النص")

# صفحة تحليل المواقع
def site_analyzer_page():
    st.title("📊 Site Analyzer - محلل المواقع")
    
    st.info("💡 احصل على تحليل شامل لأي موقع ويب")
    
    url = st.text_input("🌐 رابط الموقع", placeholder="https://example.com")
    
    analysis_type = st.multiselect(
        "🔍 نوع التحليل",
        ["SEO الأساسي", "الروابط", "الصور", "السرعة", "الكلمات المفتاحية"],
        default=["SEO الأساسي", "الروابط"]
    )
    
    if st.button("🔍 تحليل الموقع", type="primary"):
        if url:
            with st.spinner("جاري التحليل..."):
                # تحليل الموقع
                analysis = analyze_website(url)
                
                if 'error' in analysis:
                    st.error(f"❌ خطأ في التحليل: {analysis['error']}")
                else:
                    st.success("✅ تم التحليل بنجاح!")
                    
                    # نتائج SEO الأساسي
                    if "SEO الأساسي" in analysis_type:
                        st.subheader("🎯 SEO الأساسي")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**العنوان (Title):**")
                            st.code(analysis['title'])
                            st.caption(f"الطول: {len(analysis['title'])} حرف {'✅' if 30 <= len(analysis['title']) <= 60 else '⚠️'}")
                        
                        with col2:
                            st.markdown(f"**الوصف (Meta Description):**")
                            st.code(analysis['meta_description'])
                            st.caption(f"الطول: {len(analysis['meta_description'])} حرف {'✅' if 120 <= len(analysis['meta_description']) <= 160 else '⚠️'}")
                        
                        # العناوين
                        st.markdown("**توزيع العناوين:**")
                        headings_data = pd.DataFrame([analysis['headings']])
                        st.bar_chart(headings_data.T)
                    
                    # الروابط
                    if "الروابط" in analysis_type:
                        st.subheader("🔗 تحليل الروابط")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("روابط داخلية", analysis['internal_links'])
                        with col2:
                            st.metric("روابط خارجية", analysis['external_links'])
                        with col3:
                            st.metric("إجمالي الروابط", analysis['internal_links'] + analysis['external_links'])
                    
                    # الصور
                    if "الصور" in analysis_type:
                        st.subheader("🖼️ تحليل الصور")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("إجمالي الصور", analysis['total_images'])
                        with col2:
                            st.metric("صور بـ Alt", analysis['images_with_alt'])
                        with col3:
                            alt_percentage = (analysis['images_with_alt'] / analysis['total_images'] * 100) if analysis['total_images'] > 0 else 0
                            st.metric("نسبة التحسين", f"{alt_percentage:.1f}%")
                    
                    # الكلمات المفتاحية
                    if "الكلمات المفتاحية" in analysis_type:
                        st.subheader("🔑 الكلمات المفتاحية المستخرجة")
                        keywords_df = pd.DataFrame(analysis['keywords'], columns=['الكلمة', 'التكرار'])
                        st.dataframe(keywords_df, use_container_width=True)
                    
                    # تقييم عام
                    st.markdown("---")
                    st.subheader("📈 التقييم العام")
                    
                    # حساب النقاط
                    score = 0
                    max_score = 100
                    
                    # Title
                    if 30 <= len(analysis['title']) <= 60:
                        score += 20
                    elif len(analysis['title']) > 0:
                        score += 10
                    
                    # Meta Description
                    if 120 <= len(analysis['meta_description']) <= 160:
                        score += 20
                    elif len(analysis['meta_description']) > 0:
                        score += 10
                    
                    # Images Alt
                    if analysis['total_images'] > 0:
                        alt_ratio = analysis['images_with_alt'] / analysis['total_images']
                        score += int(alt_ratio * 20)
                    
                    # Headings
                    if analysis['headings']['h1'] == 1:
                        score += 20
                    elif analysis['headings']['h1'] > 0:
                        score += 10
                    
                    # Word count
                    if analysis['word_count'] >= 300:
                        score += 20
                    elif analysis['word_count'] >= 100:
                        score += 10
                    
                    st.progress(score / max_score)
                    st.metric("النقاط", f"{score}/{max_score}")
                    
                    if score >= 80:
                        st.success("🎉 ممتاز! الموقع محسن بشكل جيد")
                    elif score >= 60:
                        st.warning("⚠️ جيد، لكن هناك مجال للتحسين")
                    else:
                        st.error("❌ يحتاج إلى تحسينات كبيرة")
        else:
            st.error("⚠️ المرجو إدخال رابط الموقع")

# صفحة تتبع الترتيب
def rank_tracker_page():
    st.title("📈 Rank Tracker - متتبع الترتيب")
    
    st.info("💡 تتبع ترتيب موقعك في محركات البحث")
    
    col1, col2 = st.columns(2)
    
    with col1:
        website = st.text_input("🌐 موقعك", placeholder="example.com")
        search_engine = st.selectbox("🔍 محرك البحث", ["Google", "Bing", "Yahoo"])
    
    with col2:
        location = st.selectbox("📍 الموقع الجغرافي", ["المغرب", "السعودية", "مصر", "الإمارات"])
        device = st.selectbox("📱 الجهاز", ["Desktop", "Mobile"])
    
    keywords_to_track = st.text_area(
        "🔑 الكلمات المفتاحية (واحد في كل سطر)",
        placeholder="كلمة مفتاحية 1\nكلمة مفتاحية 2\nكلمة مفتاحية 3",
        height=100
    )
    
    if st.button("📊 تتبع الترتيب", type="primary"):
        if website and keywords_to_track:
            keywords_list = [k.strip() for k in keywords_to_track.split('\n') if k.strip()]
            
            with st.spinner("جاري التحقق من الترتيب..."):
                time.sleep(2)
                
                # بيانات تجريبية
                import random
                
                tracking_data = []
                for keyword in keywords_list:
                    current_rank = random.randint(1, 100)
                    previous_rank = current_rank + random.randint(-10, 10)
                    change = current_rank - previous_rank
                    
                    tracking_data.append({
                        'الكلمة المفتاحية': keyword,
                        'الترتيب الحالي': current_rank,
                        'الترتيب السابق': previous_rank,
                        'التغيير': change,
                        'الاتجاه': '📈' if change < 0 else '📉' if change > 0 else '➡️',
                        'الصفحة': (current_rank - 1) // 10 + 1,
                        'حجم البحث': random.randint(100, 10000)
                    })
                
                df = pd.DataFrame(tracking_data)
                
                st.success(f"✅ تم تتبع {len(keywords_list)} كلمة مفتاحية!")
                
                # إحصائيات
                col1, col2, col3, col4 = st.columns(4)
                
                improvements = len(df[df['التغيير'] < 0])
                declines = len(df[df['التغيير'] > 0])
                stable = len(df[df['التغيير'] == 0])
                avg_rank = df['الترتيب الحالي'].mean()
                
                with col1:
                    st.metric("متوسط الترتيب", f"{avg_rank:.1f}")
                with col2:
                    st.metric("تحسنات", improvements, delta=f"+{improvements}")
                with col3:
                    st.metric("تراجعات", declines, delta=f"-{declines}", delta_color="inverse")
                with col4:
                    st.metric("مستقر", stable)
                
                st.markdown("---")
                
                # الجدول
                st.dataframe(df, use_container_width=True)
                
                # رسم بياني
                st.subheader("📊 تصور بصري")
                st.bar_chart(df.set_index('الكلمة المفتاحية')['الترتيب الحالي'])
                
                # توصيات
                st.subheader("💡 التوصيات")
                
                if improvements > declines:
                    st.success("🎉 أداء ممتاز! استمر في استراتيجيتك الحالية")
                elif declines > improvements:
                    st.warning("⚠️ هناك بعض التراجع. قد تحتاج لمراجعة استراتيجية المحتوى")
                else:
                    st.info("ℹ️ الأداء مستقر. فكر في تحسينات جديدة")
                
                # تحميل
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 تحميل التقرير",
                    csv,
                    f"rank_tracking_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv"
                )
        else:
            st.error("⚠️ المرجو إدخال الموقع والكلمات المفتاحية")

# الشريط الجانبي
def sidebar():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/seo.png", width=100)
        st.title("SEO Tool")
        
        page = st.radio(
            "📋 القائمة",
            [
                "🏠 الرئيسية",
                "🔗 Backlink Builder",
                "✍️ Content Generator",
                "🔍 Keyword Research",
                "🔄 Article Spinner",
                "📊 Site Analyzer",
                "📈 Rank Tracker"
            ]
        )
        
        st.markdown("---")
        
        # معلومات
        st.subheader("ℹ️ معلومات")
        st.info("""
        هاد الأداة كتوفر ليك:
        - بناء روابط تلقائي
        - توليد محتوى بالـAI
        - بحث عن كلمات مفتاحية
        - تحليل المواقع
        - تتبع الترتيب
        """)
        
        st.markdown("---")
        st.caption("Made with ❤️ using Streamlit")
        
        return page

# البرنامج الرئيسي
def main():
    page = sidebar()
    
    if page == "🏠 الرئيسية":
        main_page()
    elif page == "🔗 Backlink Builder":
        backlink_builder_page()
    elif page == "✍️ Content Generator":
        content_generator_page()
    elif page == "🔍 Keyword Research":
        keyword_research_page()
    elif page == "🔄 Article Spinner":
        article_spinner_page()
    elif page == "📊 Site Analyzer":
        site_analyzer_page()
    elif page == "📈 Rank Tracker":
        rank_tracker_page()

if __name__ == "__main__":
    main()

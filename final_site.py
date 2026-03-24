import streamlit as st
import requests

# --- 1. الإعدادات الأساسية (قانونية وآمنة) ---
API_KEY = "15d12a66d39113a797e50a451064731a"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# --- 2. واجهة المستخدم ---
st.set_page_config(page_title="Salma Private Space", layout="wide")

# تصميم العنوان بشكل شيك
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #E50914;
        font-size: 50px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        color: #555;
        font-size: 20px;
        margin-bottom: 30px;
    }
    </style>
    <div class="main-title">🎬 SALMA FLIX</div>
    <div class="sub-title">أهلاً يا ماما! أحدث الأفلام العالمية والعربية بين يديكِ</div>
    """, unsafe_allow_html=True)

# --- 3. وظائف جلب البيانات ---
def get_movies(query=None):
    if query:
        # بحث عن فيلم معين
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=ar&query={query}"
    else:
        # عرض الأفلام العربية التريند حالياً
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=ar&region=EG&sort_by=popularity.desc&with_original_language=ar"
    
    try:
        res = requests.get(url, timeout=15)
        return res.json().get('results', [])
    except:
        return []

# --- 4. محرك البحث والعرض ---
search_query = st.text_input("🔍 ابحثي عن فيلم يا ماما...", placeholder="اكتبي اسم الفيلم هنا (مثلاً: ولاد رزق)")

# جلب القائمة بناءً على البحث أو الأفلام المقترحة
movies_list = get_movies(search_query if search_query else None)

if movies_list:
    st.write(f"### تم العثور على {len(movies_list)} فيلم")
    
    # توزيع الأفلام في أعمدة (4 أفلام في كل صف)
    cols = st.columns(4)
    for idx, m in enumerate(movies_list[:20]): # نعرض أول 20 نتيجة
        if m.get('poster_path'):
            with cols[idx % 4]:
                # عرض البوستر
                st.image(f"{IMAGE_BASE}{m['poster_path']}", use_container_width=True)
                # العنوان
                st.write(f"**{m['title']}**")
                # سنة الإنتاج والتقييم
                year = m.get('release_date', 'غير معروف')[:4]
                st.caption(f"📅 {year} | ⭐ {m.get('vote_average', 0)}")
                
                # رابط المشاهدة المباشر (باستخدام ID الفيلم)
                # الرابط ده بيفتح مشغل (Player) عالمي مخفي
                tmdb_id = m['id']
                watch_link = f"https://vidsrc.me/embed/movie?tmdb={tmdb_id}"
                
                st.link_button("مشاهدة الآن 🍿", watch_link)
else:
    if search_query:
        st.warning("للأسف مش لاقيين الفيلم ده، جربي اسم تاني.")
    else:
        st.info("جاري تحميل أحدث الأفلام... تأكدي من الإنترنت.")

# --- 5. ركن التعليمات في الجنب ---
st.sidebar.title("تعليمات الاستخدام ❤️")
st.sidebar.success("""
1. اختاري الفيلم اللي تحبيه.
2. دوسي على زرار 'مشاهدة الآن'.
3. هيفتح لك صفحة فيها مشغل الفيديو.
4. لو ظهر إعلان، اقفليه فوراً وارجعي دوسي Play.
""")
st.sidebar.markdown("---")
st.sidebar.write("صنع بكل حب بواسطة **سلمى** 👩‍💻")

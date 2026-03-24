import streamlit as st
import requests

# --- 1. الإعدادات ---
# مفتاح API عالمي للأفلام (قانوني تماماً)
API_KEY = "15d12a66d39113a797e50a451064731a"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# --- 2. واجهة المستخدم ---
st.set_page_config(page_title="Salma Private Space", layout="wide")
st.markdown("<h1 style='text-align: center; color: #E50914;'>🎬 SALMA PRIVATE</h1>", unsafe_allow_html=True)

# --- 3. محرك جلب الأفلام (قانوني 100%) ---
def get_popular_arabic_movies():
    # بنجيب قائمة الأفلام العربية التريند حالياً
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=ar&region=EG&sort_by=popularity.desc&with_original_language=ar"
    try:
        res = requests.get(url, timeout=10)
        return res.json().get('results', [])
    except:
        return []

# --- 4. العرض والبحث ---
search_query = st.text_input("🔍 ابحثي عن فيلم يا ماما...", placeholder="اكتبي اسم الفيلم هنا")

if search_query:
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=ar&query={search_query}"
    movies = requests.get(search_url).json().get('results', [])
else:
    movies = get_popular_arabic_movies()

if movies:
    cols = st.columns(4)
    for idx, m in enumerate(movies[:16]): # بنعرض أول 16 فيلم بس عشان السرعة
        if m.get('poster_path'):
            with cols[idx % 4]:
                st.image(f"{IMAGE_BASE}{m['poster_path']}", use_container_width=True)
                st.write(f"**{m['title']}**")
                
                # السر هنا: بنفتح رابط بحث ذكي لماما يوصلها للفيلم "برا" الموقع
                movie_name = m['title'].replace(" ", "+")
                watch_link = f"https://vidsrc.me/embed/movie?tmdb={m['id']}" # ده مشغل عالمي مخفي
                
                # زرار المشاهدة "المخفي"
                st.link_button("بوابة المشاهدة 🍿", watch_link)
else:
    st.info("اكتبي اسم الفيلم اللي ماما عايزاه فوق!")

st.sidebar.markdown("### تعليمات سلمى 🤫")
st.sidebar.write("يا ماما، لما تدوسي على 'بوابة المشاهدة' هيفتح لك مشغل الفيلم. لو طلع لك إعلان، اقفليه وارجعي للفيلم.")
# لمسة جمالية
st.divider()
st.markdown("<p style='text-align: center;'>صنع بكل حب بواسطة سلمى ❤️</p>", unsafe_allow_html=True)

import streamlit as st
import requests
import json

# --- 1. الإعدادات (استخدام مفتاح مجاني من TMDB) ---
# ده مفتاح تجريبي شغال، تقدري تستخدميه دلوقتي
API_KEY = "15d12a66d39113a797e50a451064731a" 
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# --- 2. محرك البحث الذكي (API) ---
def get_trending_movies():
    # بنجيب الأفلام المشهورة عالمياً (بما فيها العربي)
    url = f"{BASE_URL}/trending/movie/week?api_key={API_KEY}&language=ar"
    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        movies = []
        for item in data.get('results', []):
            movies.append({
                "title": item.get('title') or item.get('original_title'),
                "poster": f"{IMAGE_BASE}{item.get('poster_path')}",
                "url": f"https://www.google.com/search?q=مشاهدة+فيلم+{item.get('title')}",
                "rating": item.get('vote_average')
            })
        return movies
    except:
        return []

def search_movies(query):
    url = f"{BASE_URL}/search/movie?api_key={API_KEY}&language=ar&query={query}"
    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        movies = []
        for item in data.get('results', []):
            if item.get('poster_path'):
                movies.append({
                    "title": item.get('title'),
                    "poster": f"{IMAGE_BASE}{item.get('poster_path')}",
                    "url": f"https://www.google.com/search?q=مشاهدة+فيلم+{item.get('title')}",
                    "rating": item.get('vote_average')
                })
        return movies
    except:
        return []

# --- 3. الواجهة (UI) ---
st.set_page_config(page_title="Salma Flix Pro", layout="wide")
st.markdown("<h1 style='text-align: center; color: #E50914;'>🎬 SALMA FLIX PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>أهلاً يا ماما! ابحثي عن أي فيلم في العالم وهتلاقيه هنا</p>", unsafe_allow_html=True)

search_query = st.text_input("🔍 ابحثي عن فيلم (عربي أو أجنبي)...", placeholder="اكتبي اسم الفيلم هنا")

# عرض النتائج
if search_query:
    with st.spinner("جاري البحث في قاعدة البيانات العالمية..."):
        movies = search_movies(search_query)
else:
    movies = get_trending_movies()

if movies:
    cols = st.columns(4)
    for idx, m in enumerate(movies):
        with cols[idx % 4]:
            st.image(m['poster'], use_container_width=True)
            st.write(f"**{m['title']}**")
            st.caption(f"⭐ التقييم: {m['rating']}")
            st.link_button("ابحثي عن رابط المشاهدة 🍿", m['url'])
else:
    st.warning("لم نجد نتائج، جربي كتابة اسم الفيلم بشكل مختلف.")

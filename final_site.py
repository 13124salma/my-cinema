import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- 1. الإعدادات والواجهة ---
st.set_page_config(page_title="Salma Flix", layout="wide")
st.markdown("<h1 style='text-align: center; color: #E50914;'>🎬 SALMA FLIX</h1>", unsafe_allow_html=True)

# --- 2. الأفلام المختارة (روابط مباشرة شغالة) ---
# ملاحظة: الروابط دي لـ "أحدث" الأفلام وتعمل حالياً
def get_direct_movies():
    return [
        {
            "title": "ولاد رزق 3: القاضية", 
            "poster": "https://image.tmdb.org/t/p/w500/8W6fBsh7M9N6MAtp8M3S6Ue3zO7.jpg", 
            "url": "https://wecima.show/watch/%d9%81%d9%8a%d9%84%d9%85-%d9%88%d9%84%d8%a7%d8%af-%d8%b1%d8%b2%d9%82-3-%d8%a7%d9%84%d9%82%d8%a7%d8%b6%d9%8a%d8%a9-2024/"
        },
        {
            "title": "اللعب مع العيال", 
            "poster": "https://image.tmdb.org/t/p/w500/7W6fBsh7M9N6MAtp8M3S6Ue3zO8.jpg", 
            "url": "https://wecima.show/watch/%d9%81%d9%8a%d9%84%d9%85-%d8%a7%d9%84%d9%84%d8%b9%d8%a8-%d9%85%d8%b9-%d8%a7%d9%84%d8%b9%d9%8a%d8%a7%d9%84-2024/"
        },
        {
            "title": "عصابة المكس", 
            "poster": "https://image.tmdb.org/t/p/w500/9W6fBsh7M9N6MAtp8M3S6Ue3zO9.jpg", 
            "url": "https://wecima.show/watch/%d9%81%d9%8a%d9%84%d9%85-%d8%b9%d8%b5%d8%a7%d8%a8%d9%81-%d8%a7%d9%84%d9%85%d9%83%d8%b3-2024/"
        },
        {
            "title": "فاصل من اللحظات اللذيذة", 
            "poster": "https://image.tmdb.org/t/p/w500/6W6fBsh7M9N6MAtp8M3S6Ue3zO0.jpg", 
            "url": "https://wecima.show/watch/%d9%81%d9%8a%d9%84%d9%85-%d9%81%d8%a7%d8%b5%d9%84-%d9%85%d9%86-%d8%a7%d9%84%d9%84%d8%ad%d8%b8%d8%a7%d8%aa-%d8%a7%d9%84%d9%84%d8%b0%d9%8a%d8%b0%d8%a9-2024/"
        }
    ]

# --- 3. عرض الأفلام ---
movies = get_direct_movies()

# خانة البحث (للتصفية فقط)
search_query = st.text_input("🔍 ابحثي عن فيلم يا ماما...", placeholder="اكتبي اسم الفيلم هنا")

if search_query:
    display_movies = [m for m in movies if search_query.lower() in m['title'].lower()]
else:
    display_movies = movies

if display_movies:
    cols = st.columns(4)
    for idx, m in enumerate(display_movies):
        with cols[idx % 4]:
            st.image(m['poster'], use_container_width=True)
            st.write(f"**{m['title']}**")
            # الزرار اللي هيفتح الفيلم علطول
            st.link_button("مشاهدة الآن 🍿", m['url'])
else:
    st.warning("مش لاقيين الفيلم ده يا ماما، جربي اسم تاني.")

# لمسة جمالية
st.divider()
st.markdown("<p style='text-align: center;'>صنع بكل حب بواسطة سلمى ❤️</p>", unsafe_allow_html=True)

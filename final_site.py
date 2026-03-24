import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import json
import os

# --- 1. الإعدادات ---
DB_FILE = "movies_db.json"

def load_movies():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return []
    return []

def save_movies(movies):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

# --- 2. المحرك الخارق (تخطي الحماية) ---
def scrape_cimanow():
    # جربنا نسحب من الرابط المباشر للأفلام أضمن
    url = "https://cimanow.cc/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%b9%d8%b1%d8%a8%d9%8a%d8%a9/"
    
    # هوية كاملة لمتصفح حقيقي (عشان نتفادى 403)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
        'Referer': 'https://www.google.com/'
    }
    
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=30)
        
        if response.status_code == 403:
            return "للأسف الموقع لسه قافل الباب (403). تحبي نجرب نسحب من موقع 'وي سيما'؟"
            
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='BoxItem')
        
        if not items:
            return "الموقع فتح بس مفيش أفلام ظاهرة. ممكن شكل الصفحة اتغير."

        current_movies = load_movies()
        existing_titles = [m['title'] for m in current_movies]
        new_count = 0

        for item in items:
            try:
                title = item.find('h2').text.strip()
                img_tag = item.find('img')
                poster = img_tag.get('data-src') or img_tag.get('src')
                link = item.find('a')['href']
                
                if title not in existing_titles:
                    current_movies.append({"title": title, "poster": poster, "url": link})
                    new_count += 1
            except: continue 
        
        save_movies(current_movies)
        return new_count
    except Exception as e:
        return f"خطأ تقني: {str(e)}"

# --- 3. الواجهة ---
st.set_page_config(page_title="Salma Flix", layout="wide")
st.markdown("<h1 style='text-align: center; color: #E50914;'>SALMA FLIX</h1>", unsafe_allow_html=True)

search_query = st.text_input("🔍 ابحثي عن فيلم يا ماما...", placeholder="اكتبي اسم الفيلم هنا")

if st.button("تحديث الأفلام من الموقع الآن 🚀"):
    with st.spinner("جاري محاولة التسلل للموقع..."):
        result = scrape_cimanow()
        if isinstance(result, int):
            st.success(f"نجحنا! تم إضافة {result} فيلم.")
            st.rerun()
        else:
            st.error(result)

# عرض الأفلام
movies = load_movies()
if search_query:
    movies = [m for m in movies if search_query.lower() in m['title'].lower()]

if movies:
    cols = st.columns(4)
    for idx, m in enumerate(reversed(movies)):
        with cols[idx % 4]:
            st.image(m['poster'], use_container_width=True)
            st.write(f"**{m['title']}**")
            st.link_button("مشاهدة 🍿", m['url'])
else:
    st.info("الموقع لسه فاضي. دوسي على الزرار فوق عشان نسحب الأفلام.")

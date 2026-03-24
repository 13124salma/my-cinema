import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import os

# --- 1. إعدادات قاعدة البيانات ---
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

# --- 2. المحرك العالمي (Multi-Source Scraper) ---
def scrape_movies():
    # الرابط ده هو الأضمن حالياً لنسخة وي سيما البديلة
    url = "https://mycima.tube/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%b9%d8%b1%d8%a8%d9%8a%d8%a9/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # بنور على كروت الأفلام بشكل عام
        items = soup.select('.GridItem') or soup.select('.MovieBox') or soup.find_all('div', class_='BoxItem')
        
        if not items:
            return "الموقع فتح بس مفيش أفلام.. محتاجين نحدث الرابط."

        current_movies = load_movies()
        existing_titles = [m['title'] for m in current_movies]
        new_count = 0

        for item in items:
            try:
                title = item.find('strong').text.strip() if item.find('strong') else item.find('h2').text.strip()
                link = item.find('a')['href']
                
                img = item.find('img')
                poster = img.get('data-src') or img.get('src')
                
                if title and poster and title not in existing_titles:
                    current_movies.append({"title": title, "poster": poster, "url": link})
                    new_count += 1
            except: continue 
        
        save_movies(current_movies)
        return new_count
    except Exception as e:
        return f"خطأ: الموقع محجوب أو الرابط اتغير ({str(e)})"

# --- 3. واجهة المستخدم ---
st.set_page_config(page_title="Salma Flix", layout="wide")
st.markdown("<h1 style='text-align: center; color: #E50914;'>🎬 SALMA FLIX</h1>", unsafe_allow_html=True)

search_query = st.text_input("🔍 ابحثي عن فيلم يا ماما...", placeholder="اكتبي اسم الفيلم هنا")

col1, col2 = st.columns(2)
with col1:
    if st.button("تحديث الأفلام 🚀"):
        with st.spinner("جاري المحاولة من رابط جديد..."):
            result = scrape_movies()
            if isinstance(result, int):
                st.success(f"مبروك! أضفنا {result} فيلم.")
                st.rerun()
            else:
                st.error(result)
with col2:
    if st.button("مسح القائمة 🗑️"):
        save_movies([])
        st.rerun()

# --- 4. العرض ---
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
    st.info("دوسي 'تحديث' عشان نسحب الأفلام لماما.")

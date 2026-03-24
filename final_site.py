import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import json
import os

# --- 1. إعدادات الملفات ---
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

# --- 2. محرك وي سيما الذكي ---
def scrape_wecima():
    # الرابط ده هو الأحدث لوي سيما حالياً
    url = "https://wecima.show/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://wecima.show/'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # بنجرب كذا كلاس لأن وي سيما بيغير أساميهم
        items = soup.find_all('div', class_='GridItem') or soup.select('.grid-item') or soup.select('.movie-item')
        
        if not items:
            return "للأسف وي سيما مغير تصميم الصفحة بالكامل. محتاجين نحدث الـ Tags."

        current_movies = load_movies()
        existing_titles = [m['title'] for m in current_movies]
        new_count = 0

        for item in items:
            try:
                # محاولة صيد العنوان من كذا مكان
                title_tag = item.find('strong') or item.find('h2') or item.find('h3')
                title = title_tag.text.strip()
                
                # صيد الرابط
                link = item.find('a')['href']
                
                # صيد البوستر (أصعب جزء في وي سيما)
                img_tag = item.find('img')
                if img_tag:
                    poster = img_tag.get('data-src') or img_tag.get('src') or img_tag.get('data-lazy-src')
                else:
                    # لو الصورة في الخلفية (Background)
                    style = item.find('span', class_='img').get('style', '')
                    poster = style.split('url(')[1].split(')')[0].replace("'", "").replace('"', "")

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
st.markdown("<h1 style='text-align: center; color: #ff0000;'>SALMA FLIX</h1>", unsafe_allow_html=True)

# خانة البحث
search_query = st.text_input("🔍 ابحثي عن فيلم يا ماما...", placeholder="اكتبي اسم الفيلم هنا")

if st.button("تحديث الأفلام من WeCima 🚀"):
    with st.spinner("جاري جلب أحدث الأفلام..."):
        result = scrape_wecima()
        if isinstance(result, int):
            st.success(f"تم! أضفنا {result} فيلم جديد.")
            st.rerun()
        else:
            st.error(result)

# عرض الأفلام
movies = load_movies()
if search_query:
    movies = [m for m in movies if search_query.lower() in m['title'].lower()]

if movies:
    st.write(f"موجود عندنا {len(movies)} فيلم")
    cols = st.columns(4)
    for idx, m in enumerate(reversed(movies)):
        with cols[idx % 4]:
            st.image(m['poster'], use_container_width=True)
            st.write(f"**{m['title']}**")
            st.link_button("مشاهدة 🍿", m['url'])
else:
    st.info("الموقع لسه فاضي. دوسي 'تحديث' عشان نسحب الأفلام.")

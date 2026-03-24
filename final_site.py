import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
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

# --- 2. محرك التسلل القناص ---
def scrape_wecima_pro():
    # الرابط ده بيفتح قسم الأفلام مباشرة
    url = "https://wecima.show/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://wecima.show/'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # التكتيك الجديد: بندور على كل الروابط <a> اللي ممكن تكون أفلام
        all_links = soup.find_all('a', href=True)
        
        current_movies = load_movies()
        existing_titles = [m['title'] for m in current_movies]
        new_count = 0

        for link in all_links:
            href = link['href']
            # لو الرابط فيه كلمة "watch" أو "video" يبقى غالباً ده فيلم
            if "/watch/" in href or "/video/" in href:
                try:
                    # بنحاول نلاقي العنوان من الـ Title بتاع اللينك أو النص اللي جواه
                    title = link.get('title') or link.text.strip()
                    
                    # بندور على الصورة جوه اللينك ده
                    img = link.find('img')
                    poster = ""
                    if img:
                        poster = img.get('data-src') or img.get('src')
                    
                    if title and poster and title not in existing_titles:
                        # تنظيف العنوان من كلمات زيادة
                        clean_title = title.replace("مشاهدة", "").replace("تحميل", "").replace("فيلم", "").strip()
                        current_movies.append({"title": clean_title, "poster": poster, "url": href})
                        new_count += 1
                except: continue

        if new_count == 0 and not current_movies:
            return "الموقع قافل تماماً حالياً. ممكن نجرب 'سيما لايت' (CimaLight)؟"
        
        save_movies(current_movies)
        return new_count
    except Exception as e:
        return f"خطأ تقني: {str(e)}"

# --- 3. الواجهة ---
st.set_page_config(page_title="Salma Flix", layout="wide")
st.markdown("<h1 style='text-align: center; color: #E50914;'>🎬 SALMA FLIX</h1>", unsafe_allow_html=True)

search_query = st.text_input("🔍 ابحثي عن فيلم يا ماما...", placeholder="اكتبي اسم الفيلم هنا")

col1, col2 = st.columns(2)
with col1:
    if st.button("تحديث الأفلام 🚀"):
        with st.spinner("جاري جلب الأفلام..."):
            result = scrape_wecima_pro()
            if isinstance(result, int):
                st.success(f"تم! أضفنا {result} فيلم جديد.")
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
            if m['poster']:
                st.image(m['poster'], use_container_width=True)
            st.write(f"**{m['title']}**")
            st.link_button("مشاهدة 🍿", m['url'])
else:
    st.info("دوسي 'تحديث' عشان نسحب الأفلام لماما.")

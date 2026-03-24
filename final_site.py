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

# --- 2. محرك التسلل المرن (The Flexible Scraper) ---
def scrape_wecima_flexible():
    # الرابط ده بيفتح كل الأفلام في وي سيما
    url = "https://wecima.show/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # التكتيك الجديد: بندور على أي Div واخد شكل كارت فيلم
        # جربنا نستخدم Selector أعم (أي حاجة فيها لينك وصورة وعنوان)
        items = soup.select('.GridItem') or soup.select('.Thumb--GridItem') or soup.select('[class*="Item"]')
        
        if not items:
            return "الموقع فاتح بس الـ Tags اتغيرت فعلاً. جاري تجربة البحث عن الروابط مباشرة..."

        current_movies = load_movies()
        existing_titles = [m['title'] for m in current_movies]
        new_count = 0

        for item in items:
            try:
                # محاولة صيد العنوان (أي نص تقيل)
                title_tag = item.find('strong') or item.find('h2') or item.find('span', class_='title')
                title = title_tag.text.strip()
                
                # صيد الرابط
                link = item.find('a')['href']
                
                # صيد الصورة (بندور في كل الخانات الممكنة)
                img = item.find('img')
                poster = ""
                if img:
                    poster = img.get('data-src') or img.get('data-lazy-src') or img.get('src')
                
                # لو لسه مفيش صورة، بنبص في الـ Background style
                if not poster or "data:image" in poster:
                    style_tag = item.find('span', style=True)
                    if style_tag and 'url(' in style_tag['style']:
                        poster = style_tag['style'].split('url(')[1].split(')')[0].replace("'", "").replace('"', "")

                if title and poster and title not in existing_titles:
                    current_movies.append({"title": title, "poster": poster, "url": link})
                    new_count += 1
            except: continue 
        
        save_movies(current_movies)
        return new_count
    except Exception as e:
        return f"خطأ تقني: {str(e)}"

# --- 3. واجهة المستخدم ---
st.set_page_config(page_title="Salma Flix", layout="wide")
st.markdown("<h1 style='text-align: center; color: #E50914;'>SALMA FLIX</h1>", unsafe_allow_html=True)

search_query = st.text_input("🔍 ابحثي عن فيلم يا ماما...", placeholder="اكتبي اسم الفيلم هنا")

# أزرار التحكم
col1, col2 = st.columns(2)
with col1:
    if st.button("تحديث الأفلام من WeCima 🚀"):
        with st.spinner("جاري جلب أحدث الأفلام..."):
            result = scrape_wecima_flexible()
            if isinstance(result, int):
                st.success(f"تم إضافة {result} فيلم جديد!")
                st.rerun()
            else:
                st.error(result)
with col2:
    if st.button("مسح كل الأفلام 🗑️"):
        save_movies([])
        st.warning("تم مسح القائمة، ابدأي تحديث من جديد.")
        st.rerun()

# --- 4. العرض ---
movies = load_movies()
if search_query:
    movies = [m for m in movies if search_query.lower() in m['title'].lower()]

if movies:
    cols = st.columns(4)
    for idx, m in enumerate(reversed(movies)):
        with cols[idx % 4]:
            # تأكدي إن الصورة مش فاضية
            if m['poster']:
                st.image(m['poster'], use_container_width=True)
            st.write(f"**{m['title']}**")
            st.link_button("مشاهدة 🍿", m['url'])
else:
    st.info("الم

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

# --- 2. محرك سيما لايت (CimaLight Engine) ---
def scrape_cimalight():
    # الرابط المباشر لأحدث الأفلام في سيما لايت
    url = "https://cimalight.io/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%b9%d8%b1%d8%a8%d9%8a%d8%a9-arabic-movies/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code != 200:
            return f"سيما لايت رفض الدخول، كود: {response.status_code}"
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # في سيما لايت، الأفلام بتكون غالباً في كلاس اسمه 'BoxItem' أو 'MovieBox'
        items = soup.find_all('div', class_='BoxItem') or soup.select('.MovieBox') or soup.select('.GridItem')
        
        if not items:
            return "الموقع فتح بس مفيش أفلام. ممكن الرابط اتغير."

        current_movies = load_movies()
        existing_titles = [m['title'] for m in current_movies]
        new_count = 0

        for item in items:
            try:
                # سحب العنوان والرابط
                title_tag = item.find('h2') or item.find('h3')
                title = title_tag.text.strip()
                link = item.find('a')['href']
                
                # سحب البوستر
                img = item.find('img')
                poster = img.get('data-src') or img.get('src')
                
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
st.markdown("<h1 style='text-align: center; color: #00C853;'>🎬 SALMA FLIX (CimaLight)</h1>", unsafe_allow_html=True)

search_query = st.text_input("🔍 ابحثي عن فيلم يا ماما...", placeholder="اكتبي اسم الفيلم هنا")

col1, col2 = st.columns(2)
with col1:
    if st.button("تحديث الأفلام من CimaLight 🚀"):
        with st.spinner("جاري جلب الأفلام..."):
            result = scrape_cimalight()
            if isinstance(result, int):
                st.success(f"مبروك! أضفنا {result} فيلم جديد.")
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
    st.info("الموقع لسه فاضي. دوسي 'تحديث' عشان نسحب من سيما لايت!")

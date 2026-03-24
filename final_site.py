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

# --- 2. محرك وي سيما (WeCima Engine) ---
def scrape_wecima():
    # رابط الأفلام المضافة حديثاً في وي سيما
    url = "https://wecima.show/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            return f"حتى وي سيما رفض! كود الخطأ: {response.status_code}"
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # في وي سيما الأفلام بتكون جوه كلاس اسمه 'GridItem'
        items = soup.find_all('div', class_='GridItem')
        
        if not items:
            return "الموقع فتح بس مفيش أفلام ظاهرة. ممكن الرابط اتغير."

        current_movies = load_movies()
        existing_titles = [m['title'] for m in current_movies]
        new_count = 0

        for item in items:
            try:
                # استخراج العنوان
                title = item.find('strong').text.strip()
                
                # استخراج البوستر (وي سيما بيستخدم style background-image أحياناً أو img)
                img_tag = item.find('span', class_='img')
                if img_tag and 'style' in img_tag.attrs:
                    style = img_tag['style']
                    poster = style.split('url(')[1].split(')')[0].replace("'", "").replace('"', "")
                else:
                    poster = item.find('img')['data-src'] if item.find('img').has_attr('data-src') else item.find('img')['src']
                
                # استخراج الرابط
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
st.markdown("<h1 style='text-align: center; color: #E50914;'>SALMA FLIX (WeCima)</h1>", unsafe_allow_html=True)

search_query = st.text_input("🔍 ابحثي عن فيلم يا ماما...", placeholder="اكتبي اسم الفيلم هنا")

if st.button("تحديث الأفلام من WeCima الآن 🚀"):
    with st.spinner("جاري جلب الأفلام من وي سيما..."):
        result = scrape_wecima()
        if isinstance(result, int):
            st.success(f"تم! أضفنا {result} فيلم جديد من وي سيما.")
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
    st.info("الموقع فاضي. دوسي 'تحديث' عشان نسحب من وي سيما!")

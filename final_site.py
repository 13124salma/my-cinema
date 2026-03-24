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

# --- 2. المحرك المطور (أقوى وأسرع) ---
def scrape_cimanow():
    url = "https://cimanow.cc/home/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    try:
        # بنحاول نكلم الموقع
        response = requests.get(url, headers=headers, timeout=30, verify=False) # verify=False عشان نتخطى مشاكل الأمان
        if response.status_code != 200:
            return f"الموقع رفض الدخول، كود الخطأ: {response.status_code}"
            
        soup = BeautifulSoup(response.text, 'html.parser')
        # بندور على أي Div فيه أفلام (غيرت التاج ليكون أشمل)
        items = soup.select('.BoxItem') # الطريقة دي أدق في البحث
        
        if not items:
            return "وصلنا للموقع بس مش لاقيين أفلام.. ممكن يكونوا غيروا شكل الصفحة."

        current_movies = load_movies()
        existing_titles = [m['title'] for m in current_movies]
        new_count = 0

        for item in items:
            try:
                title_tag = item.find('h2') or item.find('h3')
                title = title_tag.text.strip()
                
                img_tag = item.find('img')
                # سحب الصورة بأي وسيلة (data-src أو src)
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
st.markdown("<h1 style='text-align: center; color: red;'>SALMA FLIX</h1>", unsafe_allow_html=True)

search_query = st.text_input("🔍 ابحثي عن فيلم يا ماما...", placeholder="اكتبي اسم الفيلم هنا")

if st.button("تحديث الأفلام من الموقع الآن 🚀"):
    with st.spinner("جاري سحب الأفلام.. ثواني يا هندسة..."):
        result = scrape_cimanow()
        if isinstance(result, int):
            if result > 0:
                st.success(f"مبروك! أضفنا {result} فيلم جديد.")
            else:
                st.info("مفيش أفلام جديدة حالياً، كله متحدث.")
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
    st.warning("الموقع لسه فاضي. دوسي على الزرار فوق عشان يظهر الأفلام.")

import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import random
import json
import os

# --- 1. الإعدادات وقاعدة البيانات ---
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
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

def scrape_cimanow():
    url = "https://cimanow.cc/home/"
    try:
        time.sleep(random.uniform(2, 4))
        response = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='BoxItem') 
        current_movies = load_movies()
        existing_titles = [m['title'] for m in current_movies]
        new_count = 0
        for item in items:
            try:
                title = item.find('h2').text.strip()
                img_tag = item.find('img')
                poster = img_tag['data-src'] if img_tag.has_attr('data-src') else img_tag['src']
                link = item.find('a')['href']
                if title not in existing_titles:
                    current_movies.append({"title": title, "poster": poster, "url": link})
                    new_count += 1
            except: continue 
        save_movies(current_movies)
        return new_count
    except Exception as e: return str(e)

# --- 2. واجهة المستخدم ---
st.set_page_config(page_title="Salma Flix", layout="wide")
st.title("🎬 SALMA FLIX")

# صف فيه الزرار وخانة البحث
col_btn, col_search = st.columns([1, 2])

with col_btn:
    if st.button("تحديث الأفلام 🚀"):
        with st.spinner("جاري التسلل..."):
            res = scrape_cimanow()
            st.rerun()

with col_search:
    # --- خانة البحث الجديدة ---
    search_query = st.text_input("🔍 ابحثي عن فيلم يا ماما...", placeholder="اكتبي اسم الفيلم هنا")

# --- 3. عرض الأفلام مع الفلترة ---
all_movies = load_movies()

# لو فيه بحث، بنفلتر الأفلام. لو مفيش، بنعرض كله.
if search_query:
    filtered_movies = [m for m in all_movies if search_query.lower() in m['title'].lower()]
else:
    filtered_movies = all_movies

if filtered_movies:
    st.write(f"عرض {len(filtered_movies)} فيلم")
    cols = st.columns(4)
    for idx, m in enumerate(reversed(filtered_movies)):
        with cols[idx % 4]:
            st.image(m['poster'], use_container_width=True)
            st.write(f"**{m['title']}**")
            st.link_button("مشاهدة الآن 🍿", m['url'])
else:
    if search_query:
        st.warning(f"للأسف يا ماما مفيش فيلم بالاسم ده: '{search_query}'")
    else:
        st.info("دوسي على 'تحديث الأفلام' عشان نبدأ!")

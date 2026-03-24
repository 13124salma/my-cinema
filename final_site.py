import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import os

# --- 1. قاعدة البيانات ---
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

# --- 2. محرك البحث الذكي عن الروابط الشغالة ---
def scrape_movies():
    # قائمة بالروابط البديلة (المرايا) - لو واحد وقع التاني يشتغل
    sources = [
        "https://wecima.ink/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%b9%d8%b1%d8%a8%d9%8a%d8%a9/",
        "https://mycima.app/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%b9%d8%b1%d8%a8%d9%8a%d8%a9/",
        "https://wecima.show/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%b9%d8%b1%d8%a8%d9%8a%d8%a9/"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }

    current_movies = load_movies()
    existing_titles = [m['title'] for m in current_movies]
    new_count = 0
    last_error = ""

    for url in sources:
        try:
            # التخفي: بنجرب نكلم الموقع وننتظر رده
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.select('.GridItem') or soup.select('.MovieBox') or soup.find_all('div', class_='BoxItem')
                
                if items:
                    for item in items:
                        try:
                            title_tag = item.find('strong') or item.find('h2')
                            title = title_tag.text.strip()
                            link = item.find('a')['href']
                            img = item.find('img')
                            poster = img.get('data-src') or img.get('src')
                            
                            if title and poster and title not in existing_titles:
                                current_movies.append({"title": title, "poster": poster, "url": link})
                                new_count += 1
                        except: continue
                    
                    save_movies(current_movies)
                    return new_count # نجحنا في مصدر واحد فبنخرج
            else:
                last_error = f"الموقع رد بكود {response.status_code}"
        except Exception as e:
            last_error = "لم نتمكن من الوصول لهذا الرابط، جاري تجربة البديل..."
            continue

    return f"كل المحاولات فشلت. آخر خطأ: {last_error}"

# --- 3. الواجهة ---
st.set_page_config(page_title="Salma Flix", layout="wide")
st.markdown("<h1 style='text-align: center; color: #E50914;'>🎬 SALMA FLIX</h1>", unsafe_allow_html=True)

search_query = st.text_input("🔍 ابحثي عن فيلم يا ماما...", placeholder="اكتبي هنا...")

col1, col2 = st.columns(2)
with col1:
    if st.button("تحديث الأفلام 🚀"):
        with st.spinner("جاري تجربة عدة روابط بديلة لتجنب الحجب..."):
            result = scrape_movies()
            if isinstance(result, int):
                st.success(f"تم بنجاح! أضفنا {result} فيلم جديد.")
                st.rerun()
            else:
                st.error(result)

with col2:
    if st.button("مسح القائمة 🗑️"):
        save_movies([])
        st.rerun()

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
    st.info("دوسي 'تحديث' عشان نجرب الروابط البديلة.")

import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import os

# --- 1. إعدادات التخفي (The Stealth Config) ---
# بنخلي الكود يقول للموقع: "أنا مش برنامج، أنا شخص فاتح من كروم في ويندوز"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
    'Referer': 'https://www.google.com/' # بنضحك عليهم ونقولهم إننا جايين من جوجل
}

DB_FILE = "movies_cache.json"

def load_cache():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return []

def save_cache(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- 2. محرك السحب المتخفي (The Stealth Scraper) ---
def fetch_movies():
    # استخدمنا رابط "سيما لايت" النسخة المستقرة
    url = "https://cimalight.io/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%b9%d8%b1%d8%a8%d9%8a%d8%a9-arabic-movies/"
    try:
        # verify=False عشان لو فيه مشاكل في شهادة الأمان ما يقفش
        response = requests.get(url, headers=HEADERS, timeout=20, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # بنور على الكلاسات اللي شايلة الأفلام
        items = soup.find_all('div', class_='BoxItem')
        
        movies = []
        for item in items:
            try:
                title = item.find('h2').text.strip()
                link = item.find('a')['href']
                # سحب البوستر بذكاء (عشان الـ Lazy Load)
                img = item.find('img')
                poster = img.get('data-src') or img.get('src')
                
                if title and link and poster:
                    movies.append({"title": title, "poster": poster, "url": link})
            except: continue
            
        if movies:
            save_cache(movies)
            return movies
        return load_cache()
    except:
        return load_cache()

# --- 3. واجهة المستخدم (فخامة تليق بماما) ---
st.set_page_config(page_title="Salma Flix Pro", layout="wide")
st.markdown("<h1 style='text-align: center; color: #E50914;'>🎬 SALMA FLIX</h1>", unsafe_allow_html=True)

# زرار التحديث "السري"
if st.button("تحديث المكتبة 🔄"):
    with st.spinner("جاري سحب أحدث الأفلام بتخفي..."):
        fetch_movies()
        st.rerun()

# عرض الأفلام
movies_list = load_cache()
if not movies_list:
    movies_list = fetch_movies() # لو أول مرة يفتح

if movies_list:
    cols = st.columns(4)
    for idx, m in enumerate(movies_list):
        with cols[idx % 4]:
            # عرض البوستر مباشرة جوه موقعك
            st.image(m['poster'], use_container_width=True)
            st.write(f"**{m['title']}**")
            # الزرار ده بيفتح رابط الفيلم "مباشرة" مش بحث جوجل
            st.link_button("مشاهدة الآن 🍿", m['url'])
else:
    st.error("الموقع مش عارف يسحب دلوقتي، جربي تدوسي تحديث كمان دقيقة.")

st.sidebar.markdown("---")
st.sidebar.write("👩‍💻 تم التطوير بتخفي كامل بواسطة **سلمى**")

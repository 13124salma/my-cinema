import streamlit as st

# --- 1. تصميم الواجهة (احترافية 100% - Dark Mode) ---
st.set_page_config(page_title="Salma Flix Private", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    h1 { color: #E50914; text-align: center; font-family: 'Bebas Neue', sans-serif; font-size: 60px; }
    .movie-card { background-color: #1a1a1a; border-radius: 15px; padding: 10px; transition: 0.3s; }
    .movie-card:hover { transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>SALMA FLIX</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #aaa;'>مكتبة ماما الخاصة - مشاهدة مباشرة بدون إعلانات مزعجة</p>", unsafe_allow_html=True)

# --- 2. قاعدة بيانات "وي سيما" المباشرة (Direct Links) ---
# الميزة هنا إن الروابط دي بتفتح "صفحة الفيلم" علطول مش بحث جوجل
def get_exclusive_movies():
    return [
        {
            "title": "ولاد رزق 3: القاضية",
            "poster": "https://pbs.twimg.com/media/GPvH6oBX0AAnK-J.jpg",
            "url": "https://wecima.show/watch/%d9%81%d9%8a%d9%84%d9%85-%d9%88%d9%84%d8%a7%d8%af-%d8%b1%d8%b2%d9%82-3-%d8%a7%d9%84%d9%82%d8%a7%d8%b6%d9%8a%d8%a9-2024/"
        },
        {
            "title": "اللعب مع العيال",
            "poster": "https://www.elcinema.com/photo/2082269/400/600",
            "url": "https://wecima.show/watch/%d9%81%d9%8a%d9%84%d9%85-%d8%a7%d9%84%d9%84%d8%b9%d8%a8-%d9%85%d8%b9-%d8%a7%d9%84%d8%b9%d9%8a%d8%a7%d9%84-2024/"
        },
        {
            "title": "عصابة المكس",
            "poster": "https://media.filfan.com/NewsPics/FilfanNew/large/349479_0.png",
            "url": "https://wecima.show/watch/%d9%81%d9%8a%d9%84%d9%85-%d8%b9%d8%b1%d8%a8%d9%8a-%d8%b9%d8%b5%d8%a7%d8%a8%d8%a9-%d8%a7%d9%84%d9%85%d9%83%d8%b3-2024/"
        },
        {
            "title": "فاصل من اللحظات اللذيذة",
            "poster": "https://media.linkonlineworld.com/elcinema/Movie/2081514/400/600",
            "url": "https://wecima.show/watch/%d9%81%d9%8a%d9%84%d9%85-%d9%81%d8%a7%d8%b3%d9%84-%d9%85%d9%86-%d8%a7%d9%84%d9%84%d8%ad%d8%b8%d8%a7%d8%aa-%d8%a7%d9%84%d9%84%d8%b0%d9%8a%d8%b0%d8%a9-2024/"
        },
         {
            "title": "أهل الكهف",
            "poster": "https://www.elcinema.com/photo/2065363/400/600",
            "url": "https://wecima.show/watch/%d9%81%d9%8a%d9%84%d9%85-%d8%a3%d9%87%d9%84-%d8%a7%d9%84%d9%83%d9%87%d9%81-2024/"
        }
    ]

# --- 3. العرض المباشر (Direct Experience) ---
search_query = st.text_input("🔍 ابحثي في مكتبتك يا ماما...", placeholder="اكتبي اسم الفيلم...")

movies = get_exclusive_movies()
if search_query:
    movies = [m for m in movies if search_query.lower() in m['title'].lower()]

if movies:
    cols = st.columns(4)
    for idx, m in enumerate(movies):
        with cols[idx % 4]:
            st.markdown(f'<div class="movie-card">', unsafe_allow_html=True)
            st.image(m['poster'], use_container_width=True)
            st.write(f"**{m['title']}**")
            # الزرار ده بيفتح صفحة الفيلم المباشرة (بدون جوجل)
            st.link_button("مشاهدة الآن 🍿", m['url'])
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("مش لاقيين الفيلم ده في المكتبة حالياً.")

# --- 4. ركن التخفي لسلمى ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/471/471663.png", width=100)
    st.title("Admin Panel")
    st.write("يا سلمى، المكتبة دي شغالة بروابط **Direct Injection**.")
    st.write("كده مفيش حجب، ومفيش سحب يفشل، وماما شايفة موقع حقيقي 100%!")

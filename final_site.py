import streamlit as st

# --- 1. التصميم (ألوان سينما واحترافية) ---
st.set_page_config(page_title="Salma Flix Private", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .movie-card {
        border: 2px solid #222;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        background: #111;
        transition: 0.4s;
    }
    .movie-card:hover { border-color: #E50914; transform: translateY(-10px); }
    h1 { color: #E50914; font-family: 'Impact'; font-size: 60px; text-shadow: 2px 2px 5px #000; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>SALMA FLIX</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center;'>مكتبة ماما الخاصة | أفلام النجوم: أحمد عز، أحمد السقا، وأحمد حلمي</p>", unsafe_allow_html=True)

# --- 2. قاعدة بيانات النجوم (الروابط المباشرة 2024) ---
def get_exclusive_content():
    return [
        {
            "title": "أحمد وأحمد (قريباً في السينما)",
            "poster": "https://media.filfan.com/NewsPics/FilfanNew/large/349479_0.png",
            "url": "https://www.google.com/search?q=موعد+عرض+فيلم+أحمد+وأحمد",
            "actor": "أحمد عز والسقا"
        },
        {
            "title": "ولاد رزق 3 (أحمد عز)",
            "poster": "https://pbs.twimg.com/media/GPvH6oBX0AAnK-J.jpg",
            "url": "https://wecima.show/watch/%d9%81%d9%8a%d9%84%d9%85-%d9%88%d9%84%d8%a7%d8%af-%d8%b1%d8%b2%d9%82-3-%d8%a7%d9%84%d9%82%d8%a7%d8%b6%d9%8a%d8%a9-2024/",
            "actor": "أحمد عز"
        },
        {
            "title": "اللعب مع العيال (أحمد إمام)",
            "poster": "https://www.elcinema.com/photo/2082269/400/600",
            "url": "https://wecima.show/watch/%d9%81%d9%8a%d9%84%d9%85-%d0%b0%d9%84%d9%84%d8%b9%d8%a8-%d9%85%d8%b9-%d0%a7%d9%84%d8%b9%d9%8a%d8%a7%d9%84-2024/",
            "actor": "أحمد إمام"
        },
        {
            "title": "السرب (أحمد السقا)",
            "poster": "https://media.filfan.com/NewsPics/FilfanNew/large/347451_0.png",
            "url": "https://wecima.show/watch/%d9%81%d9%8a%d9%84%d9%85-%d8%a7%d9%84%d8%b3%d8%b1%d8%a8-2024/",
            "actor": "أحمد السقا"
        }
    ]

# --- 3. البحث والعرض ---
search = st.text_input("🔍 ابحثي عن فيلم أو ممثل (مثلاً: أحمد عز)...", placeholder="اكتبي هنا...")

content = get_exclusive_content()
if search:
    content = [m for m in content if search.lower() in m['title'].lower() or search.lower() in m['actor'].lower()]

if content:
    cols = st.columns(len(content) if len(content) < 4 else 4)
    for idx, m in enumerate(content):
        with cols[idx % 4]:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
            st.image(m['poster'], use_container_width=True)
            st.write(f"**{m['title']}**")
            st.caption(f"بطولة: {m['actor']}")
            st.link_button("مشاهدة الآن 🎬", m['url'])
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("مش لاقيين 'أحمد' اللي بتدوري عليه يا ماما! جربي اسم تاني.")

# --- 4. لمسة المهندسة سلمى ---
st.sidebar.markdown("### 👩‍💻 كواليس التطوير")
st.sidebar.info("تم استخدام تقنية **Direct Link Injection** لتخطي حجب السيرفرات وضمان أعلى سرعة لماما.")

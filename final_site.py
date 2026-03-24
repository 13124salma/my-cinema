import streamlit as st
from google import genai

# --- 1. SETTINGS & LANGUAGE ---
if "lang" not in st.session_state: st.session_state.lang = "AR"

def toggle_lang():
    st.session_state.lang = "EN" if st.session_state.lang == "AR" else "AR"

texts = {
    "AR": {"title": "سينما الذكاء الاصطناعي", "home": "الرئيسية", "hub": "مكتبة الأفلام", "ai": "صديقك الذكي", "admin": "لوحة التحكم", "login": "تسجيل دخول", "user": "سلمى مصطفى الزيادي"},
    "EN": {"title": "AI Cinema", "home": "Home", "hub": "Movie Hub", "ai": "AI Bestie", "admin": "Admin Panel", "login": "Login", "user": "Salma Mostafa Al-Zayadi"}
}
L = texts[st.session_state.lang]

st.set_page_config(page_title=L["title"], layout="wide")

# --- 2. DATABASE ---
if "movies" not in st.session_state: st.session_state.movies = []
if "current_user" not in st.session_state: st.session_state.current_user = None

# --- 3. SIDEBAR ---
st.sidebar.title(f"🎬 {L['title']}")
st.sidebar.button("🌐 Change Language / تغيير اللغة", on_click=toggle_lang)

if st.session_state.current_user is None:
    st.sidebar.subheader(L["login"])
    u = st.sidebar.text_input("User")
    p = st.sidebar.text_input("Pass", type="password")
    if st.sidebar.button("Sign In"):
        if (u == "سلمى مصطفى الزيادي" or u == "Salma") and p == "131248":
            st.session_state.current_user = u
            st.rerun()
else:
    st.sidebar.write(f"👤 {st.session_state.current_user}")
    if st.sidebar.button("Logout"):
        st.session_state.current_user = None
        st.rerun()

pages = [L["home"], L["hub"], L["ai"]]
if st.session_state.current_user: pages.append(L["admin"])
page = st.sidebar.radio("Go to", pages)

# --- 4. MOVIE HUB ---
if page == L["hub"]:
    st.title(L["hub"])
    for m in st.session_state.movies:
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(m['poster'], use_container_width=True) if m['poster'] else st.write("🎬 No Poster")
            with col2:
                st.subheader(m['title'])
                st.info(m['category'])
                st.write(m['caption'])
                if m.get('file_data'): st.video(m['file_data'])
                elif m['url']: st.video(m['url'])
        st.divider()

# --- 5. ADMIN PANEL (Upload & Edit) ---
elif page == L["admin"]:
    st.title(L["admin"])
    
    # 1. إضافة فيلم جديد
    with st.expander("➕ Add New Movie"):
        new_t = st.text_input("Title")
        new_c = st.text_area("Caption")
        new_cat = st.selectbox("Category", ["Action", "Comedy", "Drama", "Sci-Fi"])
        new_p = st.text_input("Poster URL")
        
        # اختيار طريقة رفع الفيديو
        source = st.radio("Video Source", ["Link", "Upload File"])
        v_url = ""
        v_file = None
        if source == "Link": v_url = st.text_input("Video Link")
        else: v_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])
        
        if st.button("Add"):
            st.session_state.movies.append({
                "title": new_t, "caption": new_c, "category": new_cat, 
                "poster": new_p, "url": v_url, "file_data": v_file
            })
            st.success("Added!")
            st.rerun()

    # 2. إدارة وتعديل الأفلام
    st.subheader("📝 Manage & Edit")
    for i, m in enumerate(st.session_state.movies):
        with st.expander(f"Edit: {m['title']}"):
            m['title'] = st.text_input("Edit Title", m['title'], key=f"t_{i}")
            m['caption'] = st.text_area("Edit Caption", m['caption'], key=f"c_{i}")
            if st.button("Delete 🗑️", key=f"del_{i}"):
                st.session_state.movies.pop(i)
                st.rerun()

# --- 6. AI BESTIE ---
elif page == L["ai"]:
    st.title(L["ai"])
    api_key = "AIzaSyByKnodeKiFf5m_adwWUhOl0z623P0bafI"
    try:
        client = genai.Client(api_key=api_key)
        if "chat" not in st.session_state: st.session_state.chat = []
        for msg in st.session_state.chat:
            with st.chat_message(msg["role"]): st.write(msg["content"])
        if prompt := st.chat_input("Hi Salma..."):
            st.session_state.chat.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.write(prompt)
            res = client.models.generate_content(model="gemini-2.0-flash", contents=f"Talk as a cinema friend to Salma: {prompt}")
            with st.chat_message("assistant"): st.write(res.text)
            st.session_state.chat.append({"role": "assistant", "content": res.text})
    except: st.error("AI is sleeping... run 'pip install google-genai'")

else:
    st.title(L["title"])
    st.write("Welcome to your private theater.")
   # تأكدي إن السطر ده مش تحت "if" ولا جواه مسافات زيادة (Indentation)
if st.button("تحديث الأفلام تلقائياً من CimaNow 🚀"):
    with st.spinner("جاري جمع أحدث الأفلام..."):
        result = scrape_cimanow()
        if isinstance(result, int):
            st.success(f"تم! أضفنا {result} فيلم جديد.")
            st.rerun()
        else:
            st.error(result) 

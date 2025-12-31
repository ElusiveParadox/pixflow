import streamlit as st
import requests
import base64
import urllib.parse
import time
import os

# ------- Backend Import ---------
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
st.write("Using backend:", BACKEND_URL)


# ---------- Page Config ----------
st.set_page_config(page_title="Pixflow", layout="wide", page_icon="🌀")

# ---------- Dark Theme ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: radial-gradient(circle at top, #0b1020, #020617 70%);
    color: #e5e7eb;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(2,6,23,0.95);
    border-right: 1px solid #1e293b;
}

/* Logo */
.logo {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Inputs */
input, textarea {
    background: rgba(15,23,42,0.9) !important;
    color: #e5e7eb !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #4f46e5, #0ea5e9);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.55rem 1.3rem;
    font-weight: 600;
    transition: 0.25s ease;
}
.stButton>button:hover { transform: translateY(-2px); }

/* Cards */
.post-card {
    background: rgba(15,23,42,0.9);
    border: 1px solid #1e293b;
    border-radius: 18px;
    padding: 1rem;
    margin-bottom: 1.3rem;
    box-shadow: 0 12px 35px rgba(0,0,0,0.5);
    transition: 0.3s;
}
.post-card:hover { transform: translateY(-3px); }

/* Delete highlight */
.delete-card {
    background: #7f1d1d !important;
    border: 2px solid #ef4444 !important;
}

/* Avatar */
.avatar {
    width:36px;height:36px;border-radius:50%;
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    display:flex;align-items:center;justify-content:center;
    font-weight:700;color:white;
}

/* Caption below */
.caption {
    color: #c7d2fe;
    font-size: 0.85rem;
    margin-top: 0.4rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Session ----------
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "likes" not in st.session_state:
    st.session_state.likes = {}
if "show_overlay" not in st.session_state:
    st.session_state.show_overlay = True
if "delete_highlight" not in st.session_state:
    st.session_state.delete_highlight = None


def get_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def avatar_from_email(email):
    return email[0].upper()


# ---------- Login ----------
def login_page():
    st.markdown(
        "<div style='text-align:center;margin-top:4rem'>", unsafe_allow_html=True
    )
    st.markdown("<div class='logo'>🌀 Pixflow</div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#94a3b8'>Flow your moments. Share your world.</p>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("### 🔐 Sign in")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if email and password:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Login", width="stretch"):
                    res = requests.post(
                        f"{BACKEND_URL}/auth/jwt/login",
                        data={"username": email, "password": password},
                    )

                    if res.status_code == 200:
                        st.session_state.token = res.json()["access_token"]
                        user_res = requests.get(
                            f"{BACKEND_URL}/users/me", headers=get_headers()
                        )

                        if user_res.status_code == 200:
                            st.session_state.user = user_res.json()
                            st.rerun()
                        else:
                            st.error("Failed to get user info")
                    else:
                        st.error("Invalid credentials")
            with col2:
                if st.button("Sign Up", width="stretch"):
                    res = requests.post(
                        f"{BACKEND_URL}/auth/register",
                        json={"email": email, "password": password},
                    )

                    if res.status_code == 201:
                        st.success("Account created! Login now.")
                    else:
                        st.error(res.json().get("detail", "Registration failed"))
        else:
            st.info("Enter your credentials")


# ---------- Upload ----------
def upload_page():
    st.markdown("## 📸 Create Post")

    uploaded_file = st.file_uploader(
        "Upload media", type=["png", "jpg", "jpeg", "mp4", "avi", "mov", "mkv", "webm"]
    )

    caption = st.text_area(
        "Caption", placeholder="Write something about this...", height=100
    )

    if uploaded_file:
        if st.button("🚀 Share Post"):
            with st.spinner("Uploading..."):
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type,
                    )
                }
                data = {"caption": caption}
                res = requests.post(
                    f"{BACKEND_URL}/upload",
                    files=files,
                    data=data,
                    headers=get_headers(),
                )

                if res.status_code == 200:
                    st.success("Post shared!")
                    st.rerun()
                else:
                    st.error("Upload failed")


# ---------- Helpers ----------
def encode_text_for_overlay(text):
    if not text:
        return ""
    return urllib.parse.quote(base64.b64encode(text.encode()).decode())


def create_transformed_url(original_url, caption=None):
    if caption and st.session_state.show_overlay:
        encoded = encode_text_for_overlay(caption)
        # Smaller font size fs-60
        trans = f"l-text,ie-{encoded},ly-N15,lx-15,fs-60,co-white,bg-00000080,l-end"
        parts = original_url.split("/")
        return f"{'/'.join(parts[:4])}/tr:{trans}/{'/'.join(parts[4:])}"
    return original_url


# ---------- Feed ----------
def feed_page():
    st.markdown("## 🏠 Pixflow Feed")

    # Toggle for caption overlay
    st.checkbox("Show caption on image", key="show_overlay")

    with st.spinner("Loading feed..."):
        time.sleep(0.3)
        res = requests.get(f"{BACKEND_URL}/feed", headers=get_headers())

    if res.status_code == 200:
        posts = res.json()["posts"]
        if not posts:
            st.info("No posts yet.")
            return

        cols = st.columns(3)
        i = 0

        for post in posts:
            card_class = "post-card"
            if st.session_state.delete_highlight == post["id"]:
                card_class += " delete-card"

            with cols[i % 3]:
                st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)

                h1, h2 = st.columns([5, 1])
                with h1:
                    st.markdown(
                        f"<div style='display:flex;gap:0.6rem;align-items:center'>"
                        f"<div class='avatar'>{avatar_from_email(post['email'])}</div>"
                        f"<div><b>{post['email']}</b><br>"
                        f"<span style='color:#94a3b8;font-size:0.75rem'>{post['created_at'][:10]}</span></div>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                with h2:
                    if post.get("is_owner", False):
                        if st.button("🗑️", key=f"del_{post['id']}"):
                            st.session_state.delete_highlight = post["id"]
                            d = requests.delete(
                                f"{BACKEND_URL}/posts/{post['id']}",
                                headers=get_headers(),
                            )

                            if d.status_code == 200:
                                st.success("Deleted")
                                st.session_state.delete_highlight = None
                                st.rerun()
                            else:
                                st.error("Delete failed")
                                st.session_state.delete_highlight = None

                caption = post.get("caption", "")

                if post["file_type"] == "image":
                    url = create_transformed_url(post["url"], caption)
                    st.image(url, width="stretch")
                else:
                    parts = post["url"].split("/")
                    video_url = f"{'/'.join(parts[:4])}/tr:w-400,h-200,cm-pad_resize,bg-blurred/{'/'.join(parts[4:])}"
                    st.video(video_url)

                # Caption below card always visible
                if caption:
                    st.markdown(
                        f"<div class='caption'>{caption}</div>", unsafe_allow_html=True
                    )

                st.markdown("</div>", unsafe_allow_html=True)
                i += 1
    else:
        st.error("Failed to load feed")


# ---------- Main ----------
if st.session_state.user is None:
    login_page()
else:
    st.sidebar.markdown("<div class='logo'>🌀 Pixflow</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"**{st.session_state.user['email']}**")
    st.sidebar.markdown("---")

    page = st.sidebar.radio("Navigate", ["🏠 Feed", "📸 Upload"])

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()

    if page == "🏠 Feed":
        feed_page()
    else:
        upload_page()

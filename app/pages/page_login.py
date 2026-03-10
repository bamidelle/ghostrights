import streamlit as st
from database.db import get_supabase, get_profile

def render():

    # ── CSS ──────────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background: #0a0a0a; color: #f0ede6;
        font-family: 'DM Sans', sans-serif;
    }
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(ellipse at 20% 50%,
            #1a0a2e 0%, #0a0a0a 60%);
    }
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stHeader"]  { background: transparent; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    .gr-logo {
        font-family: 'Syne', sans-serif;
        font-size: 22px; font-weight: 800; color: #c8ff00;
        text-align: center; padding: 40px 0 0; cursor: pointer;
    }
    .gr-card {
        max-width: 440px; margin: 40px auto 0;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 24px; padding: 48px 40px;
        backdrop-filter: blur(12px);
    }
    .gr-card-title {
        font-family: 'Syne', sans-serif;
        font-size: 28px; font-weight: 800;
        text-align: center; margin-bottom: 8px;
    }
    .gr-card-sub {
        text-align: center; font-size: 14px;
        color: rgba(240,237,230,0.45);
        margin-bottom: 36px; line-height: 1.6;
    }
    .gr-label {
        font-size: 12px; letter-spacing: 0.8px;
        text-transform: uppercase;
        color: rgba(240,237,230,0.4);
        margin-bottom: 6px; margin-top: 20px;
    }
    .stTextInput input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        color: #f0ede6 !important;
        padding: 14px 16px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 15px !important;
    }
    .stTextInput input:focus {
        border-color: rgba(200,255,0,0.5) !important;
        box-shadow: 0 0 0 3px rgba(200,255,0,0.08) !important;
    }
    .stButton > button {
        background: #c8ff00 !important;
        color: #0a0a0a !important; border: none !important;
        border-radius: 10px !important;
        padding: 14px 32px !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 15px !important; font-weight: 700 !important;
        width: 100% !important; margin-top: 28px !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background: #d4ff33 !important;
        box-shadow: 0 8px 32px rgba(200,255,0,0.25) !important;
    }
    .gr-divider {
        display: flex; align-items: center;
        gap: 12px; margin: 24px 0;
    }
    .gr-divider-line {
        flex: 1; height: 1px;
        background: rgba(255,255,255,0.08);
    }
    .gr-divider-text {
        font-size: 12px; color: rgba(240,237,230,0.3);
    }
    .gr-switch {
        text-align: center; font-size: 13px;
        color: rgba(240,237,230,0.4); margin-top: 24px;
    }
    .gr-switch span { color: #c8ff00; cursor: pointer; font-weight: 500; }
    .gr-forgot {
        text-align: right; font-size: 12px;
        color: rgba(200,255,0,0.6);
        cursor: pointer; margin-top: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── LOGO ─────────────────────────────────────────────────
    if st.button("👻 GhostRights", key="logo_home"):
        st.session_state.current_page = "landing"
        st.rerun()

    # ── CARD ─────────────────────────────────────────────────
    st.markdown("""
    <div class="gr-card">
        <div class="gr-card-title">Welcome back</div>
        <div class="gr-card-sub">
            Log in to your GhostRights account<br>
            and see what we caught while you were away.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="gr-label">Email Address</div>',
                    unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="your@email.com",
                              label_visibility="collapsed", key="login_email")

        st.markdown('<div class="gr-label">Password</div>',
                    unsafe_allow_html=True)
        password = st.text_input("Password", placeholder="••••••••",
                                 type="password",
                                 label_visibility="collapsed",
                                 key="login_password")

        st.markdown('<div class="gr-forgot">Forgot password?</div>',
                    unsafe_allow_html=True)

        login_btn = st.button("Login to GhostRights →", key="login_btn")

        st.markdown("""
        <div class="gr-divider">
            <div class="gr-divider-line"></div>
            <div class="gr-divider-text">OR</div>
            <div class="gr-divider-line"></div>
        </div>
        """, unsafe_allow_html=True)

        signup_btn = st.button("Create a free account", key="go_signup")

        st.markdown("""
        <div class="gr-switch">
            Don't have an account?
            <span id="signup-link">Sign up free</span>
        </div>
        """, unsafe_allow_html=True)

    # ── LOGIN LOGIC ───────────────────────────────────────────
    if login_btn:
        if not email or not password:
            st.error("Please enter your email and password.")
        else:
            with st.spinner("Logging you in..."):
                success, message = _do_login(email, password)
            if success:
                st.success("Welcome back! Redirecting...")
                st.rerun()
            else:
                st.error(f"Login failed: {message}")

    if signup_btn:
        st.session_state.current_page = "signup"
        st.rerun()


def _do_login(email: str, password: str):
    """Authenticate user with Supabase."""
    try:
        supabase = get_supabase()
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if response.user:
            st.session_state.authenticated = True
            st.session_state.user = response.user
            st.session_state.profile = get_profile(response.user.id)
            st.session_state.current_page = "dashboard"
            return True, "Success"
        return False, "Invalid credentials"
    except Exception as e:
        return False, str(e)

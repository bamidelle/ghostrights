import streamlit as st
from database.db import get_supabase, get_profile

def render():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    .main .block-container {
        background: #F0EDE8 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #111111 !important;
    }
    [data-testid="stSidebar"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    #MainMenu, footer, header { display: none !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    .kl-login-wrap {
        min-height: 100vh;
        display: flex; align-items: center; justify-content: center;
        background: #F0EDE8;
        padding: 40px 20px;
    }
    .kl-login-card {
        background: #FFFFFF;
        border: 1.5px solid #E8E4DE;
        border-radius: 24px;
        padding: 48px 44px;
        width: 100%; max-width: 440px;
        box-shadow: 0 8px 40px rgba(0,0,0,0.07);
    }
    .kl-login-logo {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 18px; font-weight: 900;
        color: #111111; margin-bottom: 32px;
        display: block; letter-spacing: -0.3px;
    }
    .kl-login-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 28px; font-weight: 900;
        letter-spacing: -0.8px; color: #111111;
        margin-bottom: 6px; line-height: 1.1;
    }
    .kl-login-sub {
        font-size: 14px; color: #6B6B6B;
        font-weight: 500; margin-bottom: 32px;
        line-height: 1.5;
    }
    .kl-field-label {
        font-size: 11px; font-weight: 800;
        letter-spacing: 1px; text-transform: uppercase;
        color: #9B9B9B; margin-bottom: 6px;
        margin-top: 18px; display: block;
    }
    .kl-field-label:first-of-type { margin-top: 0; }
    .kl-divider {
        display: flex; align-items: center; gap: 12px;
        margin: 24px 0; color: #9B9B9B;
        font-size: 12px; font-weight: 600;
    }
    .kl-divider::before, .kl-divider::after {
        content: ''; flex: 1;
        height: 1px; background: #E8E4DE;
    }
    .kl-switch {
        text-align: center; font-size: 13px;
        color: #6B6B6B; font-weight: 500;
        margin-top: 24px;
    }
    .kl-switch b { color: #111111; cursor: pointer; }

    /* Streamlit overrides */
    .stTextInput input {
        background: #F0EDE8 !important;
        border: 1.5px solid #E8E4DE !important;
        border-radius: 10px !important;
        color: #111111 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        padding: 12px 16px !important;
    }
    .stTextInput input:focus {
        border-color: #111111 !important;
        box-shadow: 0 0 0 3px rgba(26,26,26,0.08) !important;
    }
    .stButton > button {
        background: #111111 !important;
        color: #fff !important;
        border: none !important;
        border-radius: 100px !important;
        padding: 14px 28px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 15px !important;
        font-weight: 800 !important;
        width: 100% !important;
        letter-spacing: -0.2px !important;
        transition: all 0.15s !important;
    }
    .stButton > button:hover { background: #333 !important; }
    .stAlert { border-radius: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

    # Center the card
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown('<div class="kl-login-card">', unsafe_allow_html=True)

        # Logo + heading
        st.markdown("""
        <span class="kl-login-logo">👻 GhostRights</span>
        <div class="kl-login-title">Welcome back.</div>
        <div class="kl-login-sub">
            Log in to see what we caught<br>while you were away.
        </div>
        """, unsafe_allow_html=True)

        # Form
        st.markdown('<span class="kl-field-label">Email address</span>', unsafe_allow_html=True)
        email = st.text_input("e", placeholder="you@email.com",
                              label_visibility="collapsed", key="login_email")

        st.markdown('<span class="kl-field-label">Password</span>', unsafe_allow_html=True)
        password = st.text_input("p", type="password",
                                 placeholder="Your password",
                                 label_visibility="collapsed", key="login_password")

        # Forgot password
        st.markdown("""
        <div style="text-align:right;margin-top:6px;margin-bottom:24px;">
            <span style="font-size:12px;color:#9B9B9B;
                  font-weight:600;cursor:pointer;">
                Forgot password?
            </span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Login to GhostRights →", key="login_btn"):
            if not email or not password:
                st.error("Please enter your email and password.")
            else:
                _do_login(email, password)

        st.markdown('<div class="kl-divider">OR</div>', unsafe_allow_html=True)

        if st.button("Create a free account →", key="goto_signup"):
            st.session_state.current_page = "signup"
            st.rerun()

        st.markdown("""
        <div class="kl-switch">
            No account yet?
            <b onclick="">Sign up free</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


def _do_login(email, password):
    with st.spinner("Logging in..."):
        try:
            supabase = get_supabase()
            resp = supabase.auth.sign_in_with_password({
                "email": email, "password": password
            })
            user = resp.user
            if user:
                st.session_state.authenticated = True
                st.session_state.user = user
                profile = get_profile(user.id)
                st.session_state.profile = profile
                st.session_state.current_page = "dashboard"
                st.rerun()
            else:
                st.error("Login failed. Check your email and password.")
        except Exception as e:
            err = str(e).lower()
            if "invalid" in err or "credentials" in err:
                st.error("Incorrect email or password.")
            elif "confirmed" in err:
                st.error("Please confirm your email first.")
            else:
                st.error(f"Login error: {e}")

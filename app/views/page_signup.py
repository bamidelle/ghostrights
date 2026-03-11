import streamlit as st
from database.db import get_supabase, get_supabase_admin, get_profile

KLAVIYO_CSS = """
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

.kl-field-label {
    font-size: 11px; font-weight: 800;
    letter-spacing: 1px; text-transform: uppercase;
    color: #9B9B9B; margin-bottom: 6px;
    margin-top: 18px; display: block;
}
.kl-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #D8F3DC; color: #1B4332;
    font-size: 11px; font-weight: 800;
    letter-spacing: 0.8px; text-transform: uppercase;
    padding: 5px 12px; border-radius: 100px;
    margin-bottom: 20px;
}
.kl-badge-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #4ADE80; animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,100%{opacity:1;transform:scale(1)}
    50%{opacity:0.5;transform:scale(0.8)}
}
.plan-pill {
    border: 2px solid #E8E4DE;
    border-radius: 12px; padding: 16px 18px;
    cursor: pointer; transition: all 0.15s;
    margin-bottom: 8px; background: #fff;
}
.plan-pill.selected {
    border-color: #111111;
    background: #111111; color: #fff;
}
.plan-pill-name { font-size: 14px; font-weight: 800; letter-spacing: -0.2px; }
.plan-pill-price { font-size: 13px; font-weight: 600; opacity: 0.6; }

/* Streamlit overrides */
.stTextInput input {
    background: #fff !important;
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
.stSelectbox > div > div {
    background: #fff !important;
    border: 1.5px solid #E8E4DE !important;
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #111111 !important;
}
.stRadio > div {
    gap: 8px !important;
}
.stRadio label {
    background: #fff !important;
    border: 1.5px solid #E8E4DE !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
    width: 100% !important;
}
.stButton > button {
    background: #111111 !important;
    color: #fff !important; border: none !important;
    border-radius: 100px !important;
    padding: 14px 28px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 15px !important; font-weight: 800 !important;
    width: 100% !important; letter-spacing: -0.2px !important;
    transition: all 0.15s !important;
}
.stButton > button:hover { background: #333 !important; }
.stAlert { border-radius: 12px !important; }
</style>
"""

def render():
    st.markdown(KLAVIYO_CSS, unsafe_allow_html=True)

    # Two-column layout: form left, benefits right
    left, right = st.columns([1.1, 0.9])

    # ── LEFT — SIGNUP FORM ────────────────────────────────────
    with left:
        st.markdown("""
        <div style="background:#fff;border:1.5px solid #E8E4DE;
             border-radius:24px;padding:44px 40px;
             box-shadow:0 8px 40px rgba(0,0,0,0.06);">
        """, unsafe_allow_html=True)

        st.markdown("""
        <span style="font-family:'Plus Jakarta Sans',sans-serif;
              font-size:18px;font-weight:900;color:#111111;
              display:block;margin-bottom:24px;">
            👻 GhostRights
        </span>
        <div class="kl-badge">
            <div class="kl-badge-dot"></div>
            Free to start
        </div>
        <div style="font-family:'Plus Jakarta Sans',sans-serif;
             font-size:26px;font-weight:900;letter-spacing:-0.8px;
             color:#111111;margin-bottom:6px;line-height:1.1;">
            Start protecting<br>your content.
        </div>
        <div style="font-size:14px;color:#6B6B6B;font-weight:500;
             margin-bottom:28px;line-height:1.5;">
            Join African creators already protecting
            their work with GhostRights.
        </div>
        """, unsafe_allow_html=True)

        # Form fields
        st.markdown('<span class="kl-field-label">Full name</span>', unsafe_allow_html=True)
        full_name = st.text_input("fn", placeholder="e.g. Emeka Okafor",
                                  label_visibility="collapsed", key="su_name")

        st.markdown('<span class="kl-field-label">Email address</span>', unsafe_allow_html=True)
        email = st.text_input("em", placeholder="your@email.com",
                              label_visibility="collapsed", key="su_email")

        st.markdown('<span class="kl-field-label">Phone / WhatsApp</span>', unsafe_allow_html=True)
        phone = st.text_input("ph", placeholder="+234 801 234 5678",
                              label_visibility="collapsed", key="su_phone")

        st.markdown('<span class="kl-field-label">I am a...</span>', unsafe_allow_html=True)
        creator_type = st.selectbox("ct",
            ["Filmmaker / Director", "Musician / Artist",
             "YouTuber / Content Creator", "Podcaster",
             "Photographer", "Label / Studio", "Other"],
            label_visibility="collapsed", key="su_type")

        st.markdown('<span class="kl-field-label">Password</span>', unsafe_allow_html=True)
        password = st.text_input("pw", type="password",
                                 placeholder="Min. 8 characters",
                                 label_visibility="collapsed", key="su_pass")

        st.markdown('<span class="kl-field-label">Choose your plan</span>', unsafe_allow_html=True)
        plan = st.radio("plan",
            ["🆓 Free scan only",
             "⚡ Starter — ₦8,000/month",
             "🚀 Pro — ₦20,000/month",
             "🏆 Studio — ₦75,000/month"],
            label_visibility="collapsed", key="su_plan")

        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)

        if st.button("Create my account →", key="signup_btn"):
            if not full_name or not email or not password:
                st.error("Please fill in all required fields.")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters.")
            else:
                _do_signup(full_name, email, phone,
                           creator_type, password, plan)

        st.markdown("""
        <div style="text-align:center;font-size:13px;
             color:#9B9B9B;font-weight:500;margin-top:20px;">
            Already have an account?
            <span style="color:#111111;font-weight:800;
                  cursor:pointer;">Log in</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Login link button (hidden label, just for routing)
        if st.button("← Back to login", key="goto_login"):
            st.session_state.current_page = "login"
            st.rerun()

    # ── RIGHT — BENEFITS ─────────────────────────────────────
    with right:
        st.markdown("""
        <div style="padding:40px 32px;">

        <div style="font-family:'Plus Jakarta Sans',sans-serif;
             font-size:22px;font-weight:900;letter-spacing:-0.5px;
             color:#111111;margin-bottom:20px;line-height:1.15;">
            Why GhostRights?
        </div>
        """, unsafe_allow_html=True)

        benefits = [
            ("🕷️", "Detects piracy across 7+ platforms",
             "YouTube, Facebook, Telegram, TikTok, Instagram, blogs and torrent sites."),
            ("💰", "Monetizes stolen content automatically",
             "Redirect ad revenue from pirated copies straight to your account."),
            ("⚔️", "Sends DMCA takedowns at scale",
             "Legal notices generated and sent automatically within minutes."),
            ("📱", "WhatsApp alerts when piracy is found",
             "Get notified the moment a new pirated copy is detected."),
            ("📊", "Monthly PDF piracy intelligence reports",
             "Full breakdown of who is stealing your content and how much you are losing."),
            ("🤝", "You keep 80% of recovered revenue",
             "GhostRights only takes 20% commission on recovered ad revenue."),
        ]

        for icon, title, desc in benefits:
            st.markdown(f"""
            <div style="display:flex;gap:14px;margin-bottom:20px;
                 align-items:flex-start;">
                <div style="font-size:22px;flex-shrink:0;
                     margin-top:2px;">{icon}</div>
                <div>
                    <div style="font-size:14px;font-weight:800;
                         color:#111111;letter-spacing:-0.2px;
                         margin-bottom:3px;">{title}</div>
                    <div style="font-size:13px;color:#6B6B6B;
                         font-weight:500;line-height:1.55;">
                         {desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Social proof card
        st.markdown("""
        <div style="margin-top:32px;background:#111111;
             border-radius:16px;padding:24px 24px;">
            <div style="font-size:32px;font-weight:900;
                 color:#4ADE80;letter-spacing:-1px;
                 font-family:'Plus Jakarta Sans',sans-serif;
                 margin-bottom:4px;">₦2.3M</div>
            <div style="font-size:13px;color:rgba(255,255,255,0.5);
                 font-weight:500;line-height:1.6;">
                Recovered for African creators<br>
                in their first month on GhostRights
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


def _do_signup(full_name, email, phone,
               creator_type, password, plan_choice):
    with st.spinner("Creating your account..."):
        try:
            supabase = get_supabase()
            admin    = get_supabase_admin()

            # Map plan choice to slug
            plan_map = {
                "🆓 Free scan only":         "free",
                "⚡ Starter — ₦8,000/month": "starter",
                "🚀 Pro — ₦20,000/month":    "pro",
                "🏆 Studio — ₦75,000/month": "studio",
            }
            plan_slug = plan_map.get(plan_choice, "free")

            # Map creator type
            type_map = {
                "Filmmaker / Director":      "filmmaker",
                "Musician / Artist":         "musician",
                "YouTuber / Content Creator":"youtuber",
                "Podcaster":                 "podcaster",
                "Photographer":              "photographer",
                "Label / Studio":            "label",
                "Other":                     "other",
            }
            ctype = type_map.get(creator_type, "other")

            # Create auth user
            resp = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name":    full_name,
                        "creator_type": ctype,
                        "phone":        phone,
                    }
                }
            })

            if not resp.user:
                st.error("Signup failed. Please try again.")
                return

            user = resp.user

            # Upsert profile
            try:
                admin.table("profiles").upsert({
                    "id":           user.id,
                    "email":        email,
                    "full_name":    full_name,
                    "phone":        phone,
                    "creator_type": ctype,
                    "plan":         plan_slug,
                    "role":         "creator",
                }).execute()
            except Exception:
                pass

            # Set session
            st.session_state.authenticated = True
            st.session_state.user = user
            st.session_state.profile = {
                "id":           user.id,
                "email":        email,
                "full_name":    full_name,
                "phone":        phone,
                "creator_type": ctype,
                "plan":         plan_slug,
                "role":         "creator",
            }
            st.session_state.current_page = "dashboard"

            st.success("🎉 Account created! Welcome to GhostRights.")
            st.rerun()

        except Exception as e:
            err = str(e).lower()
            if "already registered" in err or "already exists" in err:
                st.error("An account with this email already exists. Please log in.")
            else:
                st.error(f"Signup error: {e}")

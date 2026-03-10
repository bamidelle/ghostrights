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
        background: radial-gradient(ellipse at 80% 20%,
            #0d1f0d 0%, #0a0a0a 60%);
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
        max-width: 480px; margin: 32px auto 0;
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
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        color: #f0ede6 !important;
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
    .gr-plan-selector {
        display: flex; gap: 10px; margin-top: 8px;
    }
    .gr-switch {
        text-align: center; font-size: 13px;
        color: rgba(240,237,230,0.4); margin-top: 24px;
    }
    .gr-terms {
        text-align: center; font-size: 11px;
        color: rgba(240,237,230,0.25);
        margin-top: 16px; line-height: 1.6;
    }
    .gr-terms span { color: rgba(200,255,0,0.5); }
    .gr-benefit {
        display: flex; align-items: center; gap: 10px;
        font-size: 13px; color: rgba(240,237,230,0.5);
        margin-bottom: 10px;
    }
    .gr-benefit::before { content: "✓"; color: #c8ff00; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

    # ── LOGO ─────────────────────────────────────────────────
    if st.button("👻 GhostRights", key="logo_home"):
        st.session_state.current_page = "landing"
        st.rerun()

    # ── LAYOUT — form left, benefits right ───────────────────
    col_form, col_gap, col_benefits = st.columns([5, 1, 4])

    with col_form:
        st.markdown("""
        <div class="gr-card">
            <div class="gr-card-title">Start protecting<br>your content</div>
            <div class="gr-card-sub">
                Join African creators already protecting<br>
                their work with GhostRights.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="gr-label">Full Name</div>',
                    unsafe_allow_html=True)
        full_name = st.text_input("Full Name",
                                  placeholder="e.g. Emeka Okafor",
                                  label_visibility="collapsed",
                                  key="signup_name")

        st.markdown('<div class="gr-label">Email Address</div>',
                    unsafe_allow_html=True)
        email = st.text_input("Email",
                              placeholder="your@email.com",
                              label_visibility="collapsed",
                              key="signup_email")

        st.markdown('<div class="gr-label">Phone / WhatsApp</div>',
                    unsafe_allow_html=True)
        phone = st.text_input("Phone",
                              placeholder="+234 801 234 5678",
                              label_visibility="collapsed",
                              key="signup_phone")

        st.markdown('<div class="gr-label">Password</div>',
                    unsafe_allow_html=True)
        password = st.text_input("Password",
                                 placeholder="Min. 8 characters",
                                 type="password",
                                 label_visibility="collapsed",
                                 key="signup_password")

        st.markdown('<div class="gr-label">Confirm Password</div>',
                    unsafe_allow_html=True)
        password2 = st.text_input("Confirm",
                                  placeholder="Repeat your password",
                                  type="password",
                                  label_visibility="collapsed",
                                  key="signup_password2")

        st.markdown('<div class="gr-label">I Am A...</div>',
                    unsafe_allow_html=True)
        creator_type = st.selectbox("Creator type",
            ["Filmmaker / Producer", "Musician / Artist",
             "YouTuber / Content Creator", "Podcaster",
             "Record Label", "Film Studio", "Other"],
            label_visibility="collapsed",
            key="signup_creator_type")

        st.markdown('<div class="gr-label">Choose Your Plan</div>',
                    unsafe_allow_html=True)
        plan = st.selectbox("Plan",
            ["Starter — ₦8,000/month",
             "Pro — ₦20,000/month (Most Popular)",
             "Studio — ₦75,000/month"],
            label_visibility="collapsed",
            key="signup_plan")

        signup_btn = st.button("Create My Account →", key="signup_btn")

        st.markdown("""
        <div class="gr-terms">
            By signing up you agree to our
            <span>Terms of Service</span> and
            <span>Privacy Policy</span>.
        </div>
        """, unsafe_allow_html=True)

        login_btn = st.button("Already have an account? Login",
                              key="go_login")

    with col_benefits:
        st.markdown("""
        <div style="padding: 80px 20px 0;">
            <div style="font-family:'Syne',sans-serif; font-size:20px;
                 font-weight:800; margin-bottom:32px; color:#f0ede6;">
                Why GhostRights?
            </div>
            <div class="gr-benefit">Detects piracy across 6+ platforms</div>
            <div class="gr-benefit">Monetizes stolen content automatically</div>
            <div class="gr-benefit">Sends DMCA takedowns at scale</div>
            <div class="gr-benefit">WhatsApp alerts when piracy is found</div>
            <div class="gr-benefit">Monthly PDF piracy intelligence reports</div>
            <div class="gr-benefit">You keep 80% of recovered revenue</div>
            <div class="gr-benefit">Built specifically for African creators</div>

            <div style="margin-top:48px; padding:28px;
                 background:rgba(200,255,0,0.05);
                 border:1px solid rgba(200,255,0,0.15);
                 border-radius:16px;">
                <div style="font-size:32px; font-family:'Syne',sans-serif;
                     font-weight:800; color:#c8ff00;">₦2.3M</div>
                <div style="font-size:12px; color:rgba(240,237,230,0.4);
                     margin-top:6px; line-height:1.6;">
                    Recovered for a Nollywood producer<br>
                    in his first month on GhostRights
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── SIGNUP LOGIC ──────────────────────────────────────────
    if signup_btn:
        # Validation
        if not full_name or not email or not password:
            st.error("Please fill in all required fields.")
        elif password != password2:
            st.error("Passwords do not match.")
        elif len(password) < 8:
            st.error("Password must be at least 8 characters.")
        else:
            with st.spinner("Creating your account..."):
                success, message = _do_signup(
                    full_name, email, phone, password, creator_type, plan
                )
            if success:
                st.success("""
                    ✅ Account created! Check your email to verify
                    your account then login.
                """)
            else:
                st.error(f"Signup failed: {message}")

    if login_btn:
        st.session_state.current_page = "login"
        st.rerun()


def _do_signup(full_name, email, phone, password, creator_type, plan):
    """Create new user account in Supabase."""
    try:
        supabase = get_supabase()

        # Map plan display name to plan key
        plan_map = {
            "Starter — ₦8,000/month": "starter",
            "Pro — ₦20,000/month (Most Popular)": "pro",
            "Studio — ₦75,000/month": "studio"
        }
        plan_key = plan_map.get(plan, "starter")

        # Map creator type
        type_map = {
            "Filmmaker / Producer": "filmmaker",
            "Musician / Artist": "musician",
            "YouTuber / Content Creator": "youtuber",
            "Podcaster": "podcaster",
            "Record Label": "label",
            "Film Studio": "studio",
            "Other": "other"
        }
        creator_type_key = type_map.get(creator_type, "other")

        # Create auth user
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "full_name": full_name,
                    "phone": phone,
                    "creator_type": creator_type_key,
                    "selected_plan": plan_key
                }
            }
        })

        if response.user:
            # Update profile with extra details
            # (handle_new_user trigger creates base profile)
            supabase.table("profiles").update({
                "phone": phone,
                "creator_type": creator_type_key,
                "whatsapp_number": phone,
            }).eq("id", response.user.id).execute()

            return True, "Success"

        return False, "Could not create account. Please try again."

    except Exception as e:
        error_msg = str(e)
        if "already registered" in error_msg.lower():
            return False, "This email is already registered. Please login instead."
        return False, error_msg

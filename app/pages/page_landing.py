import streamlit as st

def render():

    # ── CSS ──────────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background: #0a0a0a;
        color: #f0ede6;
        font-family: 'DM Sans', sans-serif;
    }
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(ellipse at 20% 50%, #1a0a2e 0%, #0a0a0a 60%),
                    radial-gradient(ellipse at 80% 20%, #0d1f0d 0%, transparent 50%);
    }
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stHeader"]  { background: transparent; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    /* NAV */
    .gr-nav {
        display: flex; justify-content: space-between; align-items: center;
        padding: 24px 60px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .gr-logo {
        font-family: 'Syne', sans-serif;
        font-size: 22px; font-weight: 800;
        color: #c8ff00; letter-spacing: -0.5px;
    }
    .gr-nav-links { display: flex; gap: 32px; }
    .gr-nav-links a {
        color: rgba(240,237,230,0.6);
        text-decoration: none; font-size: 14px;
        transition: color 0.2s;
    }

    /* HERO */
    .gr-hero {
        padding: 100px 60px 80px;
        max-width: 900px;
    }
    .gr-badge {
        display: inline-block;
        background: rgba(200,255,0,0.1);
        border: 1px solid rgba(200,255,0,0.3);
        color: #c8ff00; font-size: 12px;
        padding: 6px 16px; border-radius: 100px;
        margin-bottom: 32px; letter-spacing: 1px;
        text-transform: uppercase;
    }
    .gr-h1 {
        font-family: 'Syne', sans-serif;
        font-size: clamp(48px, 7vw, 88px);
        font-weight: 800; line-height: 1.0;
        letter-spacing: -2px; margin: 0 0 24px;
        color: #f0ede6;
    }
    .gr-h1 span { color: #c8ff00; }
    .gr-sub {
        font-size: 18px; color: rgba(240,237,230,0.55);
        max-width: 560px; line-height: 1.7;
        margin-bottom: 52px; font-weight: 300;
    }

    /* SCAN BOX */
    .gr-scan-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px; padding: 40px;
        max-width: 680px;
        backdrop-filter: blur(12px);
        margin-bottom: 80px;
    }
    .gr-scan-title {
        font-family: 'Syne', sans-serif;
        font-size: 20px; font-weight: 700;
        margin-bottom: 8px; color: #f0ede6;
    }
    .gr-scan-sub {
        font-size: 13px; color: rgba(240,237,230,0.45);
        margin-bottom: 28px;
    }
    .gr-input-label {
        font-size: 12px; letter-spacing: 0.8px;
        text-transform: uppercase;
        color: rgba(240,237,230,0.4);
        margin-bottom: 6px;
    }

    /* Streamlit input overrides */
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

    /* CTA Button */
    .stButton > button {
        background: #c8ff00 !important;
        color: #0a0a0a !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 32px !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 15px !important; font-weight: 700 !important;
        width: 100% !important; cursor: pointer !important;
        transition: all 0.2s !important;
        letter-spacing: 0.3px !important;
    }
    .stButton > button:hover {
        background: #d4ff33 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 32px rgba(200,255,0,0.25) !important;
    }

    /* STATS */
    .gr-stats {
        display: flex; gap: 60px;
        padding: 60px 60px;
        border-top: 1px solid rgba(255,255,255,0.06);
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 80px;
    }
    .gr-stat-num {
        font-family: 'Syne', sans-serif;
        font-size: 42px; font-weight: 800;
        color: #c8ff00; line-height: 1;
    }
    .gr-stat-label {
        font-size: 13px; color: rgba(240,237,230,0.45);
        margin-top: 6px;
    }

    /* HOW IT WORKS */
    .gr-section { padding: 0 60px 80px; }
    .gr-section-label {
        font-size: 11px; letter-spacing: 2px;
        text-transform: uppercase;
        color: rgba(200,255,0,0.7);
        margin-bottom: 16px;
    }
    .gr-section-title {
        font-family: 'Syne', sans-serif;
        font-size: 36px; font-weight: 800;
        letter-spacing: -1px; margin-bottom: 48px;
    }
    .gr-steps { display: flex; gap: 24px; flex-wrap: wrap; }
    .gr-step {
        flex: 1; min-width: 200px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px; padding: 32px;
    }
    .gr-step-num {
        font-family: 'Syne', sans-serif;
        font-size: 48px; font-weight: 800;
        color: rgba(200,255,0,0.2);
        line-height: 1; margin-bottom: 16px;
    }
    .gr-step-title {
        font-size: 16px; font-weight: 500;
        margin-bottom: 10px;
    }
    .gr-step-desc {
        font-size: 13px; color: rgba(240,237,230,0.45);
        line-height: 1.6;
    }

    /* PRICING */
    .gr-plans { display: flex; gap: 20px; flex-wrap: wrap; margin-top: 0; }
    .gr-plan {
        flex: 1; min-width: 220px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px; padding: 36px 28px;
    }
    .gr-plan.featured {
        background: rgba(200,255,0,0.06);
        border-color: rgba(200,255,0,0.3);
    }
    .gr-plan-name {
        font-size: 12px; letter-spacing: 1.5px;
        text-transform: uppercase;
        color: rgba(240,237,230,0.4);
        margin-bottom: 12px;
    }
    .gr-plan.featured .gr-plan-name { color: #c8ff00; }
    .gr-plan-price {
        font-family: 'Syne', sans-serif;
        font-size: 36px; font-weight: 800;
        margin-bottom: 4px;
    }
    .gr-plan-period {
        font-size: 12px; color: rgba(240,237,230,0.35);
        margin-bottom: 28px;
    }
    .gr-plan-feature {
        font-size: 13px; color: rgba(240,237,230,0.6);
        padding: 8px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        display: flex; align-items: center; gap: 8px;
    }
    .gr-plan-feature::before { content: "→"; color: #c8ff00; }

    /* FOOTER */
    .gr-footer {
        padding: 40px 60px;
        border-top: 1px solid rgba(255,255,255,0.06);
        display: flex; justify-content: space-between;
        align-items: center;
    }
    .gr-footer-logo {
        font-family: 'Syne', sans-serif;
        font-size: 18px; font-weight: 800; color: #c8ff00;
    }
    .gr-footer-copy {
        font-size: 12px; color: rgba(240,237,230,0.3);
    }

    /* login link */
    .gr-login-link {
        text-align: center; font-size: 13px;
        color: rgba(240,237,230,0.4);
        margin-top: 16px;
    }
    .gr-login-link span {
        color: #c8ff00; cursor: pointer;
        font-weight: 500;
    }

    /* result card */
    .gr-result {
        background: rgba(200,255,0,0.05);
        border: 1px solid rgba(200,255,0,0.2);
        border-radius: 16px; padding: 28px;
        margin-top: 24px;
    }
    .gr-result-title {
        font-family: 'Syne', sans-serif;
        font-size: 18px; font-weight: 700;
        color: #c8ff00; margin-bottom: 16px;
    }
    .gr-result-row {
        display: flex; justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-size: 14px;
    }
    .gr-result-row:last-child { border-bottom: none; }
    .gr-result-val { color: #c8ff00; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

    # ── NAV ───────────────────────────────────────────────────
    st.markdown("""
    <div class="gr-nav">
        <div class="gr-logo">👻 GhostRights</div>
        <div class="gr-nav-links">
            <a href="#">How It Works</a>
            <a href="#">Pricing</a>
            <a href="#">For Labels</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── HERO ──────────────────────────────────────────────────
    st.markdown("""
    <div class="gr-hero">
        <div class="gr-badge">🌍 Built For African Creators</div>
        <h1 class="gr-h1">
            Pirates are profiting<br>from <span>your content</span><br>right now.
        </h1>
        <p class="gr-sub">
            GhostRights hunts stolen content across Facebook, YouTube,
            TikTok, Telegram and thousands of websites — then makes it
            pay you or destroys it. Automatically.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── SCAN CARD ─────────────────────────────────────────────
    st.markdown("""
    <div style="padding: 0 60px;">
        <div class="gr-scan-card">
            <div class="gr-scan-title">🔍 Scan Your Content For Free</div>
            <div class="gr-scan-sub">
                See exactly where your content is being stolen — in 60 seconds. No card required.
            </div>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="gr-input-label">Your Full Name</div>',
                        unsafe_allow_html=True)
            name = st.text_input("name", placeholder="e.g. Emeka Okafor",
                                 label_visibility="collapsed", key="scan_name")
        with col2:
            st.markdown('<div class="gr-input-label">Email Address</div>',
                        unsafe_allow_html=True)
            email = st.text_input("email", placeholder="your@email.com",
                                  label_visibility="collapsed", key="scan_email")

        st.markdown('<div class="gr-input-label" style="margin-top:16px;">Content Title</div>',
                    unsafe_allow_html=True)
        content_title = st.text_input("title",
                                      placeholder="e.g. Living In Bondage, Essence (ft. Tems)",
                                      label_visibility="collapsed", key="scan_title")

        st.markdown('<div class="gr-input-label" style="margin-top:16px;">YouTube / Facebook / Website Link</div>',
                    unsafe_allow_html=True)
        content_url = st.text_input("url",
                                    placeholder="https://youtube.com/watch?v=...",
                                    label_visibility="collapsed", key="scan_url")

        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="gr-input-label" style="margin-top:16px;">Content Type</div>',
                        unsafe_allow_html=True)
            content_type = st.selectbox("type",
                ["Movie / Film", "Music Track", "YouTube Video",
                 "Podcast", "Short Film", "Other"],
                label_visibility="collapsed", key="scan_type")

        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
        scan_btn = st.button("🔍 Scan My Content For Free — It's Free", key="scan_btn")

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── SCAN LOGIC ────────────────────────────────────────────
    if scan_btn:
        if not name or not email or not content_title:
            st.error("Please fill in your name, email and content title.")
        else:
            # Save lead to Supabase
            _save_scan_lead(name, email, content_title, content_url, content_type)

            # Show animated scan
            with st.spinner("🔍 Scanning YouTube... Facebook... Telegram... Blogs..."):
                import time
                time.sleep(3)

            # Show mock results (real crawler plugs in here in Step 5)
            st.markdown(f"""
            <div style="padding: 0 60px;">
            <div class="gr-result">
                <div class="gr-result-title">
                    ⚠️ We found piracy of "{content_title}"
                </div>
                <div class="gr-result-row">
                    <span>Pirated copies found</span>
                    <span class="gr-result-val">23 copies</span>
                </div>
                <div class="gr-result-row">
                    <span>Platforms affected</span>
                    <span class="gr-result-val">Facebook, Telegram, 4 blogs</span>
                </div>
                <div class="gr-result-row">
                    <span>Estimated total views</span>
                    <span class="gr-result-val">89,400 views</span>
                </div>
                <div class="gr-result-row">
                    <span>Estimated revenue lost</span>
                    <span class="gr-result-val">₦847,000</span>
                </div>
                <div class="gr-result-row">
                    <span>Full report emailed to</span>
                    <span class="gr-result-val">{email}</span>
                </div>
            </div>
            <p style="font-size:13px; color:rgba(240,237,230,0.4);
               margin-top:12px; padding: 0 4px;">
                ✉️ Full piracy report sent to your email.
                Subscribe to take action on these {23} pirated copies.
            </p>
            </div>
            """, unsafe_allow_html=True)

            # Signup CTA after scan
            st.markdown("<div style='padding: 0 60px; margin-top: 20px;'>",
                        unsafe_allow_html=True)
            if st.button("🚀 Start Recovering My Content — Subscribe Now",
                         key="post_scan_cta"):
                st.session_state.current_page = "signup"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # ── STATS ─────────────────────────────────────────────────
    st.markdown("""
    <div class="gr-stats">
        <div>
            <div class="gr-stat-num">$2B+</div>
            <div class="gr-stat-label">Lost to African content piracy yearly</div>
        </div>
        <div>
            <div class="gr-stat-num">24/7</div>
            <div class="gr-stat-label">Continuous crawling across all platforms</div>
        </div>
        <div>
            <div class="gr-stat-num">6+</div>
            <div class="gr-stat-label">Platforms monitored simultaneously</div>
        </div>
        <div>
            <div class="gr-stat-num">20%</div>
            <div class="gr-stat-label">Commission only — we earn when you earn</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── HOW IT WORKS ──────────────────────────────────────────
    st.markdown("""
    <div class="gr-section">
        <div class="gr-section-label">How It Works</div>
        <div class="gr-section-title">Simple. Automatic. Relentless.</div>
        <div class="gr-steps">
            <div class="gr-step">
                <div class="gr-step-num">01</div>
                <div class="gr-step-title">Upload Your Content</div>
                <div class="gr-step-desc">
                    Register your movies, music or videos.
                    We fingerprint every file uniquely.
                </div>
            </div>
            <div class="gr-step">
                <div class="gr-step-num">02</div>
                <div class="gr-step-title">We Hunt Pirates</div>
                <div class="gr-step-desc">
                    Our crawlers scan YouTube, Facebook,
                    TikTok, Telegram and blogs every hour.
                </div>
            </div>
            <div class="gr-step">
                <div class="gr-step-num">03</div>
                <div class="gr-step-title">Monetize or Destroy</div>
                <div class="gr-step-desc">
                    Claim ad revenue from pirated copies
                    or send automated DMCA takedowns.
                </div>
            </div>
            <div class="gr-step">
                <div class="gr-step-num">04</div>
                <div class="gr-step-title">You Get Paid</div>
                <div class="gr-step-desc">
                    Revenue flows to your account.
                    You keep 80%. We take 20% commission.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PRICING ───────────────────────────────────────────────
    st.markdown("""
    <div class="gr-section">
        <div class="gr-section-label">Pricing</div>
        <div class="gr-section-title">Pay only for what you need.</div>
        <div class="gr-plans">
            <div class="gr-plan">
                <div class="gr-plan-name">Starter</div>
                <div class="gr-plan-price">₦8,000</div>
                <div class="gr-plan-period">per month</div>
                <div class="gr-plan-feature">5 content items protected</div>
                <div class="gr-plan-feature">100 scans per month</div>
                <div class="gr-plan-feature">30 takedowns per month</div>
                <div class="gr-plan-feature">Basic dashboard</div>
            </div>
            <div class="gr-plan featured">
                <div class="gr-plan-name">⭐ Pro — Most Popular</div>
                <div class="gr-plan-price">₦20,000</div>
                <div class="gr-plan-period">per month</div>
                <div class="gr-plan-feature">20 content items protected</div>
                <div class="gr-plan-feature">Unlimited scans</div>
                <div class="gr-plan-feature">Unlimited takedowns</div>
                <div class="gr-plan-feature">Ad revenue monetization</div>
                <div class="gr-plan-feature">WhatsApp alerts</div>
                <div class="gr-plan-feature">Monthly PDF report</div>
            </div>
            <div class="gr-plan">
                <div class="gr-plan-name">Studio</div>
                <div class="gr-plan-price">₦75,000</div>
                <div class="gr-plan-period">per month</div>
                <div class="gr-plan-feature">Unlimited everything</div>
                <div class="gr-plan-feature">Priority crawling</div>
                <div class="gr-plan-feature">API access</div>
                <div class="gr-plan-feature">White-label option</div>
                <div class="gr-plan-feature">Dedicated manager</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── FOOTER ────────────────────────────────────────────────
    st.markdown("""
    <div class="gr-footer">
        <div class="gr-footer-logo">👻 GhostRights</div>
        <div class="gr-footer-copy">
            © 2026 GhostRights. Built for African creators.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Nav buttons
    col_a, col_b, col_c = st.columns([4, 1, 1])
    with col_b:
        if st.button("Login", key="nav_login"):
            st.session_state.current_page = "login"
            st.rerun()
    with col_c:
        if st.button("Sign Up →", key="nav_signup"):
            st.session_state.current_page = "signup"
            st.rerun()


def _save_scan_lead(name, email, title, url, content_type):
    """Save free scan lead to Supabase for email retargeting."""
    try:
        from database.db import get_supabase_admin
        supabase = get_supabase_admin()
        supabase.table("free_scan_leads").insert({
            "full_name": name,
            "email": email,
            "content_title": title,
            "content_url": url,
            "content_type": content_type,
            "scan_status": "complete",
        }).execute()
    except Exception:
        pass  # Never crash landing page on DB error

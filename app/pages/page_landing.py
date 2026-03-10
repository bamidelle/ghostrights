import streamlit as st
from database.db import get_supabase_admin


def render():

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

    :root {
        --white:   #FFFFFF;
        --off:     #F0EDE8;
        --dark:    #1A1A1A;
        --dark2:   #111111;
        --grey:    #6B6B6B;
        --grey2:   #9B9B9B;
        --border:  #E8E4DE;
        --red:     #C0392B;
        --red-lt:  #E8463A;
    }

    /* ── GLOBAL RESET ── */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    .main .block-container {
        background: var(--white) !important;
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: var(--dark) !important;
    }

    /* Hide EVERYTHING Streamlit */
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="stSidebar"],
    #MainMenu, footer, header,
    .stDeployButton,
    div[data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* ── NAV ── */
    .kl-nav {
        position: sticky; top: 0; z-index: 999;
        background: var(--white);
        border-bottom: 1px solid var(--border);
        display: flex; align-items: center;
        justify-content: space-between;
        padding: 0 56px; height: 72px;
    }
    .kl-logo {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 20px; font-weight: 900;
        color: var(--dark2); letter-spacing: -0.5px;
        display: flex; align-items: center; gap: 8px;
    }
    .kl-nav-links {
        display: flex; gap: 40px;
    }
    .kl-nav-link {
        font-size: 15px; font-weight: 600;
        color: var(--dark); text-decoration: none;
        letter-spacing: -0.2px;
    }
    .kl-nav-right { display: flex; gap: 12px; align-items: center; }
    .kl-btn-outline {
        padding: 10px 22px; border-radius: 100px;
        font-size: 15px; font-weight: 700;
        color: var(--dark); background: transparent;
        border: 1.5px solid var(--dark); cursor: pointer;
        font-family: 'Plus Jakarta Sans', sans-serif;
        transition: all 0.15s; white-space: nowrap;
        letter-spacing: -0.2px;
    }
    .kl-btn-outline:hover { background: var(--dark); color: #fff; }
    .kl-btn-black {
        padding: 10px 22px; border-radius: 100px;
        font-size: 15px; font-weight: 700;
        color: #fff; background: var(--dark2);
        border: none; cursor: pointer;
        font-family: 'Plus Jakarta Sans', sans-serif;
        transition: all 0.15s; white-space: nowrap;
        letter-spacing: -0.2px;
    }
    .kl-btn-black:hover { background: #333; }

    /* ── HERO ── */
    .kl-hero {
        background: var(--white);
        padding: 80px 56px 0;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 80px; align-items: flex-start;
        max-width: 1280px; margin: 0 auto;
    }
    .kl-hero-eyebrow {
        font-size: 13px; font-weight: 800;
        letter-spacing: 1.5px; text-transform: uppercase;
        color: var(--red); margin-bottom: 20px;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .kl-hero-h1 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 58px; font-weight: 900;
        line-height: 1.05; letter-spacing: -2px;
        color: var(--dark2); margin-bottom: 28px;
    }
    .kl-hero-sub {
        font-size: 18px; line-height: 1.6;
        color: var(--grey); font-weight: 400;
        margin-bottom: 40px; max-width: 420px;
        letter-spacing: -0.2px;
    }
    .kl-hero-ctas {
        display: flex; gap: 14px; align-items: center;
        flex-wrap: wrap;
    }
    .kl-cta-black {
        padding: 14px 28px; border-radius: 100px;
        font-size: 16px; font-weight: 800;
        color: #fff; background: var(--dark2);
        border: none; cursor: pointer;
        font-family: 'Plus Jakarta Sans', sans-serif;
        letter-spacing: -0.3px; transition: all 0.15s;
        text-decoration: none; display: inline-block;
    }
    .kl-cta-black:hover { background: #333; }
    .kl-cta-text {
        font-size: 15px; font-weight: 700;
        color: var(--dark); text-decoration: none;
        letter-spacing: -0.2px;
        border-bottom: 2px solid var(--dark);
        padding-bottom: 2px;
    }
    .kl-hero-trust {
        display: flex; align-items: center; gap: 12px;
        margin-top: 36px; font-size: 13px;
        color: var(--grey2); font-weight: 500;
    }
    .kl-avatars { display: flex; }
    .kl-av {
        width: 30px; height: 30px; border-radius: 50%;
        border: 2px solid #fff;
        background: var(--off); margin-left: -8px;
        font-size: 12px; display: flex;
        align-items: center; justify-content: center;
    }
    .kl-av:first-child { margin-left: 0; }

    /* ── HERO RIGHT CARD ── */
    .kl-hero-card {
        background: var(--dark2);
        border-radius: 20px; overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.18);
        margin-top: 8px;
    }
    .kl-card-top {
        padding: 32px 36px 28px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .kl-card-eyebrow {
        font-size: 11px; font-weight: 700;
        letter-spacing: 1.2px; text-transform: uppercase;
        color: rgba(255,255,255,0.35); margin-bottom: 10px;
    }
    .kl-card-num {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 54px; font-weight: 900;
        letter-spacing: -2px; color: #fff;
        line-height: 1; margin-bottom: 6px;
    }
    .kl-card-sub {
        font-size: 14px; color: rgba(255,255,255,0.4);
        font-weight: 500;
    }
    .kl-card-body { padding: 8px 0; }
    .kl-card-row {
        display: flex; justify-content: space-between;
        align-items: center; padding: 16px 36px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .kl-card-row:last-child { border-bottom: none; }
    .kl-row-label {
        font-size: 14px; color: rgba(255,255,255,0.45);
        font-weight: 500;
    }
    .kl-row-val {
        font-size: 15px; font-weight: 800;
        color: #fff; letter-spacing: -0.3px;
    }
    .kl-row-val.green { color: #4ADE80; }
    .kl-row-badge {
        font-size: 12px; font-weight: 800;
        background: rgba(74,222,128,0.15);
        color: #4ADE80;
        padding: 4px 12px; border-radius: 100px;
        letter-spacing: -0.2px;
    }

    /* ── WAVE DIVIDER ── */
    .kl-wave {
        width: 100%; overflow: hidden;
        line-height: 0; margin-top: -2px;
    }

    /* ── PLATFORMS BAR ── */
    .kl-platforms {
        background: var(--off);
        padding: 24px 56px;
        display: flex; align-items: center;
        justify-content: center; gap: 40px;
        flex-wrap: wrap;
        border-top: 1px solid var(--border);
        border-bottom: 1px solid var(--border);
    }
    .kl-platforms-label {
        font-size: 12px; font-weight: 800;
        letter-spacing: 1.2px; text-transform: uppercase;
        color: var(--grey2);
    }
    .kl-platform {
        font-size: 14px; font-weight: 700;
        color: var(--grey); letter-spacing: -0.2px;
    }

    /* ── SECTION ── */
    .kl-section {
        padding: 96px 56px;
        max-width: 1280px; margin: 0 auto;
    }
    .kl-section-eyebrow {
        font-size: 13px; font-weight: 800;
        letter-spacing: 1.2px; text-transform: uppercase;
        color: var(--red); margin-bottom: 20px;
    }
    .kl-section-h2 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 48px; font-weight: 900;
        letter-spacing: -2px; line-height: 1.08;
        color: var(--dark2); margin-bottom: 20px;
    }
    .kl-section-sub {
        font-size: 18px; color: var(--grey);
        line-height: 1.6; max-width: 500px;
        margin-bottom: 56px; font-weight: 400;
    }

    /* ── STEPS GRID ── */
    .kl-steps {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
    }
    .kl-step {
        background: var(--off);
        border-radius: 16px; padding: 32px 28px;
        position: relative; overflow: hidden;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .kl-step:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.08);
    }
    .kl-step-num {
        position: absolute; top: 20px; right: 20px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 72px; font-weight: 900;
        color: rgba(26,26,26,0.05);
        line-height: 1; letter-spacing: -3px;
    }
    .kl-step-icon { font-size: 28px; margin-bottom: 20px; }
    .kl-step-title {
        font-size: 17px; font-weight: 800;
        color: var(--dark2); margin-bottom: 10px;
        letter-spacing: -0.4px;
    }
    .kl-step-desc {
        font-size: 14px; color: var(--grey);
        line-height: 1.65; font-weight: 400;
    }

    /* ── STATS — dark section ── */
    .kl-dark-section {
        background: var(--dark2);
        padding: 80px 56px;
    }
    .kl-dark-inner {
        max-width: 1280px; margin: 0 auto;
        display: grid; grid-template-columns: repeat(4,1fr);
        gap: 24px;
    }
    .kl-dark-stat { text-align: center; }
    .kl-dark-num {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 56px; font-weight: 900;
        letter-spacing: -2px; color: #fff;
        margin-bottom: 8px; line-height: 1;
    }
    .kl-dark-label {
        font-size: 15px; color: rgba(255,255,255,0.4);
        font-weight: 500;
    }

    /* ── PRICING ── */
    .kl-pricing-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }
    .kl-plan {
        background: var(--off);
        border-radius: 20px; padding: 36px 32px;
        position: relative; transition: all 0.2s;
    }
    .kl-plan:hover {
        box-shadow: 0 12px 40px rgba(0,0,0,0.1);
        transform: translateY(-3px);
    }
    .kl-plan.featured {
        background: var(--dark2);
    }
    .kl-plan-badge {
        position: absolute; top: -13px; left: 50%;
        transform: translateX(-50%);
        background: var(--red-lt); color: #fff;
        font-size: 11px; font-weight: 800;
        letter-spacing: 0.8px; text-transform: uppercase;
        padding: 4px 16px; border-radius: 100px;
        white-space: nowrap;
    }
    .kl-plan-name {
        font-size: 13px; font-weight: 800;
        letter-spacing: 1.2px; text-transform: uppercase;
        color: var(--grey2); margin-bottom: 16px;
    }
    .kl-plan.featured .kl-plan-name {
        color: rgba(255,255,255,0.35);
    }
    .kl-plan-price {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 52px; font-weight: 900;
        letter-spacing: -2px; color: var(--dark2);
        line-height: 1; margin-bottom: 4px;
    }
    .kl-plan.featured .kl-plan-price { color: #fff; }
    .kl-plan-period {
        font-size: 14px; color: var(--grey2);
        margin-bottom: 28px; font-weight: 500;
    }
    .kl-plan.featured .kl-plan-period {
        color: rgba(255,255,255,0.3);
    }
    .kl-plan-divider {
        border: none;
        border-top: 1px solid rgba(26,26,26,0.1);
        margin: 0 0 24px;
    }
    .kl-plan.featured .kl-plan-divider {
        border-color: rgba(255,255,255,0.1);
    }
    .kl-plan-features {
        list-style: none; padding: 0; margin: 0 0 32px;
    }
    .kl-plan-features li {
        display: flex; align-items: flex-start; gap: 10px;
        font-size: 14px; color: var(--grey);
        padding: 7px 0; font-weight: 500;
        letter-spacing: -0.1px;
    }
    .kl-plan.featured .kl-plan-features li {
        color: rgba(255,255,255,0.6);
    }
    .kl-check {
        font-size: 14px; flex-shrink: 0;
        margin-top: 1px; color: var(--dark2);
        font-weight: 900;
    }
    .kl-plan.featured .kl-check { color: #4ADE80; }
    .kl-plan-btn {
        width: 100%; padding: 14px;
        border-radius: 100px; font-size: 15px;
        font-weight: 800; cursor: pointer;
        font-family: 'Plus Jakarta Sans', sans-serif;
        transition: all 0.2s; letter-spacing: -0.2px;
        border: 1.5px solid var(--dark2);
        background: transparent; color: var(--dark2);
    }
    .kl-plan.featured .kl-plan-btn {
        background: #fff; color: var(--dark2); border-color: #fff;
    }
    .kl-plan-btn:hover { background: var(--dark2); color: #fff; }
    .kl-plan.featured .kl-plan-btn:hover {
        background: rgba(255,255,255,0.85);
    }

    /* ── SCAN SECTION ── */
    .kl-scan-wrap {
        background: var(--off);
        border-top: 1px solid var(--border);
        padding: 80px 56px;
    }
    .kl-scan-center {
        max-width: 640px; margin: 0 auto; text-align: center;
    }
    .kl-scan-form-card {
        background: var(--white);
        border: 1px solid var(--border);
        border-radius: 20px; padding: 40px;
        margin-top: 40px; text-align: left;
        box-shadow: 0 4px 24px rgba(0,0,0,0.05);
    }
    .kl-field-label {
        font-size: 12px; font-weight: 800;
        letter-spacing: 0.8px; text-transform: uppercase;
        color: var(--grey2); margin-bottom: 6px;
        margin-top: 20px; display: block;
    }
    .kl-field-label:first-child { margin-top: 0; }

    /* Streamlit overrides */
    .stTextInput input, .stTextArea textarea {
        background: var(--off) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--dark2) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 15px !important; font-weight: 500 !important;
        padding: 12px 16px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--dark2) !important;
        box-shadow: 0 0 0 3px rgba(26,26,26,0.08) !important;
    }
    .stSelectbox > div > div {
        background: var(--off) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--dark2) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 15px !important;
    }
    .stButton > button {
        background: var(--dark2) !important;
        color: #fff !important; border: none !important;
        border-radius: 100px !important;
        padding: 14px 28px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 15px !important; font-weight: 800 !important;
        width: 100% !important; letter-spacing: -0.2px !important;
        transition: all 0.15s !important;
    }
    .stButton > button:hover { background: #333 !important; }

    /* ── FOOTER ── */
    .kl-footer {
        background: var(--dark2);
        padding: 64px 56px 40px;
    }
    .kl-footer-inner { max-width: 1280px; margin: 0 auto; }
    .kl-footer-top {
        display: flex; justify-content: space-between;
        padding-bottom: 48px; margin-bottom: 40px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        gap: 48px;
    }
    .kl-footer-brand { flex: 1.5; }
    .kl-footer-logo {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 20px; font-weight: 900; color: #fff;
        margin-bottom: 12px;
    }
    .kl-footer-tagline {
        font-size: 14px; color: rgba(255,255,255,0.3);
        line-height: 1.65; max-width: 240px; font-weight: 400;
    }
    .kl-footer-col { flex: 1; }
    .kl-footer-col-title {
        font-size: 11px; font-weight: 800;
        letter-spacing: 1.2px; text-transform: uppercase;
        color: rgba(255,255,255,0.3); margin-bottom: 16px;
    }
    .kl-footer-link {
        display: block; font-size: 14px;
        color: rgba(255,255,255,0.55);
        margin-bottom: 10px; text-decoration: none;
        font-weight: 500; transition: color 0.15s;
    }
    .kl-footer-link:hover { color: #fff; }
    .kl-footer-bottom {
        display: flex; justify-content: space-between;
        font-size: 13px; color: rgba(255,255,255,0.2);
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── NAV ───────────────────────────────────────────────────
    st.markdown("""
    <div class="kl-nav">
        <div class="kl-logo">👻 GhostRights</div>
        <div class="kl-nav-links">
            <a class="kl-nav-link" href="#">How It Works</a>
            <a class="kl-nav-link" href="#">Pricing</a>
            <a class="kl-nav-link" href="#">For Labels</a>
        </div>
        <div class="kl-nav-right">
            <button class="kl-btn-outline" onclick="">Log in</button>
            <button class="kl-btn-black" onclick="">Get a free scan</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hidden Streamlit nav buttons
    c1, c2, c3 = st.columns([8, 1, 1])
    with c2:
        if st.button("Log in", key="nav_login"):
            st.session_state.current_page = "login"
            st.rerun()
    with c3:
        if st.button("Sign up", key="nav_signup"):
            st.session_state.current_page = "signup"
            st.rerun()

    # ── HERO ──────────────────────────────────────────────────
    st.markdown("""
    <div style="max-width:1280px;margin:0 auto;padding:80px 56px 0;">
    <div class="kl-hero" style="max-width:100%;padding:0;">
        <div>
            <div class="kl-hero-eyebrow">The Creator Protection Platform</div>
            <h1 class="kl-hero-h1">
                Pirates are<br>
                profiting from<br>
                your content.
            </h1>
            <p class="kl-hero-sub">
                GhostRights finds every stolen copy of your movies,
                music, and videos — then makes pirates pay you,
                or destroys them. Automatically.
            </p>
            <div class="kl-hero-ctas">
                <a class="kl-cta-black" href="#">Get a free scan</a>
                <a class="kl-cta-text" href="#">See how it works →</a>
            </div>
            <div class="kl-hero-trust">
                <div class="kl-avatars">
                    <div class="kl-av">🎬</div>
                    <div class="kl-av">🎵</div>
                    <div class="kl-av">📺</div>
                    <div class="kl-av">🎙</div>
                </div>
                Trusted by Nollywood filmmakers &amp; Afrobeats artists
            </div>
        </div>
        <div>
            <div class="kl-hero-card">
                <div class="kl-card-top">
                    <div class="kl-card-eyebrow">Revenue recovered this month</div>
                    <div class="kl-card-num">₦2.3M</div>
                    <div class="kl-card-sub">across all GhostRights creators</div>
                </div>
                <div class="kl-card-body">
                    <div class="kl-card-row">
                        <span class="kl-row-label">Pirated copies found</span>
                        <span class="kl-row-val">1,847</span>
                    </div>
                    <div class="kl-card-row">
                        <span class="kl-row-label">Takedowns sent</span>
                        <span class="kl-row-val">634</span>
                    </div>
                    <div class="kl-card-row">
                        <span class="kl-row-label">Monetised copies</span>
                        <span class="kl-row-val green">1,213</span>
                    </div>
                    <div class="kl-card-row">
                        <span class="kl-row-label">Detection accuracy</span>
                        <span class="kl-row-badge">94.7%</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PLATFORMS ─────────────────────────────────────────────
    st.markdown("""
    <div style="margin-top:64px;">
    <div class="kl-platforms">
        <span class="kl-platforms-label">We hunt pirates on</span>
        <span class="kl-platform">📺 YouTube</span>
        <span class="kl-platform">📘 Facebook</span>
        <span class="kl-platform">✈️ Telegram</span>
        <span class="kl-platform">🎵 TikTok</span>
        <span class="kl-platform">📷 Instagram</span>
        <span class="kl-platform">🏴‍☠️ Torrent Sites</span>
        <span class="kl-platform">📝 Blogs</span>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ── HOW IT WORKS ──────────────────────────────────────────
    st.markdown("""
    <div class="kl-section">
        <div class="kl-section-eyebrow">How It Works</div>
        <h2 class="kl-section-h2">From upload to paid<br>in 4 steps.</h2>
        <p class="kl-section-sub">
            GhostRights runs in the background,
            24 hours a day. You create. We protect.
        </p>
        <div class="kl-steps">
            <div class="kl-step">
                <div class="kl-step-num">01</div>
                <div class="kl-step-icon">📁</div>
                <div class="kl-step-title">Upload your content</div>
                <div class="kl-step-desc">Upload your movie, song, or video. We fingerprint it instantly — our crawlers know exactly what to hunt.</div>
            </div>
            <div class="kl-step">
                <div class="kl-step-num">02</div>
                <div class="kl-step-icon">🕷️</div>
                <div class="kl-step-title">Crawlers start hunting</div>
                <div class="kl-step-desc">Our AI scans YouTube, Facebook, Telegram, TikTok, blogs, and torrent sites every single hour.</div>
            </div>
            <div class="kl-step">
                <div class="kl-step-num">03</div>
                <div class="kl-step-icon">🎯</div>
                <div class="kl-step-title">Piracy detected</div>
                <div class="kl-step-desc">You get an instant alert. Choose to monetise the pirated copy or send an automated DMCA takedown.</div>
            </div>
            <div class="kl-step">
                <div class="kl-step-num">04</div>
                <div class="kl-step-icon">💰</div>
                <div class="kl-step-title">You get paid</div>
                <div class="kl-step-desc">Ad revenue from pirated copies flows to your account. Pirates pay you. Every month, automatically.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── DARK STATS ────────────────────────────────────────────
    st.markdown("""
    <div class="kl-dark-section">
        <div class="kl-dark-inner">
            <div class="kl-dark-stat">
                <div class="kl-dark-num">1,800+</div>
                <div class="kl-dark-label">Pirated copies found monthly</div>
            </div>
            <div class="kl-dark-stat">
                <div class="kl-dark-num">₦2.3M</div>
                <div class="kl-dark-label">Revenue recovered</div>
            </div>
            <div class="kl-dark-stat">
                <div class="kl-dark-num">7</div>
                <div class="kl-dark-label">Platforms monitored</div>
            </div>
            <div class="kl-dark-stat">
                <div class="kl-dark-num">94.7%</div>
                <div class="kl-dark-label">Detection accuracy</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PRICING ───────────────────────────────────────────────
    st.markdown("""
    <div class="kl-section">
        <div class="kl-section-eyebrow">Pricing</div>
        <h2 class="kl-section-h2">Pay once.<br>Earn forever.</h2>
        <p class="kl-section-sub">
            Every plan includes a free piracy scan.
            No credit card required to start.
        </p>
        <div class="kl-pricing-grid">
            <div class="kl-plan">
                <div class="kl-plan-name">Starter</div>
                <div class="kl-plan-price">₦8k</div>
                <div class="kl-plan-period">per month</div>
                <hr class="kl-plan-divider">
                <ul class="kl-plan-features">
                    <li><span class="kl-check">✓</span> Up to 5 content items</li>
                    <li><span class="kl-check">✓</span> YouTube &amp; Facebook monitoring</li>
                    <li><span class="kl-check">✓</span> Email alerts</li>
                    <li><span class="kl-check">✓</span> DMCA takedowns</li>
                    <li><span class="kl-check">✓</span> Monthly piracy report</li>
                </ul>
                <button class="kl-plan-btn">Get started →</button>
            </div>
            <div class="kl-plan featured">
                <div class="kl-plan-badge">Most Popular</div>
                <div class="kl-plan-name">Pro</div>
                <div class="kl-plan-price">₦20k</div>
                <div class="kl-plan-period">per month</div>
                <hr class="kl-plan-divider">
                <ul class="kl-plan-features">
                    <li><span class="kl-check">✓</span> Up to 25 content items</li>
                    <li><span class="kl-check">✓</span> All 7 platforms monitored</li>
                    <li><span class="kl-check">✓</span> WhatsApp + email alerts</li>
                    <li><span class="kl-check">✓</span> Ad revenue monetisation</li>
                    <li><span class="kl-check">✓</span> Watermark leak tracing</li>
                </ul>
                <button class="kl-plan-btn">Get Pro →</button>
            </div>
            <div class="kl-plan">
                <div class="kl-plan-name">Studio</div>
                <div class="kl-plan-price">₦75k</div>
                <div class="kl-plan-period">per month</div>
                <hr class="kl-plan-divider">
                <ul class="kl-plan-features">
                    <li><span class="kl-check">✓</span> Unlimited content items</li>
                    <li><span class="kl-check">✓</span> All platforms + dark web</li>
                    <li><span class="kl-check">✓</span> Dedicated account manager</li>
                    <li><span class="kl-check">✓</span> PDF intelligence reports</li>
                    <li><span class="kl-check">✓</span> Full API access</li>
                </ul>
                <button class="kl-plan-btn">Contact sales →</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── FREE SCAN ─────────────────────────────────────────────
    st.markdown("""
    <div class="kl-scan-wrap">
        <div class="kl-scan-center">
            <div class="kl-section-eyebrow">Free Piracy Scan</div>
            <h2 class="kl-section-h2" style="font-size:42px;">
                See who's stealing<br>your content right now.
            </h2>
            <p style="font-size:17px;color:#6B6B6B;line-height:1.6;font-weight:400;">
                No credit card. No account needed.
                Results in 60 seconds.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, form_col, _ = st.columns([1, 2, 1])
    with form_col:
        st.markdown('<div class="kl-scan-form-card">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'Plus Jakarta Sans',sans-serif;
             font-size:22px;font-weight:900;color:#111111;
             letter-spacing:-0.5px;margin-bottom:28px;">
            Run your free scan
        </div>""", unsafe_allow_html=True)

        st.markdown('<span class="kl-field-label">Your name</span>',
                    unsafe_allow_html=True)
        name = st.text_input("n", placeholder="e.g. Kunle Afolayan",
                             label_visibility="collapsed", key="scan_name")

        st.markdown('<span class="kl-field-label">Email address</span>',
                    unsafe_allow_html=True)
        email = st.text_input("e", placeholder="you@email.com",
                              label_visibility="collapsed", key="scan_email")

        st.markdown('<span class="kl-field-label">Content title</span>',
                    unsafe_allow_html=True)
        content_title = st.text_input("c",
            placeholder="e.g. Living In Bondage, Essence",
            label_visibility="collapsed", key="scan_title")

        st.markdown('<span class="kl-field-label">Content type</span>',
                    unsafe_allow_html=True)
        content_type = st.selectbox("t",
            ["Movie / Film", "Music Track", "YouTube Video",
             "Podcast", "Album", "Short Film", "Other"],
            label_visibility="collapsed", key="scan_type")

        st.markdown("<div style='margin-top:28px;'></div>",
                    unsafe_allow_html=True)

        if st.button("Scan my content for free →", key="run_scan"):
            if not name or not email or not content_title:
                st.error("Please fill in all fields.")
            else:
                _save_scan_lead(name, email, content_title, content_type)
                st.markdown('</div>', unsafe_allow_html=True)
                _show_scan_results(content_title)
                return

        st.markdown('</div>', unsafe_allow_html=True)

    # ── FOOTER ────────────────────────────────────────────────
    st.markdown("""
    <div class="kl-footer">
        <div class="kl-footer-inner">
            <div class="kl-footer-top">
                <div class="kl-footer-brand">
                    <div class="kl-footer-logo">👻 GhostRights</div>
                    <div class="kl-footer-tagline">
                        AI-powered content protection
                        for African creators.
                    </div>
                </div>
                <div class="kl-footer-col">
                    <div class="kl-footer-col-title">Product</div>
                    <a class="kl-footer-link" href="#">How It Works</a>
                    <a class="kl-footer-link" href="#">Pricing</a>
                    <a class="kl-footer-link" href="#">Free Scan</a>
                    <a class="kl-footer-link" href="#">For Labels</a>
                </div>
                <div class="kl-footer-col">
                    <div class="kl-footer-col-title">Legal</div>
                    <a class="kl-footer-link" href="#">Privacy Policy</a>
                    <a class="kl-footer-link" href="#">Terms of Service</a>
                    <a class="kl-footer-link" href="#">DMCA Policy</a>
                </div>
                <div class="kl-footer-col">
                    <div class="kl-footer-col-title">Contact</div>
                    <a class="kl-footer-link" href="#">support@ghostrights.com</a>
                    <a class="kl-footer-link" href="#">WhatsApp</a>
                    <a class="kl-footer-link" href="#">Twitter / X</a>
                </div>
            </div>
            <div class="kl-footer-bottom">
                <div>© 2025 GhostRights. All rights reserved.</div>
                <div>Built for African creators 🌍</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _save_scan_lead(name, email, content_title, content_type):
    try:
        admin = get_supabase_admin()
        admin.table("free_scan_leads").insert({
            "name": name, "email": email,
            "content_title": content_title,
            "content_type": content_type,
            "scan_status": "completed"
        }).execute()
    except Exception:
        pass


def _show_scan_results(title):
    import random
    copies  = random.randint(12, 47)
    views   = random.randint(80000, 450000)
    revenue = copies * random.randint(800, 2200)

    st.markdown(f"""
    <div style="background:#fff;border:1.5px solid #E8E4DE;
         border-radius:20px;padding:40px;margin-top:32px;
         max-width:640px;margin-left:auto;margin-right:auto;
         box-shadow:0 8px 32px rgba(0,0,0,0.08);">
        <div style="display:flex;align-items:center;gap:10px;
             margin-bottom:28px;">
            <div style="width:10px;height:10px;border-radius:50%;
                 background:#E8463A;flex-shrink:0;"></div>
            <span style="font-family:'Plus Jakarta Sans',sans-serif;
                  font-weight:800;font-size:16px;color:#E8463A;
                  letter-spacing:-0.3px;">
                Piracy detected for "{title}"
            </span>
        </div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);
             gap:16px;margin-bottom:28px;">
            <div style="text-align:center;padding:24px 16px;
                 background:#F0EDE8;border-radius:14px;">
                <div style="font-family:'Plus Jakarta Sans',sans-serif;
                     font-size:44px;font-weight:900;color:#E8463A;
                     letter-spacing:-2px;line-height:1;">
                    {copies}
                </div>
                <div style="font-size:13px;color:#6B6B6B;
                     margin-top:6px;font-weight:600;">
                    Pirated copies
                </div>
            </div>
            <div style="text-align:center;padding:24px 16px;
                 background:#F0EDE8;border-radius:14px;">
                <div style="font-family:'Plus Jakarta Sans',sans-serif;
                     font-size:44px;font-weight:900;color:#1A1A1A;
                     letter-spacing:-2px;line-height:1;">
                    {views//1000}K
                </div>
                <div style="font-size:13px;color:#6B6B6B;
                     margin-top:6px;font-weight:600;">
                    Stolen views
                </div>
            </div>
            <div style="text-align:center;padding:24px 16px;
                 background:#111111;border-radius:14px;">
                <div style="font-family:'Plus Jakarta Sans',sans-serif;
                     font-size:36px;font-weight:900;color:#4ADE80;
                     letter-spacing:-1px;line-height:1;">
                    ₦{revenue//1000}K
                </div>
                <div style="font-size:13px;color:rgba(255,255,255,0.4);
                     margin-top:6px;font-weight:600;">
                    Recoverable
                </div>
            </div>
        </div>
        <p style="font-size:13px;color:#9B9B9B;text-align:center;
             font-weight:500;margin:0;">
            ⚠️ Sample scan. Create a free account to see real piracy data.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Protect my content →", key="scan_cta1"):
            st.session_state.current_page = "signup"
            st.rerun()
    with c2:
        if st.button("Log in to my account", key="scan_cta2"):
            st.session_state.current_page = "login"
            st.rerun()

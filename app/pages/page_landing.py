import streamlit as st
from database.db import get_supabase_admin

def render():

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Figtree:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --bg:        #F5F3EE;
        --bg2:       #EDEAE2;
        --ink:       #1C1C1A;
        --ink2:      #4A4A45;
        --ink3:      #8A8A82;
        --green:     #2D6A4F;
        --green-lt:  #52B788;
        --green-bg:  #D8F3DC;
        --green-cta: #1B4332;
        --lime:      #B7E4C7;
        --border:    rgba(28,28,26,0.10);
        --border2:   rgba(28,28,26,0.06);
    }

    html, body, [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: var(--bg) !important;
        color: var(--ink) !important;
        font-family: 'Figtree', sans-serif !important;
    }
    [data-testid="stHeader"],
    [data-testid="stToolbar"] { display: none !important; }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    section[data-testid="stMain"] > div { padding: 0 !important; }

    /* NAV */
    .gr-nav {
        display: flex; align-items: center;
        justify-content: space-between;
        padding: 0 48px; height: 68px;
        background: var(--bg);
        border-bottom: 1px solid var(--border);
        position: sticky; top: 0; z-index: 100;
    }
    .gr-nav-logo {
        font-family: 'Figtree', sans-serif;
        font-weight: 900; font-size: 22px;
        color: var(--green-cta); letter-spacing: -0.5px;
    }
    .gr-nav-links { display: flex; gap: 36px; align-items: center; }
    .gr-nav-link {
        font-size: 14px; font-weight: 500;
        color: var(--ink2); text-decoration: none;
    }

    /* HERO */
    .gr-hero {
        max-width: 1180px; margin: 0 auto;
        padding: 96px 48px 80px;
        display: grid; grid-template-columns: 1fr 1fr;
        gap: 64px; align-items: center;
    }
    .gr-hero-badge {
        display: inline-flex; align-items: center; gap: 7px;
        background: var(--green-bg); color: var(--green);
        font-size: 12px; font-weight: 700;
        letter-spacing: 0.8px; text-transform: uppercase;
        padding: 6px 14px; border-radius: 100px;
        margin-bottom: 28px;
    }
    .gr-dot {
        width: 7px; height: 7px;
        background: var(--green-lt); border-radius: 50%;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%,100%{opacity:1;transform:scale(1)}
        50%{opacity:0.5;transform:scale(0.8)}
    }
    .gr-hero-h1 {
        font-family: 'Instrument Serif', serif;
        font-size: 60px; line-height: 1.08;
        font-weight: 400; color: var(--ink);
        letter-spacing: -1px; margin-bottom: 24px;
    }
    .gr-hero-h1 em { font-style: italic; color: var(--green); }
    .gr-hero-sub {
        font-size: 18px; line-height: 1.65;
        color: var(--ink2); margin-bottom: 40px;
        max-width: 440px;
    }
    .gr-cta-primary {
        display: inline-block;
        background: var(--green-cta); color: #fff;
        font-family: 'Figtree', sans-serif;
        font-size: 15px; font-weight: 700;
        padding: 14px 28px; border-radius: 8px;
        text-decoration: none;
    }
    .gr-hero-trust {
        display: flex; align-items: center; gap: 12px;
        margin-top: 32px; font-size: 13px; color: var(--ink3);
    }
    .gr-trust-avatars { display: flex; }
    .gr-avatar {
        width: 32px; height: 32px; border-radius: 50%;
        border: 2px solid var(--bg);
        background: var(--green-bg); margin-left: -8px;
        font-size: 13px; display: flex;
        align-items: center; justify-content: center;
    }
    .gr-avatar:first-child { margin-left: 0; }

    /* HERO CARD */
    .gr-hero-card {
        background: #fff; border: 1px solid var(--border);
        border-radius: 20px; overflow: hidden;
        box-shadow: 0 4px 40px rgba(28,28,26,0.08);
    }
    .gr-hero-card-top {
        background: var(--green-cta);
        padding: 28px 32px; color: #fff;
    }
    .gr-card-label {
        font-size: 11px; font-weight: 600;
        letter-spacing: 1px; text-transform: uppercase;
        opacity: 0.6; margin-bottom: 8px;
    }
    .gr-card-big-num {
        font-family: 'Instrument Serif', serif;
        font-size: 52px; line-height: 1;
        color: var(--lime); margin-bottom: 4px;
    }
    .gr-card-big-sub { font-size: 14px; opacity: 0.7; }
    .gr-hero-card-body { padding: 24px 32px; }
    .gr-card-stat-row {
        display: flex; justify-content: space-between;
        align-items: center; padding: 14px 0;
        border-bottom: 1px solid var(--border2);
    }
    .gr-card-stat-row:last-child { border-bottom: none; }
    .gr-stat-name { font-size: 14px; color: var(--ink2); font-weight: 500; }
    .gr-stat-val { font-size: 15px; font-weight: 700; color: var(--ink); }
    .gr-stat-val.green { color: var(--green); }
    .gr-stat-badge {
        font-size: 11px; font-weight: 700;
        background: var(--green-bg); color: var(--green);
        padding: 3px 10px; border-radius: 100px;
    }

    /* PLATFORMS BAR */
    .gr-logos-bar {
        background: var(--bg2);
        border-top: 1px solid var(--border);
        border-bottom: 1px solid var(--border);
        padding: 20px 48px;
        display: flex; align-items: center;
        justify-content: center; gap: 48px; flex-wrap: wrap;
    }
    .gr-logos-label {
        font-size: 12px; font-weight: 600;
        letter-spacing: 0.5px; text-transform: uppercase;
        color: var(--ink3); white-space: nowrap;
    }
    .gr-platform-pill {
        display: flex; align-items: center; gap: 8px;
        font-size: 14px; font-weight: 600; color: var(--ink2);
    }

    /* SECTION */
    .gr-section {
        max-width: 1180px; margin: 0 auto;
        padding: 96px 48px;
    }
    .gr-section-label {
        font-size: 12px; font-weight: 700;
        letter-spacing: 1.2px; text-transform: uppercase;
        color: var(--green); margin-bottom: 16px;
    }
    .gr-section-h2 {
        font-family: 'Instrument Serif', serif;
        font-size: 44px; line-height: 1.12;
        font-weight: 400; color: var(--ink);
        letter-spacing: -0.5px; margin-bottom: 16px;
    }
    .gr-section-h2 em { font-style: italic; color: var(--green); }
    .gr-section-sub {
        font-size: 17px; color: var(--ink2);
        line-height: 1.65; max-width: 520px;
        margin-bottom: 56px;
    }

    /* STEPS */
    .gr-steps {
        display: grid; grid-template-columns: repeat(4, 1fr);
        gap: 24px;
    }
    .gr-step {
        background: #fff; border: 1px solid var(--border);
        border-radius: 16px; padding: 32px 28px;
        position: relative; overflow: hidden;
        transition: box-shadow 0.2s;
    }
    .gr-step:hover { box-shadow: 0 8px 32px rgba(28,28,26,0.08); }
    .gr-step-num {
        position: absolute; top: 16px; right: 20px;
        font-family: 'Instrument Serif', serif;
        font-size: 80px; line-height: 1;
        color: rgba(28,28,26,0.05); font-weight: 400;
    }
    .gr-step-icon { font-size: 32px; margin-bottom: 20px; }
    .gr-step-title {
        font-size: 17px; font-weight: 700;
        color: var(--ink); margin-bottom: 10px;
    }
    .gr-step-desc {
        font-size: 14px; color: var(--ink2); line-height: 1.65;
    }

    /* STATS STRIP */
    .gr-stats-strip {
        background: var(--green-cta); padding: 64px 48px;
    }
    .gr-stats-strip-inner {
        max-width: 1180px; margin: 0 auto;
        display: grid; grid-template-columns: repeat(4, 1fr);
        gap: 32px;
    }
    .gr-big-stat { text-align: center; }
    .gr-big-stat-num {
        font-family: 'Instrument Serif', serif;
        font-size: 56px; line-height: 1;
        color: var(--lime); font-weight: 400; margin-bottom: 8px;
    }
    .gr-big-stat-label {
        font-size: 15px; color: rgba(255,255,255,0.6); font-weight: 500;
    }

    /* PRICING */
    .gr-pricing-grid {
        display: grid; grid-template-columns: repeat(3, 1fr);
        gap: 24px;
    }
    .gr-plan {
        background: #fff; border: 1px solid var(--border);
        border-radius: 20px; padding: 36px 32px;
        position: relative; transition: all 0.2s;
    }
    .gr-plan:hover {
        box-shadow: 0 8px 40px rgba(28,28,26,0.1);
        transform: translateY(-2px);
    }
    .gr-plan.featured {
        background: var(--green-cta);
        border-color: var(--green-cta);
    }
    .gr-plan-badge {
        position: absolute; top: -13px; left: 50%;
        transform: translateX(-50%);
        background: var(--green-lt); color: var(--green-cta);
        font-size: 11px; font-weight: 800;
        letter-spacing: 0.8px; text-transform: uppercase;
        padding: 4px 16px; border-radius: 100px;
        white-space: nowrap;
    }
    .gr-plan-name {
        font-size: 13px; font-weight: 700;
        letter-spacing: 0.8px; text-transform: uppercase;
        color: var(--ink3); margin-bottom: 16px;
    }
    .gr-plan.featured .gr-plan-name { color: rgba(255,255,255,0.5); }
    .gr-plan-price {
        font-family: 'Instrument Serif', serif;
        font-size: 48px; font-weight: 400;
        color: var(--ink); line-height: 1; margin-bottom: 4px;
    }
    .gr-plan.featured .gr-plan-price { color: var(--lime); }
    .gr-plan-period {
        font-size: 13px; color: var(--ink3); margin-bottom: 28px;
    }
    .gr-plan.featured .gr-plan-period { color: rgba(255,255,255,0.4); }
    .gr-plan-features { list-style: none; padding: 0; margin: 0 0 32px; }
    .gr-plan-features li {
        display: flex; align-items: center; gap: 10px;
        font-size: 14px; color: var(--ink2); padding: 8px 0;
        border-bottom: 1px solid var(--border2);
    }
    .gr-plan-features li:last-child { border-bottom: none; }
    .gr-plan.featured .gr-plan-features li {
        color: rgba(255,255,255,0.75);
        border-color: rgba(255,255,255,0.08);
    }
    .gr-check { color: var(--green-lt); font-size: 16px; flex-shrink: 0; }
    .gr-plan.featured .gr-check { color: var(--lime); }
    .gr-plan-btn {
        width: 100%; padding: 13px; border-radius: 8px;
        font-size: 15px; font-weight: 700; cursor: pointer;
        font-family: 'Figtree', sans-serif;
        transition: all 0.2s; border: none;
        background: var(--green-cta); color: #fff;
    }
    .gr-plan.featured .gr-plan-btn {
        background: var(--lime); color: var(--green-cta);
    }

    /* SCAN SECTION */
    .gr-scan-section {
        background: var(--bg2);
        border-top: 1px solid var(--border);
        border-bottom: 1px solid var(--border);
        padding: 80px 48px;
    }
    .gr-scan-inner {
        max-width: 720px; margin: 0 auto; text-align: center;
    }
    .gr-scan-form {
        background: #fff; border: 1px solid var(--border);
        border-radius: 20px; padding: 40px; text-align: left;
        box-shadow: 0 4px 24px rgba(28,28,26,0.06);
    }
    .gr-input-label {
        font-size: 12px; font-weight: 700;
        letter-spacing: 0.6px; text-transform: uppercase;
        color: var(--ink3); margin-bottom: 6px; margin-top: 20px;
        display: block;
    }
    .gr-input-label:first-child { margin-top: 0; }

    /* Streamlit overrides */
    .stTextInput input, .stTextArea textarea {
        background: var(--bg) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--ink) !important;
        font-family: 'Figtree', sans-serif !important;
        font-size: 15px !important;
    }
    .stSelectbox > div > div {
        background: var(--bg) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--ink) !important;
        font-family: 'Figtree', sans-serif !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--green) !important;
        box-shadow: 0 0 0 3px rgba(45,106,79,0.08) !important;
    }
    .stButton > button {
        background: var(--green-cta) !important;
        color: #fff !important; border: none !important;
        border-radius: 8px !important;
        padding: 13px 28px !important;
        font-family: 'Figtree', sans-serif !important;
        font-size: 15px !important; font-weight: 700 !important;
        width: 100% !important; transition: all 0.2s !important;
    }
    .stButton > button:hover { background: #143825 !important; }

    /* FOOTER */
    .gr-footer { background: var(--ink); padding: 64px 48px 40px; }
    .gr-footer-inner { max-width: 1180px; margin: 0 auto; }
    .gr-footer-top {
        display: flex; justify-content: space-between;
        align-items: flex-start; margin-bottom: 48px;
        padding-bottom: 48px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .gr-footer-logo {
        font-family: 'Figtree', sans-serif;
        font-weight: 900; font-size: 22px; color: #fff;
    }
    .gr-footer-tagline {
        font-size: 14px; color: rgba(255,255,255,0.35);
        margin-top: 8px; max-width: 260px; line-height: 1.6;
    }
    .gr-footer-col-title {
        font-size: 12px; font-weight: 700;
        letter-spacing: 0.8px; text-transform: uppercase;
        color: rgba(255,255,255,0.35); margin-bottom: 16px;
    }
    .gr-footer-link {
        display: block; font-size: 14px;
        color: rgba(255,255,255,0.6); margin-bottom: 10px;
        text-decoration: none;
    }
    .gr-footer-bottom {
        display: flex; justify-content: space-between;
        font-size: 13px; color: rgba(255,255,255,0.25);
    }

    #MainMenu, footer, header { visibility: hidden !important; }
    div[data-testid="stSidebar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    # ── NAV ───────────────────────────────────────────────────
    st.markdown("""
    <div class="gr-nav">
        <div class="gr-nav-logo">👻 GhostRights</div>
        <div class="gr-nav-links">
            <a class="gr-nav-link" href="#">How It Works</a>
            <a class="gr-nav-link" href="#">Pricing</a>
            <a class="gr-nav-link" href="#">For Labels</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_sp, col_login, col_signup = st.columns([8, 1, 1])
    with col_login:
        if st.button("Log in", key="nav_login"):
            st.session_state.current_page = "login"
            st.rerun()
    with col_signup:
        if st.button("Free scan →", key="nav_signup"):
            st.session_state.current_page = "signup"
            st.rerun()

    # ── HERO ──────────────────────────────────────────────────
    st.markdown("""
    <div class="gr-hero">
        <div>
            <div class="gr-hero-badge">
                <div class="gr-dot"></div>
                Built for African Creators
            </div>
            <h1 class="gr-hero-h1">
                Pirates are<br><em>profiting</em> from<br>your content.
            </h1>
            <p class="gr-hero-sub">
                GhostRights finds every stolen copy of your movies,
                music, and videos — then makes pirates pay you,
                or destroys them. Automatically.
            </p>
            <div>
                <a class="gr-cta-primary" href="#">
                    Scan my content free →
                </a>
            </div>
            <div class="gr-hero-trust">
                <div class="gr-trust-avatars">
                    <div class="gr-avatar">🎬</div>
                    <div class="gr-avatar">🎵</div>
                    <div class="gr-avatar">📺</div>
                    <div class="gr-avatar">🎙️</div>
                </div>
                Trusted by Nollywood filmmakers &amp; Afrobeats artists
            </div>
        </div>
        <div>
            <div class="gr-hero-card">
                <div class="gr-hero-card-top">
                    <div class="gr-card-label">Revenue recovered this month</div>
                    <div class="gr-card-big-num">₦2.3M</div>
                    <div class="gr-card-big-sub">across all GhostRights creators</div>
                </div>
                <div class="gr-hero-card-body">
                    <div class="gr-card-stat-row">
                        <span class="gr-stat-name">Pirated copies found</span>
                        <span class="gr-stat-val">1,847</span>
                    </div>
                    <div class="gr-card-stat-row">
                        <span class="gr-stat-name">Takedowns sent</span>
                        <span class="gr-stat-val">634</span>
                    </div>
                    <div class="gr-card-stat-row">
                        <span class="gr-stat-name">Monetised copies</span>
                        <span class="gr-stat-val green">1,213</span>
                    </div>
                    <div class="gr-card-stat-row">
                        <span class="gr-stat-name">Detection rate</span>
                        <span class="gr-stat-badge">94.7%</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PLATFORMS ─────────────────────────────────────────────
    st.markdown("""
    <div class="gr-logos-bar">
        <div class="gr-logos-label">We hunt pirates on</div>
        <div class="gr-platform-pill">📺 YouTube</div>
        <div class="gr-platform-pill">📘 Facebook</div>
        <div class="gr-platform-pill">✈️ Telegram</div>
        <div class="gr-platform-pill">🎵 TikTok</div>
        <div class="gr-platform-pill">📷 Instagram</div>
        <div class="gr-platform-pill">🏴‍☠️ Torrent Sites</div>
        <div class="gr-platform-pill">📝 Blogs</div>
    </div>
    """, unsafe_allow_html=True)

    # ── HOW IT WORKS ──────────────────────────────────────────
    st.markdown("""
    <div class="gr-section">
        <div class="gr-section-label">How It Works</div>
        <h2 class="gr-section-h2">From upload to <em>paid</em> in 4 steps.</h2>
        <p class="gr-section-sub">
            GhostRights runs in the background, 24 hours a day. You create. We protect.
        </p>
        <div class="gr-steps">
            <div class="gr-step">
                <div class="gr-step-num">01</div>
                <div class="gr-step-icon">📁</div>
                <div class="gr-step-title">Upload your content</div>
                <div class="gr-step-desc">Upload your movie, song, or video. We fingerprint it instantly so our crawlers know exactly what to hunt.</div>
            </div>
            <div class="gr-step">
                <div class="gr-step-num">02</div>
                <div class="gr-step-icon">🕷️</div>
                <div class="gr-step-title">Crawlers start hunting</div>
                <div class="gr-step-desc">Our AI scans YouTube, Facebook, Telegram, TikTok, blogs and torrent sites every single hour.</div>
            </div>
            <div class="gr-step">
                <div class="gr-step-num">03</div>
                <div class="gr-step-icon">🎯</div>
                <div class="gr-step-title">Piracy detected</div>
                <div class="gr-step-desc">You get an instant alert. Choose to monetise the pirated copy or send an automated DMCA takedown.</div>
            </div>
            <div class="gr-step">
                <div class="gr-step-num">04</div>
                <div class="gr-step-icon">💰</div>
                <div class="gr-step-title">You get paid</div>
                <div class="gr-step-desc">Ad revenue from pirated copies flows to your account. Pirates pay you. Every month, automatically.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── STATS STRIP ───────────────────────────────────────────
    st.markdown("""
    <div class="gr-stats-strip">
        <div class="gr-stats-strip-inner">
            <div class="gr-big-stat">
                <div class="gr-big-stat-num">1,800+</div>
                <div class="gr-big-stat-label">Pirated copies found monthly</div>
            </div>
            <div class="gr-big-stat">
                <div class="gr-big-stat-num">₦2.3M</div>
                <div class="gr-big-stat-label">Revenue recovered</div>
            </div>
            <div class="gr-big-stat">
                <div class="gr-big-stat-num">7</div>
                <div class="gr-big-stat-label">Platforms monitored</div>
            </div>
            <div class="gr-big-stat">
                <div class="gr-big-stat-num">94.7%</div>
                <div class="gr-big-stat-label">Detection accuracy</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PRICING ───────────────────────────────────────────────
    st.markdown("""
    <div class="gr-section">
        <div class="gr-section-label">Pricing</div>
        <h2 class="gr-section-h2">Pay once. Earn <em>forever.</em></h2>
        <p class="gr-section-sub">Every plan includes a free piracy scan. No credit card required.</p>
        <div class="gr-pricing-grid">
            <div class="gr-plan">
                <div class="gr-plan-name">Starter</div>
                <div class="gr-plan-price">₦8k</div>
                <div class="gr-plan-period">per month</div>
                <ul class="gr-plan-features">
                    <li><span class="gr-check">✓</span> Up to 5 content items</li>
                    <li><span class="gr-check">✓</span> YouTube &amp; Facebook monitoring</li>
                    <li><span class="gr-check">✓</span> Email alerts</li>
                    <li><span class="gr-check">✓</span> DMCA takedowns</li>
                    <li><span class="gr-check">✓</span> Monthly report</li>
                </ul>
                <button class="gr-plan-btn">Get started →</button>
            </div>
            <div class="gr-plan featured">
                <div class="gr-plan-badge">Most Popular</div>
                <div class="gr-plan-name">Pro</div>
                <div class="gr-plan-price">₦20k</div>
                <div class="gr-plan-period">per month</div>
                <ul class="gr-plan-features">
                    <li><span class="gr-check">✓</span> Up to 25 content items</li>
                    <li><span class="gr-check">✓</span> All 7 platforms monitored</li>
                    <li><span class="gr-check">✓</span> WhatsApp + email alerts</li>
                    <li><span class="gr-check">✓</span> Ad revenue monetisation</li>
                    <li><span class="gr-check">✓</span> Watermark tracing</li>
                </ul>
                <button class="gr-plan-btn">Get Pro →</button>
            </div>
            <div class="gr-plan">
                <div class="gr-plan-name">Studio</div>
                <div class="gr-plan-price">₦75k</div>
                <div class="gr-plan-period">per month</div>
                <ul class="gr-plan-features">
                    <li><span class="gr-check">✓</span> Unlimited content items</li>
                    <li><span class="gr-check">✓</span> All platforms + dark web</li>
                    <li><span class="gr-check">✓</span> Dedicated account manager</li>
                    <li><span class="gr-check">✓</span> PDF intelligence reports</li>
                    <li><span class="gr-check">✓</span> API access</li>
                </ul>
                <button class="gr-plan-btn">Contact sales →</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── FREE SCAN ─────────────────────────────────────────────
    st.markdown("""
    <div class="gr-scan-section">
        <div class="gr-scan-inner">
            <div class="gr-section-label">Free Piracy Scan</div>
            <h2 class="gr-section-h2" style="font-size:38px;">
                See who's stealing your content <em>right now.</em>
            </h2>
            <p style="font-size:16px;color:var(--ink2);line-height:1.65;">
                No credit card. No account needed.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, form_col, _ = st.columns([1, 2, 1])
    with form_col:
        with st.container():
            st.markdown('<div class="gr-scan-form">', unsafe_allow_html=True)
            st.markdown("""
            <div style="font-family:'Figtree',sans-serif;font-size:20px;
                 font-weight:800;color:#1C1C1A;margin-bottom:24px;">
                Run your free scan
            </div>""", unsafe_allow_html=True)

            st.markdown('<span class="gr-input-label">Your name</span>',
                        unsafe_allow_html=True)
            name = st.text_input("Name", placeholder="e.g. Kunle Afolayan",
                                 label_visibility="collapsed", key="scan_name")

            st.markdown('<span class="gr-input-label">Email address</span>',
                        unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="you@email.com",
                                  label_visibility="collapsed", key="scan_email")

            st.markdown('<span class="gr-input-label">Content title</span>',
                        unsafe_allow_html=True)
            content_title = st.text_input("Content",
                placeholder="e.g. Living In Bondage, Essence",
                label_visibility="collapsed", key="scan_title")

            st.markdown('<span class="gr-input-label">Content type</span>',
                        unsafe_allow_html=True)
            content_type = st.selectbox("Type",
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
                    _show_scan_results(content_title)

            st.markdown('</div>', unsafe_allow_html=True)

    # ── FOOTER ────────────────────────────────────────────────
    st.markdown("""
    <div class="gr-footer">
        <div class="gr-footer-inner">
            <div class="gr-footer-top">
                <div>
                    <div class="gr-footer-logo">👻 GhostRights</div>
                    <div class="gr-footer-tagline">
                        AI-powered content protection for African creators.
                    </div>
                </div>
                <div>
                    <div class="gr-footer-col-title">Product</div>
                    <a class="gr-footer-link" href="#">How It Works</a>
                    <a class="gr-footer-link" href="#">Pricing</a>
                    <a class="gr-footer-link" href="#">Free Scan</a>
                </div>
                <div>
                    <div class="gr-footer-col-title">Legal</div>
                    <a class="gr-footer-link" href="#">Privacy Policy</a>
                    <a class="gr-footer-link" href="#">Terms of Service</a>
                    <a class="gr-footer-link" href="#">DMCA Policy</a>
                </div>
                <div>
                    <div class="gr-footer-col-title">Contact</div>
                    <a class="gr-footer-link" href="#">support@ghostrights.com</a>
                    <a class="gr-footer-link" href="#">WhatsApp</a>
                </div>
            </div>
            <div class="gr-footer-bottom">
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
    <div style="background:#fff;border:1px solid rgba(28,28,26,0.1);
         border-radius:16px;padding:32px;margin-top:24px;
         box-shadow:0 4px 24px rgba(28,28,26,0.08);">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;">
            <div style="width:10px;height:10px;border-radius:50%;background:#e53e3e;"></div>
            <span style="font-weight:700;font-size:15px;color:#e53e3e;">
                Piracy detected for "{title}"
            </span>
        </div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:24px;">
            <div style="text-align:center;padding:20px;background:#F5F3EE;border-radius:12px;">
                <div style="font-family:'Instrument Serif',serif;font-size:40px;color:#e53e3e;">{copies}</div>
                <div style="font-size:13px;color:#4A4A45;margin-top:4px;">Pirated copies found</div>
            </div>
            <div style="text-align:center;padding:20px;background:#F5F3EE;border-radius:12px;">
                <div style="font-family:'Instrument Serif',serif;font-size:40px;color:#1C1C1A;">{views:,}</div>
                <div style="font-size:13px;color:#4A4A45;margin-top:4px;">Stolen views</div>
            </div>
            <div style="text-align:center;padding:20px;background:#D8F3DC;border-radius:12px;">
                <div style="font-family:'Instrument Serif',serif;font-size:40px;color:#2D6A4F;">₦{revenue:,}</div>
                <div style="font-size:13px;color:#2D6A4F;margin-top:4px;">Revenue you can recover</div>
            </div>
        </div>
        <div style="font-size:13px;color:#8A8A82;text-align:center;line-height:1.6;">
            ⚠️ Sample scan. Create a free account to see real piracy data.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🛡️ Protect my content →", key="scan_cta1"):
            st.session_state.current_page = "signup"
            st.rerun()
    with c2:
        if st.button("📊 See full report", key="scan_cta2"):
            st.session_state.current_page = "signup"
            st.rerun()

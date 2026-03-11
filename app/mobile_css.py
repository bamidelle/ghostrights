"""
GhostRights — Global Mobile CSS
=================================
Import and call inject_mobile_css() at the top of every page
render() function AFTER st.markdown(KL_CSS/BASE_CSS).

Usage:
    from mobile_css import inject_mobile_css
    inject_mobile_css()
"""
import streamlit as st

MOBILE_CSS = """
<style>
/* ═══════════════════════════════════════════════════════════
   GHOSTRIGHTS — MOBILE RESPONSIVE CSS
   Breakpoints:
     ≤768px  = phone portrait
     ≤1024px = tablet / phone landscape
   ═══════════════════════════════════════════════════════════ */

/* ── SIDEBAR ──────────────────────────────────────────────── */
@media (max-width: 768px) {
    /* Sidebar collapses by default on mobile — Streamlit handles
       this natively. We just style the collapsed/open states. */
    div[data-testid="stSidebar"] {
        min-width: 240px !important;
        max-width: 280px !important;
    }
    div[data-testid="stSidebarCollapsedControl"] {
        top: 12px !important;
        left: 8px !important;
    }
    /* Sidebar nav buttons — bigger tap targets */
    div[data-testid="stSidebar"] .stButton > button {
        padding: 14px 16px !important;
        font-size: 15px !important;
        min-height: 48px !important;
    }
}

/* ── MAIN CONTENT PADDING ────────────────────────────────── */
@media (max-width: 768px) {
    .block-container {
        padding: 0 16px 32px !important;
    }
}
@media (max-width: 480px) {
    .block-container {
        padding: 0 12px 24px !important;
    }
}

/* ── TOPBAR / PAGE HEADER ────────────────────────────────── */
@media (max-width: 768px) {
    .gr-topbar {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 12px !important;
        padding: 20px 0 16px !important;
        margin-bottom: 20px !important;
    }
    .gr-topbar-left h2 {
        font-size: 22px !important;
    }
    .gr-logo-inline {
        display: none !important;
    }
    .pg-header {
        padding: 20px 0 16px !important;
        margin-bottom: 20px !important;
    }
    .pg-title {
        font-size: 22px !important;
        letter-spacing: -0.5px !important;
    }
}

/* ── STAT CARDS ──────────────────────────────────────────── */
@media (max-width: 768px) {
    .gr-stat-card {
        padding: 16px 18px !important;
        border-radius: 12px !important;
    }
    .gr-stat-value {
        font-size: 28px !important;
        letter-spacing: -0.8px !important;
    }
    .gr-stat-label {
        font-size: 10px !important;
    }
    /* Streamlit columns on mobile — stack them */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 8px !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        min-width: calc(50% - 4px) !important;
        flex: 1 1 calc(50% - 4px) !important;
    }
}
@media (max-width: 480px) {
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }
}

/* ── DETECTION / NOTIFICATION CARDS ─────────────────────── */
@media (max-width: 768px) {
    .gr-detection-item {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 10px !important;
        padding: 14px 16px !important;
    }
    .gr-badge-new, .gr-badge-ok {
        align-self: flex-start !important;
    }
    .det-card {
        padding: 14px 16px !important;
    }
    .det-title {
        font-size: 14px !important;
    }
    .det-url {
        font-size: 11px !important;
        word-break: break-all !important;
    }
    .notif-card {
        padding: 14px 16px !important;
    }
    .notif-title {
        font-size: 13px !important;
    }
}

/* ── TABS ────────────────────────────────────────────────── */
@media (max-width: 768px) {
    .stTabs [data-baseweb="tab-list"] {
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        scrollbar-width: none !important;
        gap: 2px !important;
        padding: 3px !important;
    }
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
        display: none !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 12px !important;
        padding: 6px 12px !important;
        white-space: nowrap !important;
    }
}

/* ── BUTTONS ─────────────────────────────────────────────── */
@media (max-width: 768px) {
    .stButton > button {
        font-size: 14px !important;
        padding: 12px 20px !important;
        min-height: 44px !important;
    }
    /* Full width primary CTAs on mobile */
    .stButton > button[kind="primary"] {
        width: 100% !important;
    }
}

/* ── TEXT INPUTS ─────────────────────────────────────────── */
@media (max-width: 768px) {
    .stTextInput input,
    .stSelectbox select,
    .stTextArea textarea {
        font-size: 16px !important; /* Prevents iOS zoom on focus */
        min-height: 44px !important;
    }
}

/* ── PLAN BANNER ─────────────────────────────────────────── */
@media (max-width: 768px) {
    .gr-plan-banner {
        flex-direction: column !important;
        gap: 12px !important;
        padding: 14px 16px !important;
    }
}

/* ── LANDING PAGE ────────────────────────────────────────── */
@media (max-width: 768px) {
    .kl-hero-h1 {
        font-size: 36px !important;
        letter-spacing: -1.5px !important;
    }
    .kl-hero-sub {
        font-size: 15px !important;
    }
    .kl-hero {
        padding: 48px 20px 32px !important;
    }
    .kl-feat-grid {
        grid-template-columns: 1fr !important;
    }
    .kl-pricing-grid {
        grid-template-columns: 1fr !important;
        gap: 16px !important;
    }
    .kl-nav {
        padding: 12px 16px !important;
    }
    .kl-nav-links {
        display: none !important;
    }
    .kl-stats-row {
        grid-template-columns: 1fr 1fr !important;
        gap: 12px !important;
    }
}
@media (max-width: 480px) {
    .kl-hero-h1 {
        font-size: 28px !important;
        letter-spacing: -1px !important;
    }
    .kl-stats-row {
        grid-template-columns: 1fr !important;
    }
}

/* ── FREE SCAN PAGE ──────────────────────────────────────── */
@media (max-width: 768px) {
    .fs-h1 {
        font-size: 32px !important;
        letter-spacing: -1.2px !important;
    }
    .fs-hero {
        padding: 40px 16px 24px !important;
    }
    .fs-scan-wrap {
        padding: 24px 20px !important;
        border-radius: 16px !important;
        margin: 0 0 32px !important;
    }
    .fs-stat-row {
        flex-direction: column !important;
        gap: 0 !important;
    }
    .fs-stat-item {
        border-right: none !important;
        border-bottom: 1px solid #2A2A2A !important;
        padding: 14px 0 !important;
        text-align: left !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
    }
    .fs-stat-item:last-child {
        border-bottom: none !important;
    }
    .fs-stat-num {
        font-size: 28px !important;
    }
    .fs-det-card {
        padding: 14px 16px !important;
    }
    .fs-proof-grid {
        grid-template-columns: 1fr !important;
    }
    .fs-cta-box {
        padding: 24px 20px !important;
        border-radius: 0 0 16px 16px !important;
    }
    .fs-results-header {
        padding: 20px 20px !important;
    }
    .fs-progress-wrap {
        padding: 24px 20px !important;
        border-radius: 16px !important;
    }
}

/* ── LOGIN / SIGNUP ──────────────────────────────────────── */
@media (max-width: 768px) {
    .kl-login-wrap, .kl-signup-wrap {
        padding: 20px 16px !important;
        margin: 0 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
    }
    .kl-login-h1, .kl-signup-h1 {
        font-size: 26px !important;
    }
}

/* ── REPORTS PAGE ────────────────────────────────────────── */
@media (max-width: 768px) {
    .rep-card {
        padding: 16px !important;
    }
    .rep-price {
        font-size: 32px !important;
    }
}

/* ── SETTINGS PAGE ───────────────────────────────────────── */
@media (max-width: 768px) {
    .set-plan-card {
        padding: 20px 16px !important;
    }
    .set-plan-price {
        font-size: 32px !important;
    }
}

/* ── DATAFRAMES / TABLES ─────────────────────────────────── */
@media (max-width: 768px) {
    [data-testid="stDataFrame"] {
        font-size: 12px !important;
        overflow-x: auto !important;
    }
    iframe {
        max-width: 100% !important;
    }
}

/* ── SELECTBOXES / DROPDOWNS ─────────────────────────────── */
@media (max-width: 768px) {
    [data-testid="stSelectbox"] > div {
        min-height: 44px !important;
    }
}

/* ── ALERTS / BANNERS ────────────────────────────────────── */
@media (max-width: 768px) {
    [data-testid="stAlert"] {
        padding: 12px 16px !important;
        font-size: 13px !important;
    }
}

/* ── GENERAL STREAMLIT COLUMN FIXES ─────────────────────── */
@media (max-width: 600px) {
    /* Force all multi-cols to wrap at 600px */
    section[data-testid="stSidebar"] ~ .main
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }
}

/* ── TOUCH IMPROVEMENTS ──────────────────────────────────── */
@media (hover: none) and (pointer: coarse) {
    /* Mobile touch devices */
    .stButton > button {
        min-height: 48px !important;
    }
    a, button {
        -webkit-tap-highlight-color: rgba(0,0,0,0.1) !important;
    }
}

/* ── PREVENT HORIZONTAL SCROLL ───────────────────────────── */
@media (max-width: 768px) {
    html, body {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
    .main {
        overflow-x: hidden !important;
    }
}
</style>
"""

def inject_mobile_css():
    """Call this inside every page's render() function."""
    st.markdown(MOBILE_CSS, unsafe_allow_html=True)

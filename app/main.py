# ============================================================
# GhostRights — Main App Entry Point
# ============================================================

import streamlit as st
import os
import sys

# --- Fix import paths ---
_HERE     = os.path.dirname(os.path.abspath(__file__))
_ROOT     = os.path.abspath(os.path.join(_HERE, ".."))
_PAGES    = os.path.join(_HERE, "pages")
_PAYMENTS = os.path.join(_ROOT, "payments")
_DMCA     = os.path.join(_ROOT, "dmca")
_REPORTS  = os.path.join(_ROOT, "reports")
_ALERTS   = os.path.join(_ROOT, "alerts")

for _p in [_ROOT, _HERE, _PAGES, _PAYMENTS, _DMCA, _REPORTS, _ALERTS]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# --- Page Configuration ---
st.set_page_config(
    page_title="GhostRights — Protect Your Content",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:support@ghostrights.com',
        'About': 'GhostRights — AI-powered content protection for African creators.'
    }
)

# --- Import pages ---
from pages import page_landing
from pages import page_login
from pages import page_signup
from pages import page_dashboard
from pages import page_upload_content
from pages import page_detections
from pages import page_takedowns
from pages import page_monetization
from pages import page_reports
from pages import page_settings
from pages import page_admin
from pages import page_notifications

# --- Session State ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "profile" not in st.session_state:
    st.session_state.profile = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "landing"


def router():
    page = st.session_state.current_page

    if not st.session_state.authenticated:
        if page == "login":
            page_login.render()
        elif page == "signup":
            page_signup.render()
        else:
            page_landing.render()
        return

    with st.sidebar:
        render_sidebar()

    if page == "dashboard":
        page_dashboard.render()
    elif page == "upload_content":
        page_upload_content.render()
    elif page == "detections":
        page_detections.render()
    elif page == "notifications":
        page_notifications.render()
    elif page == "takedowns":
        page_takedowns.render()
    elif page == "monetization":
        page_monetization.render()
    elif page == "reports":
        page_reports.render()
    elif page == "settings":
        page_settings.render()
    elif page == "admin" and \
            st.session_state.profile and \
            st.session_state.profile.get("is_admin"):
        page_admin.render()
    else:
        page_dashboard.render()


def render_sidebar():
    profile      = st.session_state.profile or {}
    current_page = st.session_state.get("current_page","dashboard")
    plan         = profile.get("plan","starter").title()
    name         = profile.get("full_name","Creator")
    first        = name.split()[0] if name else "Creator"

    # Unread notification count badge
    try:
        from database.db import get_unread_notifications_count
        unread = get_unread_notifications_count(
            st.session_state.user.id
            if st.session_state.get("user") else None
        )
    except Exception:
        unread = 0

    st.markdown(f"""
    <style>
    div[data-testid="stSidebar"] {{
        background: #FFFFFF !important;
        border-right: 1px solid #E8E4DE !important;
    }}
    div[data-testid="stSidebarContent"] {{
        padding: 0 !important;
        background: #FFFFFF !important;
    }}
    div[data-testid="stSidebar"] .stButton > button {{
        background: transparent !important;
        color: #6B6B6B !important;
        border: none !important;
        border-radius: 8px !important;
        text-align: left !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 14px !important;
        width: 100% !important;
        justify-content: flex-start !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: all 0.12s !important;
        letter-spacing: -0.1px !important;
    }}
    div[data-testid="stSidebar"] .stButton > button:hover {{
        background: #F0EDE8 !important;
        color: #111111 !important;
    }}
    </style>

    <div style="padding:24px 20px 16px;
         border-bottom:1px solid #E8E4DE;">
        <div style="font-family:'Plus Jakarta Sans',sans-serif;
             font-size:17px;font-weight:900;
             color:#111111;letter-spacing:-0.3px;
             margin-bottom:16px;">
            👻 GhostRights
        </div>
        <div style="background:#F0EDE8;border-radius:10px;
             padding:12px 14px;">
            <div style="font-size:13px;font-weight:800;
                 color:#111111;letter-spacing:-0.2px;">
                {first}
            </div>
            <div style="font-size:11px;font-weight:700;
                 color:#9B9B9B;margin-top:2px;
                 text-transform:uppercase;letter-spacing:0.5px;">
                {plan} Plan
            </div>
        </div>
    </div>
    <div style="padding:12px 12px 8px;
         font-size:10px;font-weight:800;
         letter-spacing:1px;text-transform:uppercase;
         color:#9B9B9B;margin-top:4px;">
        Navigation
    </div>
    """, unsafe_allow_html=True)

    notif_label = (
        f"🔔 Notifications  🔴{unread}"
        if unread > 0 else "🔔 Notifications"
    )

    nav_items = [
        ("🏠", "Dashboard",      "dashboard"),
        ("📁", "My Content",     "upload_content"),
        ("🚨", "Detections",     "detections"),
        ("⚔️",  "Takedowns",     "takedowns"),
        ("💰", "Monetization",   "monetization"),
        ("📊", "Reports",        "reports"),
        (None,  notif_label,     "notifications"),
        ("⚙️",  "Settings",      "settings"),
    ]

    for item in nav_items:
        icon, label, page_key = item
        display = f"{icon} {label}" if icon else label
        if st.button(display, key=f"nav_{page_key}",
                     use_container_width=True):
            st.session_state.current_page = page_key
            st.rerun()

    if profile.get("is_admin"):
        st.markdown("""
        <div style="padding:8px 12px 4px;
             font-size:10px;font-weight:800;
             letter-spacing:1px;text-transform:uppercase;
             color:#9B9B9B;margin-top:8px;">
            Admin
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔧 Admin Panel",
                     use_container_width=True,
                     key="nav_admin"):
            st.session_state.current_page = "admin"
            st.rerun()

    st.markdown("""
    <div style="position:fixed;bottom:0;left:0;
         width:inherit;padding:16px 12px;
         border-top:1px solid #E8E4DE;
         background:#FFFFFF;">
    """, unsafe_allow_html=True)
    if st.button("🚪 Log out", use_container_width=True,
                 key="nav_logout"):
        st.session_state.authenticated = False
        st.session_state.user    = None
        st.session_state.profile = None
        st.session_state.current_page = "landing"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


router()

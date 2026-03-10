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

for _p in [_ROOT, _HERE, _PAGES, _PAYMENTS, _DMCA]:
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
    st.markdown("## 👻 GhostRights")
    st.markdown("---")

    profile = st.session_state.profile or {}
    st.markdown(f"👤 **{profile.get('full_name', 'Creator')}**")
    st.markdown(f"📦 Plan: **{profile.get('plan', 'Starter')}**")

    st.markdown("---")
    st.markdown("### Navigation")

    nav_items = [
        ("🏠", "Dashboard",    "dashboard"),
        ("📁", "My Content",   "upload_content"),
        ("🔍", "Detections",   "detections"),
        ("⚔️",  "Takedowns",   "takedowns"),
        ("💰", "Monetization", "monetization"),
        ("📊", "Reports",      "reports"),
        ("⚙️",  "Settings",    "settings"),
    ]

    for icon, label, page_key in nav_items:
        if st.button(f"{icon} {label}",
                     key=f"nav_{page_key}",
                     use_container_width=True):
            st.session_state.current_page = page_key
            st.rerun()

    if profile.get("is_admin"):
        st.markdown("---")
        if st.button("🔧 Admin Panel",
                     use_container_width=True):
            st.session_state.current_page = "admin"
            st.rerun()

    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user  = None
        st.session_state.profile = None
        st.session_state.current_page = "landing"
        st.rerun()


router()

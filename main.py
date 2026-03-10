# ============================================================
# GhostRights — Main App Entry Point
# Run: streamlit run app/main.py
# ============================================================

import streamlit as st
import os
import sys

# Add repo root to path so all modules resolve correctly
# (Streamlit runs from app/ but database/, config/ etc are in root)
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
))

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
from pages import (
    page_landing,
    page_login,
    page_signup,
    page_dashboard,
    page_upload_content,
    page_detections,
    page_takedowns,
    page_monetization,
    page_reports,
    page_settings,
    page_admin
)

# --- Session State Initialization ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "profile" not in st.session_state:
    st.session_state.profile = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "landing"


# --- Router ---
def router():
    page = st.session_state.current_page

    # Public pages (no auth required)
    if not st.session_state.authenticated:
        if page == "login":
            page_login.render()
        elif page == "signup":
            page_signup.render()
        else:
            page_landing.render()
        return

    # Protected pages (auth required)
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
    """Render the main navigation sidebar."""
    st.markdown("## 👻 GhostRights")

    st.markdown("---")

    profile = st.session_state.profile or {}
    st.markdown(f"👤 **{profile.get('full_name', 'Creator')}**")
    st.markdown(f"📦 Plan: **{profile.get('plan', 'Starter')}**")

    st.markdown("---")
    st.markdown("### Navigation")

    nav_items = [
        ("🏠", "Dashboard",     "dashboard"),
        ("📁", "My Content",    "upload_content"),
        ("🔍", "Detections",    "detections"),
        ("⚔️",  "Takedowns",    "takedowns"),
        ("💰", "Monetization",  "monetization"),
        ("📊", "Reports",       "reports"),
        ("⚙️",  "Settings",     "settings"),
    ]

    for icon, label, page_key in nav_items:
        if st.button(
            f"{icon} {label}",
            key=f"nav_{page_key}",
            use_container_width=True
        ):
            st.session_state.current_page = page_key
            st.rerun()

    # Admin link
    if profile.get("is_admin"):
        st.markdown("---")
        if st.button("🔧 Admin Panel",
                     use_container_width=True):
            st.session_state.current_page = "admin"
            st.rerun()

    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.profile = None
        st.session_state.current_page = "landing"
        st.rerun()


# --- Run App ---
router()

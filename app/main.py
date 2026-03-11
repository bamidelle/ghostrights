# ============================================================
# GhostRights — Main App Entry Point
# ============================================================

import streamlit as st
import os
import sys

# --- Fix import paths ---
_HERE     = os.path.dirname(os.path.abspath(__file__))
_ROOT     = os.path.abspath(os.path.join(_HERE, ".."))
_PAGES    = os.path.join(_HERE, "views")
_PAYMENTS = os.path.join(_ROOT, "payments")
_DMCA     = os.path.join(_ROOT, "dmca")
_REPORTS  = os.path.join(_ROOT, "reports")
_ALERTS   = os.path.join(_ROOT, "alerts")

_DATABASE = os.path.join(_ROOT, "database")
for _p in [_ROOT, _HERE, _PAGES, _PAYMENTS, _DMCA, _REPORTS, _ALERTS, _DATABASE]:
    if _p not in sys.path:
        sys.path.insert(0, _p)


# --- Mobile CSS (inlined to avoid import issues) ---
def inject_mobile_css():
    import streamlit as _st
    _st.markdown("""
<style>
@media (max-width: 768px) {
    .block-container { padding: 0 16px 32px !important; }
    .gr-topbar { flex-direction:column !important; align-items:flex-start !important; gap:12px !important; padding:20px 0 16px !important; margin-bottom:20px !important; }
    .gr-topbar-left h2 { font-size:22px !important; }
    .gr-logo-inline { display:none !important; }
    .pg-header { padding:20px 0 16px !important; margin-bottom:20px !important; }
    .pg-title { font-size:22px !important; letter-spacing:-0.5px !important; }
    .gr-stat-card { padding:16px 18px !important; border-radius:12px !important; }
    .gr-stat-value { font-size:28px !important; letter-spacing:-0.8px !important; }
    .gr-stat-label { font-size:10px !important; }
    .gr-detection-item { flex-direction:column !important; align-items:flex-start !important; gap:10px !important; padding:14px 16px !important; }
    .det-card { padding:14px 16px !important; }
    .det-title { font-size:14px !important; }
    .det-url { font-size:11px !important; word-break:break-all !important; }
    .notif-card { padding:14px 16px !important; }
    .stButton > button { font-size:14px !important; padding:12px 20px !important; min-height:44px !important; }
    .stTextInput input, .stTextArea textarea { font-size:16px !important; min-height:44px !important; }
    .stTabs [data-baseweb="tab-list"] { flex-wrap:nowrap !important; overflow-x:auto !important; scrollbar-width:none !important; }
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display:none !important; }
    .stTabs [data-baseweb="tab"] { font-size:12px !important; padding:6px 12px !important; white-space:nowrap !important; }
    .kl-hero-h1 { font-size:32px !important; letter-spacing:-1.2px !important; }
    .kl-hero { padding:40px 16px 24px !important; }
    .kl-feat-grid { grid-template-columns:1fr !important; }
    .kl-pricing-grid { grid-template-columns:1fr !important; gap:16px !important; }
    .kl-nav-links { display:none !important; }
    .fs-h1 { font-size:28px !important; letter-spacing:-1px !important; }
    .fs-scan-wrap { padding:24px 20px !important; border-radius:16px !important; margin:0 0 32px !important; }
    .fs-stat-row { flex-direction:column !important; }
    .fs-stat-item { border-right:none !important; border-bottom:1px solid #2A2A2A !important; padding:14px 0 !important; }
    .fs-stat-item:last-child { border-bottom:none !important; }
    .fs-proof-grid { grid-template-columns:1fr !important; }
    .fs-cta-box { padding:24px 20px !important; }
    div[data-testid="stSidebar"] .stButton > button { padding:14px 16px !important; font-size:15px !important; min-height:48px !important; }
    [data-testid="stHorizontalBlock"] { flex-wrap:wrap !important; gap:8px !important; }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] { min-width:calc(50% - 4px) !important; flex:1 1 calc(50% - 4px) !important; }
    html, body { overflow-x:hidden !important; max-width:100vw !important; }
}
@media (max-width: 480px) {
    .block-container { padding: 0 12px 24px !important; }
    .kl-hero-h1 { font-size:26px !important; }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] { min-width:100% !important; flex:1 1 100% !important; }
}
</style>
""", unsafe_allow_html=True)

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
import importlib.util, os as _os

def _load(name):
    path = _os.path.join(_HERE, "views", f"{name}.py")
    if not _os.path.exists(path):
        # List what actually exists to debug
        try:
            here_ls  = _os.listdir(_HERE)
            views_path = _os.path.join(_HERE, "views")
            views_ls = _os.listdir(views_path) if _os.path.exists(views_path) else ["FOLDER NOT FOUND"]
        except Exception as ls_err:
            here_ls = [str(ls_err)]
            views_ls = []
        raise FileNotFoundError(
            f"File not found: {path}\n"
            f"_HERE contents: {here_ls}\n"
            f"views/ contents: {views_ls}"
        )
    spec = importlib.util.spec_from_file_location(name, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

page_landing       = _load("page_landing")
page_login         = _load("page_login")
page_signup        = _load("page_signup")
page_dashboard     = _load("page_dashboard")
page_upload_content= _load("page_upload_content")
page_detections    = _load("page_detections")
page_takedowns     = _load("page_takedowns")
page_monetization  = _load("page_monetization")
page_reports       = _load("page_reports")
page_settings      = _load("page_settings")
page_admin         = _load("page_admin")
page_notifications = _load("page_notifications")
page_free_scan     = _load("page_free_scan")

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
    inject_mobile_css()
    page = st.session_state.current_page

    if not st.session_state.authenticated:
        if page == "login":
            page_login.render()
        elif page == "signup":
            page_signup.render()
        elif page == "free_scan":
            page_free_scan.render()
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
    elif page == "free_scan":
        page_free_scan.render()
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

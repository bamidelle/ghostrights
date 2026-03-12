"""
GhostRights — Detections page
Lists all piracy detections with filter/sort and quick actions.
"""
import streamlit as st
from datetime import datetime
from database.db import get_supabase

KL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"] {
    background:#FFFFFF !important; color:#111111 !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
}
[data-testid="stHeader"],[data-testid="stToolbar"],
[data-testid="stDecoration"],#MainMenu,footer,header { display:none !important; }
.block-container { padding:0 32px 48px !important; max-width:100% !important; }
div[data-testid="stSidebar"] { background:#FFFFFF !important; border-right:1px solid #E8E4DE !important; }
.pg-header { padding:32px 0 24px; border-bottom:1px solid #E8E4DE; margin-bottom:32px; }
.pg-title  { font-size:28px; font-weight:900; letter-spacing:-0.8px; color:#111111; margin-bottom:4px; font-family:'Plus Jakarta Sans',sans-serif; }
.pg-sub    { font-size:14px; color:#6B6B6B; font-weight:500; }
.det-card  { background:#fff; border:1.5px solid #E8E4DE; border-radius:14px; padding:18px 22px; margin-bottom:10px; }
.det-card.new-det  { border-left:4px solid #E8463A; }
.det-card.resolved { border-left:4px solid #4ADE80; }
.det-title { font-size:15px; font-weight:800; color:#111111; letter-spacing:-0.3px; margin-bottom:4px; }
.det-meta  { font-size:12px; color:#9B9B9B; font-weight:500; }
.det-url   { font-size:12px; color:#6B6B6B; word-break:break-all; margin-top:4px; }
.chip { display:inline-block; font-size:11px; font-weight:800; padding:3px 10px; border-radius:100px; text-transform:uppercase; letter-spacing:0.5px; }
.chip-new  { background:#FEF2F2; color:#E8463A; }
.chip-dmca { background:#D8F3DC; color:#1B4332; }
.chip-mon  { background:#EDE9FE; color:#5B21B6; }
.chip-done { background:#F0EDE8; color:#6B6B6B; }
.stButton > button { border-radius:100px !important; font-family:'Plus Jakarta Sans',sans-serif !important; font-weight:800 !important; font-size:13px !important; }
.stSelectbox > div > div { background:#F0EDE8 !important; border:1.5px solid #E8E4DE !important; border-radius:10px !important; color:#111111 !important; font-family:'Plus Jakarta Sans',sans-serif !important; }
.stTabs [data-baseweb="tab-list"] { gap:4px; background:#F0EDE8; border-radius:100px; padding:4px; }
.stTabs [data-baseweb="tab"] { border-radius:100px !important; font-family:'Plus Jakarta Sans',sans-serif !important; font-weight:700 !important; font-size:14px !important; color:#6B6B6B !important; border:none !important; background:transparent !important; }
.stTabs [aria-selected="true"] { background:#111111 !important; color:#fff !important; }
</style>
"""

STATUS_CHIP = {
    "new":          '🔴 <span class="chip chip-new">New</span>',
    "confirmed":    '🔍 <span class="chip chip-new">Confirmed</span>',
    "action_taken": '⚔️ <span class="chip chip-dmca">DMCA Sent</span>',
    "monetized":    '💰 <span class="chip chip-mon">Monetized</span>',
    "taken_down":   '✅ <span class="chip chip-done">Taken Down</span>',
    "ignored":      '<span class="chip chip-done">Ignored</span>',
    "disputed":     '<span class="chip chip-done">Disputed</span>',
}
PLATFORM_ICON = {
    "youtube":"▶️", "facebook":"📘", "telegram":"✈️",
    "tiktok":"🎵", "instagram":"📷", "blog":"📝",
    "torrent":"🏴‍☠️", "other":"🌐",
}


def render():
    st.markdown(KL_CSS, unsafe_allow_html=True)

    creator_id = st.session_state.user.id \
        if st.session_state.get("user") else None

    st.markdown("""
    <div class="pg-header">
        <div class="pg-title">🚨 Detections</div>
        <div class="pg-sub">All pirated copies of your content found by GhostRights</div>
    </div>
    """, unsafe_allow_html=True)

    # Filters row
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        status_filter = st.selectbox(
            "Status", ["All", "New", "DMCA Sent", "Monetized", "Dismissed"],
            label_visibility="collapsed", key="det_status"
        )
    with col2:
        platform_filter = st.selectbox(
            "Platform",
            ["All Platforms","YouTube","Facebook",
             "Telegram","TikTok","Instagram","Blog","Other"],
            label_visibility="collapsed", key="det_platform"
        )
    with col3:
        if st.button("🔄 Refresh", key="det_refresh"):
            st.rerun()

    detections = _get_detections(creator_id,
                                  status_filter,
                                  platform_filter)

    tab_all, tab_new, tab_actioned = st.tabs([
        f"📋 All ({len(detections)})",
        f"🔴 New ({sum(1 for d in detections if d.get('status')=='new')})",
        f"✅ Actioned ({sum(1 for d in detections if d.get('status') not in ['new','confirmed',''])})",
    ])

    with tab_all:
        _render_list(detections, creator_id)
    with tab_new:
        _render_list([d for d in detections
                      if d.get("status") == "new"], creator_id)
    with tab_actioned:
        _render_list([d for d in detections
                      if d.get("status") not in
                      ["new", "", None]], creator_id)


def _render_list(detections, creator_id):
    if not detections:
        st.markdown("""
        <div style="text-align:center;padding:64px 24px;
             background:#F0EDE8;border-radius:20px;margin-top:16px;">
            <div style="font-size:48px;margin-bottom:16px;">🕵️</div>
            <div style="font-size:20px;font-weight:900;
                 color:#111111;margin-bottom:8px;
                 font-family:'Plus Jakarta Sans',sans-serif;">
                No detections here
            </div>
            <div style="font-size:14px;color:#6B6B6B;font-weight:500;">
                GhostRights will list pirated copies here as they are found.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    for det in detections:
        _render_card(det, creator_id)


def _render_card(det, creator_id):
    det_id   = det.get("id","")
    platform = det.get("platform","other").lower()
    title    = det.get("pirated_page_title") or \
               det.get("content_title","Untitled")
    url      = det.get("pirated_url","")
    views    = det.get("estimated_views", 0)
    conf     = det.get("match_confidence", 0)
    status   = det.get("status","new")
    detected = det.get("first_detected_at","")

    icon     = PLATFORM_ICON.get(platform, "🌐")
    chip_html = STATUS_CHIP.get(status, "")

    try:
        dt       = datetime.fromisoformat(detected)
        det_date = dt.strftime("%b %d, %Y")
    except Exception:
        det_date = detected[:10] if detected else ""

    card_cls = "new-det" if status in ["new","confirmed"] else \
               "resolved" if status in ["taken_down","ignored","disputed"] else ""

    st.markdown(f"""
    <div class="det-card {card_cls}">
        <div style="display:flex;justify-content:space-between;
             align-items:flex-start;margin-bottom:6px;">
            <div class="det-title">{icon} {title[:55]}</div>
            <div>{chip_html}</div>
        </div>
        <div class="det-meta">
            {platform.title()} &nbsp;·&nbsp;
            ~{views:,} views &nbsp;·&nbsp;
            {conf:.0f}% match &nbsp;·&nbsp;
            Found {det_date}
        </div>
        <div class="det-url">{url[:80]}...</div>
    </div>
    """, unsafe_allow_html=True)

    if status == "new":
        c1, c2, c3, _ = st.columns([2, 2, 2, 4])
        with c1:
            if st.button("⚔️ Send DMCA",
                         key=f"dmca_{det_id}"):
                st.session_state.current_page = "takedowns"
                st.rerun()
        with c2:
            if st.button("💰 Monetize",
                         key=f"mon_{det_id}"):
                st.session_state.current_page = "monetization"
                st.rerun()
        with c3:
            if st.button("✕ Dismiss",
                         key=f"dismiss_{det_id}"):
                _update_status(det_id, "ignored")
                st.rerun()


def _get_detections(creator_id, status_filter,
                     platform_filter):
    if not creator_id:
        return []
    try:
        q = get_supabase().table("detections") \
            .select("*") \
            .eq("creator_id", creator_id) \
            .order("first_detected_at", desc=True) \
            .limit(100)

        status_map = {
            "New":      "new",
            "DMCA Sent":"action_taken",
            "Monetized":"monetized",
            "Dismissed":"ignored",
        }
        if status_filter != "All" and \
                status_filter in status_map:
            q = q.eq("status", status_map[status_filter])

        if platform_filter != "All Platforms":
            q = q.eq("platform",
                      platform_filter.lower())

        return q.execute().data or []
    except Exception:
        return []


def _update_status(det_id, new_status):
    try:
        from database.db import get_supabase_admin
        get_supabase_admin().table("detections") \
            .update({"status": new_status}) \
            .eq("id", det_id).execute()
    except Exception as e:
        st.error(f"Update failed: {e}")

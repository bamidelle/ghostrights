import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database.db import (
    get_supabase,
    get_profile,
    get_detection_stats,
    get_content_count,
    get_unread_notifications_count
)

def render():

    # ── CSS ──────────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
    :root { --bg:#FFFFFF;--off:#F0EDE8;--ink:#111111;--grey:#6B6B6B;--grey2:#9B9B9B;--border:#E8E4DE;--green:#1B4332;--green-l:#4ADE80;--red:#E8463A; }
    html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],[data-testid="stMainBlockContainer"],.main .block-container {
        background:var(--bg) !important; font-family:'Plus Jakarta Sans',sans-serif !important; color:var(--ink) !important;
    }
    [data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],#MainMenu,footer,header { display:none !important; }
    .block-container { padding:0 32px 48px !important; max-width:100% !important; }
    div[data-testid="stSidebar"] { background:#FFFFFF !important; border-right:1px solid var(--border) !important; }
    div[data-testid="stSidebar"] .stButton > button { background:transparent !important; color:var(--grey) !important; border:none !important; border-radius:8px !important; text-align:left !important; font-weight:600 !important; font-size:14px !important; padding:10px 16px !important; width:100% !important; }
    div[data-testid="stSidebar"] .stButton > button:hover { background:var(--off) !important; color:var(--ink) !important; }
    .stButton > button { border-radius:100px !important; font-family:'Plus Jakarta Sans',sans-serif !important; font-weight:800 !important; font-size:14px !important; letter-spacing:-0.2px !important; }
    .stTabs [data-baseweb="tab-list"] { gap:4px; background:var(--off); border-radius:100px; padding:4px; }
    .stTabs [data-baseweb="tab"] { border-radius:100px !important; font-family:'Plus Jakarta Sans',sans-serif !important; font-weight:700 !important; font-size:14px !important; color:var(--grey) !important; border:none !important; background:transparent !important; }
    .stTabs [aria-selected="true"] { background:var(--ink) !important; color:#fff !important; }
    .stTextInput input { background:var(--off) !important; border:1.5px solid var(--border) !important; border-radius:10px !important; color:var(--ink) !important; font-family:'Plus Jakarta Sans',sans-serif !important; }
    .stSelectbox > div > div { background:var(--off) !important; border:1.5px solid var(--border) !important; border-radius:10px !important; color:var(--ink) !important; }
    .pg-header { padding:32px 0 24px; border-bottom:1px solid var(--border); margin-bottom:32px; }
    .pg-title { font-size:28px; font-weight:900; letter-spacing:-0.8px; color:var(--ink); margin-bottom:4px; font-family:'Plus Jakarta Sans',sans-serif; }
    .pg-sub { font-size:14px; color:var(--grey); font-weight:500; }
    .gr-topbar { padding:32px 0 24px; border-bottom:1px solid var(--border); margin-bottom:32px; display:flex; justify-content:space-between; align-items:flex-end; }
    .gr-topbar-left h2 { font-family:'Plus Jakarta Sans',sans-serif; font-size:26px; font-weight:900; margin:0; color:var(--ink); letter-spacing:-0.8px; }
    .gr-topbar-left p { font-size:14px; color:var(--grey); margin:4px 0 0; font-weight:500; }
    .gr-logo-inline { font-family:'Plus Jakarta Sans',sans-serif; font-size:18px; font-weight:900; color:var(--ink); }
    .gr-stat-card { background:var(--off); border-radius:14px; padding:22px 24px; }
    .gr-stat-card.highlight { background:var(--ink); }
    .gr-stat-card.danger { background:#FEF2F2; }
    .gr-stat-label { font-size:11px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:var(--grey2); margin-bottom:10px; }
    .gr-stat-card.highlight .gr-stat-label { color:rgba(255,255,255,0.35); }
    .gr-stat-card.danger .gr-stat-label { color:#FCA5A5; }
    .gr-stat-value { font-family:'Plus Jakarta Sans',sans-serif; font-size:40px; font-weight:900; letter-spacing:-1.5px; line-height:1; color:var(--ink); }
    .gr-stat-card.highlight .gr-stat-value { color:var(--green-l); }
    .gr-stat-card.danger .gr-stat-value { color:var(--red); }
    .gr-stat-sub { font-size:12px; color:var(--grey2); margin-top:6px; font-weight:500; }
    .gr-stat-card.highlight .gr-stat-sub { color:rgba(255,255,255,0.3); }
    .gr-detection-item { background:#fff; border:1.5px solid var(--border); border-radius:12px; padding:16px 20px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center; }
    .gr-detection-item.new { border-left:4px solid var(--red); }
    .gr-det-title { font-size:14px; font-weight:700; color:var(--ink); letter-spacing:-0.2px; }
    .gr-det-meta { font-size:12px; color:var(--grey2); margin-top:2px; font-weight:500; }
    .gr-badge-new { background:#FEF2F2; color:var(--red); font-size:11px; font-weight:800; padding:3px 10px; border-radius:100px; text-transform:uppercase; }
    .gr-badge-ok { background:var(--off); color:var(--grey); font-size:11px; font-weight:800; padding:3px 10px; border-radius:100px; text-transform:uppercase; }
    .gr-notif { background:#fff; border:1.5px solid var(--border); border-radius:12px; padding:14px 18px; margin-bottom:8px; }
    .gr-notif-title { font-size:13px; font-weight:800; color:var(--ink); letter-spacing:-0.2px; margin-bottom:2px; }
    .gr-notif-body { font-size:12px; color:var(--grey); font-weight:500; line-height:1.5; }
    .gr-action-btn { display:inline-flex; align-items:center; gap:6px; background:var(--off); color:var(--ink); border:1.5px solid var(--border); border-radius:100px; padding:10px 18px; font-size:13px; font-weight:700; cursor:pointer; text-decoration:none; }

    /* ── MOBILE ── */
    @media (max-width: 768px) {
        .block-container { padding: 0 12px 24px !important; }
        .gr-topbar { flex-direction:column !important; align-items:flex-start !important; gap:8px !important; padding:16px 0 12px !important; margin-bottom:16px !important; }
        .gr-topbar-left h2 { font-size:20px !important; }
        .gr-logo-inline { display:none !important; }
        .gr-stat-card { padding:14px 16px !important; }
        .gr-stat-value { font-size:26px !important; }
        .gr-stat-label { font-size:10px !important; }
        .gr-detection-item { flex-direction:column !important; align-items:flex-start !important; gap:8px !important; padding:12px 14px !important; }
        .gr-badge-new, .gr-badge-ok { align-self:flex-start !important; }
    }
    </style>
    """, unsafe_allow_html=True)

    # ── GET DATA ─────────────────────────────────────────────
    profile = st.session_state.get("profile", {})
    creator_id = st.session_state.user.id \
        if st.session_state.get("user") else None

    name = profile.get("full_name", "Creator")
    first_name = name.split()[0] if name else "Creator"

    # Fetch real stats
    stats = get_detection_stats(creator_id) if creator_id else {}
    content_count = get_content_count(creator_id) if creator_id else 0
    notif_count = get_unread_notifications_count(creator_id) \
        if creator_id else 0

    # Fetch recent detections
    recent_detections = _get_recent_detections(creator_id)
    recent_content = _get_recent_content(creator_id)
    platform_stats = _get_platform_stats(creator_id)
    revenue_this_month = _get_monthly_revenue(creator_id)

    # ── TOP BAR ───────────────────────────────────────────────
    hour = datetime.now().hour
    greeting = "Good morning" if hour < 12 \
        else "Good afternoon" if hour < 17 \
        else "Good evening"

    st.markdown(f"""
    <div class="gr-topbar">
        <div class="gr-topbar-left">
            <h2>{greeting}, {first_name} 👋</h2>
            <p>Here's what GhostRights caught while you were away</p>
        </div>
        <div class="gr-logo-inline">👻 GhostRights</div>
    </div>
    """, unsafe_allow_html=True)

    # ── PLAN BANNER ───────────────────────────────────────────
    plan_name = profile.get("plan", "Starter")
    st.markdown(f"""
    <div class="gr-plan-banner">
        <div class="gr-plan-banner-left">
            You are on the <strong>{plan_name} Plan</strong> —
            upgrade to unlock unlimited scans,
            monetization & WhatsApp alerts
        </div>
        <button class="gr-upgrade-btn">⬆ Upgrade Plan</button>
    </div>
    """, unsafe_allow_html=True)

    # ── STAT CARDS ────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(f"""
        <div class="gr-stat-card danger">
            <div class="gr-stat-icon">🔴</div>
            <div class="gr-stat-label">New Detections</div>
            <div class="gr-stat-value">
                {stats.get('new', 0)}
            </div>
            <div class="gr-stat-sub">Needs your attention</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="gr-stat-card highlight">
            <div class="gr-stat-icon">💰</div>
            <div class="gr-stat-label">Revenue Recovered</div>
            <div class="gr-stat-value">
                ₦{revenue_this_month:,}
            </div>
            <div class="gr-stat-sub">This month</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="gr-stat-card">
            <div class="gr-stat-icon">📁</div>
            <div class="gr-stat-label">Protected Content</div>
            <div class="gr-stat-value">{content_count}</div>
            <div class="gr-stat-sub">Items registered</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="gr-stat-card">
            <div class="gr-stat-icon">⚔️</div>
            <div class="gr-stat-label">Taken Down</div>
            <div class="gr-stat-value">
                {stats.get('taken_down', 0)}
            </div>
            <div class="gr-stat-sub">Copies destroyed</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="gr-stat-card">
            <div class="gr-stat-icon">🔔</div>
            <div class="gr-stat-label">Notifications</div>
            <div class="gr-stat-value">{notif_count}</div>
            <div class="gr-stat-sub">Unread alerts</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 32px;'></div>",
                unsafe_allow_html=True)

    # ── MAIN CONTENT — 2 COLUMNS ──────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:

        # Recent Detections Feed
        st.markdown("""
        <div class="gr-section-title">
            🔴 Live Detection Feed
            <span>Latest piracy found</span>
        </div>
        """, unsafe_allow_html=True)

        if recent_detections:
            for d in recent_detections:
                status = d.get("status", "new")
                badge_class = "gr-badge-new"
                badge_text = "NEW"
                item_class = "new-item"

                if status == "monetized":
                    badge_class = "gr-badge-monetized"
                    badge_text = "MONETIZED"
                    item_class = "monetized"
                elif status == "taken_down":
                    badge_class = "gr-badge-takendown"
                    badge_text = "TAKEN DOWN"
                    item_class = "taken-down"

                platform = d.get("platform", "unknown").title()
                content_title = d.get(
                    "protected_content", {}
                ).get("title", "Unknown Content") \
                    if isinstance(d.get("protected_content"), dict) \
                    else "Content"
                views = d.get("estimated_views", 0)
                detected = d.get("first_detected_at", "")[:10] \
                    if d.get("first_detected_at") else "Recently"

                st.markdown(f"""
                <div class="gr-detection-item {item_class}">
                    <div>
                        <div class="gr-detection-title">
                            "{content_title}" found on {platform}
                        </div>
                        <div class="gr-detection-meta">
                            ~{views:,} views • Detected {detected}
                        </div>
                    </div>
                    <span class="{badge_class}">{badge_text}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Empty state
            st.markdown("""
            <div style="text-align:center; padding: 48px 24px;
                 background: rgba(255,255,255,0.02);
                 border: 1px dashed rgba(255,255,255,0.08);
                 border-radius: 16px;">
                <div style="font-size: 40px; margin-bottom: 16px;">
                    👻
                </div>
                <div style="font-family:'Syne',sans-serif;
                     font-size:16px; font-weight:700;
                     margin-bottom:8px;">
                    No piracy detected yet
                </div>
                <div style="font-size:13px;
                     color:rgba(240,237,230,0.35);">
                    Upload your content and our crawlers
                    will start hunting immediately
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top:16px;'></div>",
                        unsafe_allow_html=True)
            if st.button("📁 Upload My First Content",
                         key="upload_cta"):
                st.session_state.current_page = "upload_content"
                st.rerun()

        st.markdown("<div style='margin-top: 28px;'></div>",
                    unsafe_allow_html=True)

        # Protected Content List
        st.markdown("""
        <div class="gr-section-title">
            📁 Your Protected Content
            <span>Most pirated first</span>
        </div>
        """, unsafe_allow_html=True)

        if recent_content:
            for c in recent_content:
                title = c.get("title", "Untitled")
                ctype = c.get("content_type", "other").replace("_", " ").title()
                copies = c.get("total_pirated_copies_found", 0)
                revenue = c.get("total_revenue_recovered_ngn", 0)
                fp = "✅" if c.get("fingerprint_generated") else "⏳"

                st.markdown(f"""
                <div class="gr-content-item">
                    <div>
                        <div class="gr-content-title">{title}</div>
                        <div class="gr-content-meta">
                            {ctype} • Fingerprint {fp}
                        </div>
                    </div>
                    <div class="gr-content-stat">
                        <div class="gr-content-stat-num">
                            {copies}
                        </div>
                        <div class="gr-content-stat-label">
                            pirated copies
                        </div>
                        <div style="font-size:11px;
                             color:rgba(200,255,0,0.6);
                             margin-top:2px;">
                            ₦{revenue:,} recovered
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="font-size:13px;
                 color:rgba(240,237,230,0.3);
                 text-align:center; padding: 32px;">
                No content uploaded yet
            </div>
            """, unsafe_allow_html=True)

    with col_right:

        # Platform Breakdown
        st.markdown("""
        <div class="gr-section-title">
            🌍 Piracy By Platform
            <span>Where pirates strike most</span>
        </div>
        """, unsafe_allow_html=True)

        if platform_stats:
            total = sum(p["count"] for p in platform_stats) or 1
            platform_icons = {
                "facebook": "📘", "youtube": "📺",
                "telegram": "✈️", "tiktok": "🎵",
                "instagram": "📷", "twitter": "🐦",
                "blog": "📝", "torrent": "🏴‍☠️",
                "other": "🌐"
            }
            for p in platform_stats:
                pct = int((p["count"] / total) * 100)
                icon = platform_icons.get(p["platform"], "🌐")
                st.markdown(f"""
                <div class="gr-platform-row">
                    <div class="gr-platform-name">
                        {icon} {p['platform'].title()}
                    </div>
                    <div class="gr-platform-bar-bg">
                        <div class="gr-platform-bar-fill"
                             style="width:{pct}%">
                        </div>
                    </div>
                    <div class="gr-platform-count">
                        {p['count']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="font-size:13px;
                 color:rgba(240,237,230,0.3);
                 padding: 24px 0;">
                Platform data will appear once crawlers
                start finding piracy.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:28px;'></div>",
                    unsafe_allow_html=True)

        # Notifications
        st.markdown(f"""
        <div class="gr-section-title">
            🔔 Recent Alerts
            <span>{notif_count} unread</span>
        </div>
        """, unsafe_allow_html=True)

        notifications = _get_recent_notifications(creator_id)

        if notifications:
            notif_icons = {
                "new_detection": "🔴",
                "takedown_success": "✅",
                "claim_active": "💰",
                "revenue_earned": "💰",
                "subscription_renewal": "🔄",
                "report_ready": "📊",
                "system_alert": "⚠️"
            }
            for n in notifications[:5]:
                icon = notif_icons.get(
                    n.get("notification_type", ""), "🔔"
                )
                created = n.get("created_at", "")[:10] \
                    if n.get("created_at") else ""
                st.markdown(f"""
                <div class="gr-notif-item">
                    <div class="gr-notif-icon">{icon}</div>
                    <div>
                        <div class="gr-notif-text">
                            {n.get('message', '')}
                        </div>
                        <div class="gr-notif-time">{created}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="font-size:13px;
                 color:rgba(240,237,230,0.3);
                 padding: 24px 0;">
                🔔 No alerts yet — we'll notify you
                the moment piracy is detected.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:28px;'></div>",
                    unsafe_allow_html=True)

        # Quick Actions
        st.markdown("""
        <div class="gr-section-title">
            ⚡ Quick Actions
        </div>
        """, unsafe_allow_html=True)

        if st.button("📁 Upload New Content", key="qa_upload",
                     use_container_width=True):
            st.session_state.current_page = "upload_content"
            st.rerun()

        if st.button("🔍 View All Detections", key="qa_detect",
                     use_container_width=True):
            st.session_state.current_page = "detections"
            st.rerun()

        if st.button("⚔️ Manage Takedowns", key="qa_takedown",
                     use_container_width=True):
            st.session_state.current_page = "takedowns"
            st.rerun()

        if st.button("📊 Buy Intelligence Report", key="qa_report",
                     use_container_width=True):
            st.session_state.current_page = "reports"
            st.rerun()

        if st.button("💰 View Monetization", key="qa_money",
                     use_container_width=True):
            st.session_state.current_page = "monetization"
            st.rerun()


# ── DATA HELPERS ─────────────────────────────────────────────

def _get_recent_detections(creator_id: str) -> list:
    """Fetch 5 most recent detections."""
    if not creator_id:
        return []
    try:
        supabase = get_supabase()
        response = supabase.table("detections") \
            .select("*, protected_content(title)") \
            .eq("creator_id", creator_id) \
            .order("first_detected_at", desc=True) \
            .limit(5) \
            .execute()
        return response.data or []
    except Exception:
        return []


def _get_recent_content(creator_id: str) -> list:
    """Fetch protected content sorted by most pirated."""
    if not creator_id:
        return []
    try:
        supabase = get_supabase()
        response = supabase.table("protected_content") \
            .select("*") \
            .eq("creator_id", creator_id) \
            .eq("is_active", True) \
            .order("total_pirated_copies_found", desc=True) \
            .limit(5) \
            .execute()
        return response.data or []
    except Exception:
        return []


def _get_platform_stats(creator_id: str) -> list:
    """Get piracy count by platform."""
    if not creator_id:
        return []
    try:
        supabase = get_supabase()
        response = supabase.table("detections") \
            .select("platform") \
            .eq("creator_id", creator_id) \
            .execute()

        if not response.data:
            return []

        counts = {}
        for row in response.data:
            p = row.get("platform", "other")
            counts[p] = counts.get(p, 0) + 1

        return sorted(
            [{"platform": k, "count": v} for k, v in counts.items()],
            key=lambda x: x["count"], reverse=True
        )
    except Exception:
        return []


def _get_monthly_revenue(creator_id: str) -> int:
    """Get total estimated revenue lost this month from detections.
    Uses estimated_revenue_lost_ngn since monetization_claims
    is populated only when YouTube Content ID is live."""
    if not creator_id:
        return 0
    try:
        supabase = get_supabase()
        first_of_month = datetime.now().replace(
            day=1, hour=0, minute=0, second=0
        ).isoformat()
        response = supabase.table("detections") \
            .select("estimated_revenue_lost_ngn") \
            .eq("creator_id", creator_id) \
            .execute()

        if not response.data:
            return 0
        return sum(
            r.get("estimated_revenue_lost_ngn", 0) or 0 for r in response.data
        )
    except Exception:
        return 0


def _get_recent_notifications(creator_id: str) -> list:
    """Fetch 5 most recent notifications."""
    if not creator_id:
        return []
    try:
        supabase = get_supabase()
        response = supabase.table("notifications") \
            .select("*") \
            .eq("creator_id", creator_id) \
            .order("created_at", desc=True) \
            .limit(5) \
            .execute()
        return response.data or []
    except Exception:
        return []

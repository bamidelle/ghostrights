import streamlit as st
from database.db import get_supabase, get_supabase_admin


def render():

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        background: #FFFFFF !important; color: #1A1A1A !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { padding: 0 32px 48px !important; max-width: 100% !important; }
    .td-header { padding: 32px 0 28px; border-bottom: 1px solid #E8E4DE; margin-bottom: 32px; }
    .td-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 28px; font-weight: 900; letter-spacing: -0.8px; color: #111111; margin-bottom: 4px; }
    .td-sub { font-size: 14px; color: #6B6B6B; font-weight: 500; }
    .td-stats { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 32px; }
    .td-stat { background: #F0EDE8; border-radius: 14px; padding: 22px 24px; }
    .td-stat.dark { background: #111111; }
    .td-stat.red  { background: #FEF2F2; }
    .td-stat-label { font-size: 11px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; color: #9B9B9B; margin-bottom: 10px; }
    .td-stat.dark .td-stat-label { color: rgba(255,255,255,0.35); }
    .td-stat.red  .td-stat-label { color: #FCA5A5; }
    .td-stat-num { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 40px; font-weight: 900; letter-spacing: -1.5px; line-height: 1; color: #111111; }
    .td-stat.dark .td-stat-num { color: #4ADE80; }
    .td-stat.red  .td-stat-num { color: #E8463A; }
    .td-stat-sub { font-size: 12px; color: #9B9B9B; margin-top: 6px; font-weight: 500; }
    .td-stat.dark .td-stat-sub { color: rgba(255,255,255,0.3); }
    .td-card { background: #FFFFFF; border: 1.5px solid #E8E4DE; border-radius: 16px; padding: 22px 24px; margin-bottom: 12px; }
    .td-card.new-det { border-left: 4px solid #E8463A; }
    .td-card.sent    { border-left: 4px solid #9B9B9B; }
    .td-card-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
    .td-card-title { font-size: 15px; font-weight: 800; color: #111111; letter-spacing: -0.3px; margin-bottom: 4px; }
    .td-card-meta  { font-size: 13px; color: #6B6B6B; font-weight: 500; }
    .td-card-url   { font-size: 12px; color: #9B9B9B; word-break: break-all; margin-top: 4px; }
    .td-badge-new  { background: #FEF2F2; color: #E8463A; font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 100px; text-transform: uppercase; }
    .td-badge-sent { background: #F0EDE8; color: #6B6B6B; font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 100px; text-transform: uppercase; }
    .td-badge-mon  { background: #F0FDF4; color: #16A34A; font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 100px; text-transform: uppercase; }
    .td-card-stats { display: flex; gap: 20px; font-size: 13px; color: #9B9B9B; font-weight: 500; }
    .td-card-stat-val { color: #111111; font-weight: 700; }
    .td-dmca-preview { background: #F0EDE8; border-radius: 12px; padding: 20px 24px; margin-top: 16px; font-size: 12px; color: #4A4A45; line-height: 1.7; font-family: monospace; white-space: pre-wrap; max-height: 300px; overflow-y: auto; }
    .stButton > button { border-radius: 100px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 800 !important; font-size: 13px !important; letter-spacing: -0.2px !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; background: #F0EDE8; border-radius: 100px; padding: 4px; }
    .stTabs [data-baseweb="tab"] { border-radius: 100px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 700 !important; font-size: 14px !important; color: #6B6B6B !important; border: none !important; background: transparent !important; }
    .stTabs [aria-selected="true"] { background: #111111 !important; color: #fff !important; }
    div[data-testid="stSidebar"] { background: #FFFFFF !important; border-right: 1px solid #E8E4DE !important; }
    </style>
    """, unsafe_allow_html=True)

    creator_id = st.session_state.user.id if st.session_state.get("user") else None

    st.markdown('<div class="td-header"><div class="td-title">⚔️ Takedowns</div><div class="td-sub">Send DMCA notices and destroy pirated copies of your content</div></div>', unsafe_allow_html=True)

    detections = _get_detections(creator_id)
    takedowns  = _get_takedowns(creator_id)
    new_count  = sum(1 for d in detections if d.get("status") == "new")
    total_views = sum(d.get("estimated_views", 0) for d in detections)

    st.markdown(f"""
    <div class="td-stats">
        <div class="td-stat red"><div class="td-stat-label">Needs Action</div><div class="td-stat-num">{new_count}</div><div class="td-stat-sub">New detections</div></div>
        <div class="td-stat dark"><div class="td-stat-label">Notices Sent</div><div class="td-stat-num">{len(takedowns)}</div><div class="td-stat-sub">DMCA sent</div></div>
        <div class="td-stat"><div class="td-stat-label">Success Rate</div><div class="td-stat-num">87%</div><div class="td-stat-sub">Removed within 72hrs</div></div>
        <div class="td-stat"><div class="td-stat-label">Stolen Views</div><div class="td-stat-num">{total_views//1000 if total_views >= 1000 else total_views}{"K" if total_views >= 1000 else ""}</div><div class="td-stat-sub">Across all detections</div></div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([f"🔴 New ({new_count})", f"📋 All ({len(detections)})", f"✅ Sent ({len(takedowns)})"])

    with tab1:
        new_dets = [d for d in detections if d.get("status") == "new"]
        if not new_dets:
            _empty_state("🎉", "All clear!", "No new piracy detections right now.")
        else:
            for det in new_dets:
                _render_card(det, creator_id)

    with tab2:
        if not detections:
            _empty_state("👻", "No detections yet", "Upload content and our crawlers will start hunting.")
        else:
            for det in detections:
                _render_card(det, creator_id)

    with tab3:
        if not takedowns:
            _empty_state("📋", "No notices sent yet", "Send your first DMCA notice from the New tab.")
        else:
            for td in takedowns:
                _render_takedown(td)


def _render_card(det, creator_id):
    platform = det.get("platform", "other")
    title    = det.get("pirated_page_title", "Unknown page")
    url      = det.get("pirated_url", "")
    views    = det.get("estimated_views", 0)
    conf     = det.get("match_confidence", 0)
    status   = det.get("status", "new")
    det_id   = det.get("id", "")
    detected = det.get("first_detected_at", "")[:10] if det.get("first_detected_at") else ""
    icons    = {"youtube":"📺","facebook":"📘","telegram":"✈️","tiktok":"🎵","instagram":"📷","blog":"📝","torrent":"🏴‍☠️"}
    icon     = icons.get(platform, "🌐")
    badge    = {"new":'<span class="td-badge-new">New</span>',"takedown_requested":'<span class="td-badge-sent">DMCA Sent</span>',"monetized":'<span class="td-badge-mon">Monetized</span>'}.get(status, f'<span class="td-badge-sent">{status}</span>')
    card_cls = "new-det" if status == "new" else "sent"

    st.markdown(f"""
    <div class="td-card {card_cls}">
        <div class="td-card-top">
            <div>
                <div class="td-card-title">{icon} {platform.title()} — {title[:60]}{"..." if len(title)>60 else ""}</div>
                <div class="td-card-meta">Detected {detected}</div>
                <div class="td-card-url">{url[:80]}{"..." if len(url)>80 else ""}</div>
            </div>
            {badge}
        </div>
        <div class="td-card-stats">
            <div>Views: <span class="td-card-stat-val">{views:,}</span></div>
            <div>Confidence: <span class="td-card-stat-val">{conf:.0f}%</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if status == "new":
        c1, c2, c3 = st.columns([2, 2, 6])
        with c1:
            if st.button("⚔️ Send DMCA", key=f"dmca_{det_id}"):
                _send_dmca(det_id)
        with c2:
            if st.button("💰 Monetize", key=f"mon_{det_id}"):
                _monetize(det_id)
        with c3:
            if st.button("👁 Dismiss", key=f"dis_{det_id}"):
                _dismiss(det_id)
        st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)


def _render_takedown(td):
    ref     = td.get("dmca_reference", "")
    platform = td.get("platform", "").title()
    sent_at  = td.get("sent_at", "")[:10] if td.get("sent_at") else ""
    notice   = td.get("notice_body", "")
    with st.expander(f"📋 {ref} — {platform} — {sent_at}"):
        st.markdown(f"**URL:** {td.get('infringing_url','')}")
        st.markdown(f"**Sent to:** {td.get('sent_to_email','')}")
        st.markdown(f"**Status:** {td.get('status','').upper()}")
        if notice:
            st.markdown(f'<div class="td-dmca-preview">{notice[:1000]}...</div>', unsafe_allow_html=True)


def _send_dmca(detection_id):
    with st.spinner("Sending DMCA notice..."):
        try:
            from dmca.dmca_engine import DMCAEngine
            result = DMCAEngine().process_takedown(detection_id)
            if result.get("success"):
                st.success(f"✅ DMCA notice sent! Ref: {result.get('reference_id','')}")
                st.rerun()
            else:
                st.error(f"Failed: {result.get('error','')}")
        except Exception as e:
            st.error(f"Error: {e}")

def _monetize(detection_id):
    try:
        get_supabase_admin().table("detections").update({"status":"monetized"}).eq("id",detection_id).execute()
        st.success("💰 Marked for monetization!")
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")

def _dismiss(detection_id):
    try:
        get_supabase_admin().table("detections").update({"status":"dismissed"}).eq("id",detection_id).execute()
        st.info("Detection dismissed.")
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")

def _get_detections(creator_id):
    if not creator_id: return []
    try:
        return get_supabase().table("detections").select("*").eq("creator_id",creator_id).order("first_detected_at",desc=True).limit(50).execute().data or []
    except: return []

def _get_takedowns(creator_id):
    if not creator_id: return []
    try:
        return get_supabase().table("takedowns").select("*").eq("creator_id",creator_id).order("sent_at",desc=True).limit(50).execute().data or []
    except: return []

def _empty_state(icon, title, subtitle):
    st.markdown(f'<div style="text-align:center;padding:64px 24px;background:#F0EDE8;border-radius:20px;margin-top:16px;"><div style="font-size:48px;margin-bottom:16px;">{icon}</div><div style="font-family:Plus Jakarta Sans,sans-serif;font-size:20px;font-weight:900;color:#111111;margin-bottom:8px;">{title}</div><div style="font-size:14px;color:#6B6B6B;">{subtitle}</div></div>', unsafe_allow_html=True)

"""
GhostRights — Notifications & Alert Settings page
Handles: in-app notification feed + alert preferences
"""
import streamlit as st
from datetime import datetime
from database.db import get_supabase, get_supabase_admin


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

/* NOTIF CARD */
.notif-card {
    background:#fff; border:1.5px solid #E8E4DE;
    border-radius:14px; padding:18px 22px;
    margin-bottom:10px; display:flex;
    gap:16px; align-items:flex-start;
    transition: box-shadow 0.15s;
}
.notif-card:hover { box-shadow:0 4px 16px rgba(0,0,0,0.06); }
.notif-card.unread { border-left:4px solid #E8463A; background:#FFFCFC; }
.notif-card.new_detection      { border-left-color:#E8463A; }
.notif-card.takedown_success    { border-left-color:#1B4332; }
.notif-card.takedown_failed     { border-left-color:#E8463A; }
.notif-card.claim_active        { border-left-color:#4ADE80; }
.notif-card.revenue_earned      { border-left-color:#4ADE80; }
.notif-card.subscription_renewal { border-left-color:#4ADE80; }
.notif-card.report_ready        { border-left-color:#6B6B6B; }
.notif-card.system_alert        { border-left-color:#9B9B9B; }

.notif-icon { font-size:24px; flex-shrink:0; margin-top:2px; }
.notif-title { font-size:14px; font-weight:800; color:#111111; letter-spacing:-0.2px; margin-bottom:3px; }
.notif-body  { font-size:13px; color:#6B6B6B; font-weight:500; line-height:1.55; }
.notif-time  { font-size:11px; color:#9B9B9B; font-weight:600; margin-top:6px; }

.notif-badge-new { background:#FEF2F2; color:#E8463A; font-size:10px; font-weight:800; padding:2px 8px; border-radius:100px; text-transform:uppercase; letter-spacing:0.5px; }

/* TOGGLE SWITCH */
.toggle-row {
    display:flex; justify-content:space-between;
    align-items:center; padding:16px 0;
    border-bottom:1px solid #E8E4DE;
}
.toggle-row:last-child { border-bottom:none; }
.toggle-label { font-size:14px; font-weight:700; color:#111111; letter-spacing:-0.2px; }
.toggle-desc  { font-size:12px; color:#9B9B9B; font-weight:500; margin-top:2px; }

/* PREF CARD */
.pref-card { background:#F0EDE8; border-radius:16px; padding:24px 28px; margin-bottom:16px; }
.pref-title { font-size:16px; font-weight:900; color:#111111; letter-spacing:-0.3px; margin-bottom:4px; }
.pref-sub   { font-size:13px; color:#6B6B6B; font-weight:500; margin-bottom:20px; }

/* STATUS CHIPS */
.chip-ok  { background:#D8F3DC; color:#1B4332; font-size:11px; font-weight:800; padding:4px 12px; border-radius:100px; }
.chip-off { background:#F0EDE8; color:#9B9B9B; font-size:11px; font-weight:800; padding:4px 12px; border-radius:100px; }
.chip-err { background:#FEF2F2; color:#E8463A; font-size:11px; font-weight:800; padding:4px 12px; border-radius:100px; }

/* Streamlit overrides */
.stButton > button { border-radius:100px !important; font-family:'Plus Jakarta Sans',sans-serif !important; font-weight:800 !important; font-size:13px !important; }
.stTabs [data-baseweb="tab-list"] { gap:4px; background:#F0EDE8; border-radius:100px; padding:4px; }
.stTabs [data-baseweb="tab"] { border-radius:100px !important; font-family:'Plus Jakarta Sans',sans-serif !important; font-weight:700 !important; font-size:14px !important; color:#6B6B6B !important; border:none !important; background:transparent !important; }
.stTabs [aria-selected="true"] { background:#111111 !important; color:#fff !important; }
.stCheckbox label { font-family:'Plus Jakarta Sans',sans-serif !important; font-weight:600 !important; font-size:14px !important; }
.stTextInput input { background:#fff !important; border:1.5px solid #E8E4DE !important; border-radius:10px !important; color:#111111 !important; font-family:'Plus Jakarta Sans',sans-serif !important; font-size:15px !important; }
</style>
"""

NOTIF_ICONS = {
    "new_detection":        "🚨",
    "takedown_success":     "⚔️",
    "takedown_failed":      "❌",
    "claim_active":         "💰",
    "revenue_earned":       "💰",
    "subscription_renewal": "✅",
    "subscription_expiring":"⚠️",
    "report_ready":         "📊",
    "system_alert":         "🛡",
    "default":              "🔔",
}


def render():
    st.markdown(KL_CSS, unsafe_allow_html=True)

    creator_id   = st.session_state.user.id \
        if st.session_state.get("user") else None
    profile      = st.session_state.get("profile", {})
    creator_name = profile.get("full_name", "Creator")
    email        = profile.get("email","") or \
        (st.session_state.user.email
         if st.session_state.get("user") else "")
    phone        = profile.get("phone","")

    st.markdown("""
    <div class="pg-header">
        <div class="pg-title">🔔 Notifications</div>
        <div class="pg-sub">
            Stay on top of piracy alerts and activity
        </div>
    </div>
    """, unsafe_allow_html=True)

    notifications = _get_notifications(creator_id)
    unread = sum(1 for n in notifications if not n.get("is_read"))

    tab1, tab2, tab3 = st.tabs([
        f"🔔 Inbox ({len(notifications)})",
        "📱 Alert Settings",
        "🧪 Test Alerts",
    ])

    # ════ TAB 1 — INBOX ════
    with tab1:
        col_a, col_b = st.columns([6, 1])
        with col_a:
            if unread > 0:
                st.markdown(f"""
                <div style="background:#FEF2F2;border-radius:10px;
                     padding:12px 18px;margin-bottom:20px;
                     display:flex;align-items:center;gap:10px;">
                    <span style="font-size:18px;">🔴</span>
                    <span style="font-size:14px;font-weight:700;
                          color:#E8463A;">
                        {unread} unread notification
                        {"s" if unread > 1 else ""}
                    </span>
                </div>
                """, unsafe_allow_html=True)
        with col_b:
            if notifications and st.button(
                "Mark all read", key="mark_all"
            ):
                _mark_all_read(creator_id)
                st.rerun()

        if not notifications:
            _empty(
                "🔔", "All quiet",
                "Notifications will appear here when GhostRights "
                "detects piracy or takes action."
            )
        else:
            for notif in notifications:
                _render_notif(notif, creator_id)

    # ════ TAB 2 — ALERT SETTINGS ════
    with tab2:
        prefs = _get_prefs(creator_id)

        st.markdown("""
        <div style="margin-bottom:24px;">
        </div>
        """, unsafe_allow_html=True)

        # WhatsApp section
        st.markdown(f"""
        <div class="pref-card">
            <div class="pref-title">📱 WhatsApp Alerts</div>
            <div class="pref-sub">
                Instant alerts sent to your WhatsApp number.
                Current number:
                <strong>{phone or "Not set — add in Settings"}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        wa_piracy  = st.checkbox(
            "🚨 New piracy detected",
            value=prefs.get("wa_piracy", True),
            key="wa_piracy"
        )
        wa_dmca    = st.checkbox(
            "⚔️ DMCA notice sent",
            value=prefs.get("wa_dmca", True),
            key="wa_dmca"
        )
        wa_payment = st.checkbox(
            "💳 Payment confirmed",
            value=prefs.get("wa_payment", True),
            key="wa_payment"
        )
        wa_digest  = st.checkbox(
            "📊 Weekly digest (every Monday)",
            value=prefs.get("wa_digest", True),
            key="wa_digest"
        )

        st.markdown("<div style='margin-top:24px;'></div>",
                    unsafe_allow_html=True)

        # Email section
        st.markdown(f"""
        <div class="pref-card">
            <div class="pref-title">📧 Email Alerts</div>
            <div class="pref-sub">
                Alerts sent to:
                <strong>{email or "No email found"}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        em_piracy  = st.checkbox(
            "🚨 New piracy detected",
            value=prefs.get("em_piracy", True),
            key="em_piracy"
        )
        em_dmca    = st.checkbox(
            "⚔️ DMCA notice sent",
            value=prefs.get("em_dmca", True),
            key="em_dmca"
        )
        em_payment = st.checkbox(
            "💳 Payment confirmed",
            value=prefs.get("em_payment", True),
            key="em_payment"
        )
        em_digest  = st.checkbox(
            "📊 Weekly digest (every Monday)",
            value=prefs.get("em_digest", True),
            key="em_digest"
        )

        st.markdown("<div style='margin-top:28px;'></div>",
                    unsafe_allow_html=True)

        if st.button("💾 Save Alert Preferences",
                     key="save_prefs"):
            new_prefs = {
                "wa_piracy":  wa_piracy,
                "wa_dmca":    wa_dmca,
                "wa_payment": wa_payment,
                "wa_digest":  wa_digest,
                "em_piracy":  em_piracy,
                "em_dmca":    em_dmca,
                "em_payment": em_payment,
                "em_digest":  em_digest,
                # Map to engine format
                "whatsapp_alerts": wa_piracy or wa_dmca,
                "email_alerts":    em_piracy or em_dmca,
                "whatsapp_digest": wa_digest,
                "email_digest":    em_digest,
            }
            _save_prefs(creator_id, new_prefs)
            st.success("✅ Alert preferences saved!")

    # ════ TAB 3 — TEST ALERTS ════
    with tab3:
        st.markdown("""
        <div style="background:#F0EDE8;border-radius:16px;
             padding:28px 32px;margin-bottom:24px;">
            <div style="font-size:18px;font-weight:900;
                 color:#111111;letter-spacing:-0.5px;
                 margin-bottom:8px;
                 font-family:'Plus Jakarta Sans',sans-serif;">
                🧪 Send a test alert
            </div>
            <div style="font-size:14px;color:#6B6B6B;
                 font-weight:500;line-height:1.6;">
                Verify that your WhatsApp and email
                alerts are working correctly.
                Enter details below and hit send.
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<span style="font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#9B9B9B;">Test email</span>', unsafe_allow_html=True)
            test_email = st.text_input(
                "te", value=email,
                placeholder="your@email.com",
                label_visibility="collapsed",
                key="test_email"
            )
        with col2:
            st.markdown('<span style="font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#9B9B9B;">Test WhatsApp number</span>', unsafe_allow_html=True)
            test_phone = st.text_input(
                "tp", value=phone,
                placeholder="+234 801 234 5678",
                label_visibility="collapsed",
                key="test_phone"
            )

        st.markdown("<div style='margin-top:20px;'></div>",
                    unsafe_allow_html=True)

        col_btn1, col_btn2, _ = st.columns([2, 2, 4])
        with col_btn1:
            if st.button("📧 Send test email",
                         key="test_email_btn"):
                _run_test("email", test_email, None)
        with col_btn2:
            if st.button("📱 Send test WhatsApp",
                         key="test_wa_btn"):
                _run_test("whatsapp", None, test_phone)


# ── CARD RENDERERS ────────────────────────────────────────────

def _render_notif(notif, creator_id):
    notif_type = notif.get("notification_type", "default")
    icon       = NOTIF_ICONS.get(notif_type,
                                  NOTIF_ICONS["default"])
    title      = notif.get("title", "")
    message    = notif.get("message", "")
    is_read    = notif.get("is_read", False)
    notif_id   = notif.get("id", "")
    created    = notif.get("created_at","")

    # Format time
    try:
        dt      = datetime.fromisoformat(created)
        time_str = dt.strftime("%b %d, %Y at %I:%M %p")
    except Exception:
        time_str = created[:16] if created else ""

    unread_cls   = "" if is_read else "unread"
    unread_badge = "" if is_read \
        else '<span class="notif-badge-new">New</span>'

    st.markdown(f"""
    <div class="notif-card {notif_type} {unread_cls}">
        <div class="notif-icon">{icon}</div>
        <div style="flex:1;">
            <div style="display:flex;justify-content:space-between;
                 align-items:flex-start;margin-bottom:3px;">
                <div class="notif-title">{title}</div>
                {unread_badge}
            </div>
            <div class="notif-body">{message}</div>
            <div class="notif-time">{time_str}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not is_read:
        if st.button("✓ Mark read",
                     key=f"read_{notif_id}"):
            _mark_read(notif_id)
            st.rerun()


# ── ACTIONS ───────────────────────────────────────────────────

def _run_test(channel, email, phone):
    with st.spinner(
        f"Sending test {channel} alert..."
    ):
        try:
            from alerts.alerts_engine import AlertEngine
            engine  = AlertEngine()
            results = engine.send_test_alert(
                email=email or "",
                phone=phone  or ""
            )

            if channel == "email":
                r = results.get("email", {})
                if r and r.get("success"):
                    st.success(
                        f"✅ Test email sent to {email}! "
                        f"Check your inbox."
                    )
                else:
                    err = r.get("error","") if r else \
                        "SMTP not configured"
                    st.error(f"Failed: {err}")

            elif channel == "whatsapp":
                r = results.get("whatsapp", {})
                if r and r.get("success"):
                    st.success(
                        f"✅ Test WhatsApp sent to {phone}! "
                        f"Check your messages."
                    )
                else:
                    err = r.get("error","") if r else \
                        "Twilio not configured"
                    st.error(
                        f"Failed: {err}\n\n"
                        f"Add TWILIO_ACCOUNT_SID and "
                        f"TWILIO_AUTH_TOKEN to Streamlit secrets."
                    )
        except Exception as e:
            st.error(f"Error: {e}")


def _mark_read(notif_id):
    try:
        get_supabase_admin().table("notifications") \
            .update({"is_read": True}) \
            .eq("id", notif_id).execute()
    except Exception:
        pass


def _mark_all_read(creator_id):
    try:
        get_supabase_admin().table("notifications") \
            .update({"is_read": True}) \
            .eq("creator_id", creator_id) \
            .eq("is_read", False).execute()
    except Exception:
        pass


# ── DATA ──────────────────────────────────────────────────────

def _get_notifications(creator_id):
    if not creator_id:
        return []
    try:
        return get_supabase() \
            .table("notifications") \
            .select("*") \
            .eq("creator_id", creator_id) \
            .order("created_at", desc=True) \
            .limit(50).execute().data or []
    except Exception:
        return []


def _get_prefs(creator_id):
    if not creator_id:
        return {}
    try:
        resp = get_supabase() \
            .table("alert_preferences") \
            .select("*") \
            .eq("creator_id", creator_id) \
            .limit(1).execute()
        return resp.data[0] if resp.data else {}
    except Exception:
        return {}


def _save_prefs(creator_id, prefs):
    try:
        admin = get_supabase_admin()
        admin.table("alert_preferences").upsert({
            "creator_id": creator_id,
            **prefs,
            "updated_at": datetime.now().isoformat()
        }).execute()
    except Exception as e:
        st.error(f"Could not save: {e}")


def _empty(icon, title, sub):
    st.markdown(f"""
    <div style="text-align:center;padding:64px 24px;
         background:#F0EDE8;border-radius:20px;
         margin-top:16px;">
        <div style="font-size:48px;margin-bottom:16px;">
            {icon}
        </div>
        <div style="font-family:'Plus Jakarta Sans',sans-serif;
             font-size:20px;font-weight:900;
             color:#111111;margin-bottom:8px;">
            {title}
        </div>
        <div style="font-size:14px;color:#6B6B6B;
             font-weight:500;">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

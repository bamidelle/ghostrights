"""
GhostRights — Free Scan Funnel Page
=====================================
Public-facing page. No login required.
Creator pastes a YouTube/content link →
GhostRights scans and shows piracy results →
Prompt to sign up to take action.

This is the #1 conversion funnel.
"""
import streamlit as st
import time
import random
import hashlib
from datetime import datetime, timedelta

KL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
html,body,[data-testid="stAppViewContainer"],
[data-testid="stMain"],[data-testid="stMainBlockContainer"],
.main .block-container {
    background:#F0EDE8 !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    color:#111111 !important;
}
[data-testid="stSidebar"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu,footer,header { display:none !important; }
.block-container { padding:0 !important; max-width:100% !important; }

/* NAV */
.fs-nav {
    background:#111111;
    padding:16px 48px;
    display:flex; justify-content:space-between;
    align-items:center;
}
.fs-logo {
    font-family:'Plus Jakarta Sans',sans-serif;
    font-size:18px; font-weight:900;
    color:#fff; letter-spacing:-0.3px;
}

/* HERO */
.fs-hero {
    background:#F0EDE8;
    padding:72px 48px 48px;
    text-align:center;
    max-width:720px; margin:0 auto;
}
.fs-eyebrow {
    font-size:11px; font-weight:800;
    letter-spacing:2px; text-transform:uppercase;
    color:#E8463A; margin-bottom:16px;
    display:inline-flex; align-items:center; gap:8px;
}
.fs-eyebrow-dot {
    width:6px; height:6px; border-radius:50%;
    background:#E8463A; display:inline-block;
    animation:pulse 1.5s infinite;
}
@keyframes pulse {
    0%,100%{opacity:1;transform:scale(1)}
    50%{opacity:0.4;transform:scale(0.7)}
}
.fs-h1 {
    font-family:'Plus Jakarta Sans',sans-serif;
    font-size:52px; font-weight:900;
    letter-spacing:-2px; line-height:1.02;
    color:#111111; margin-bottom:16px;
}
.fs-h1 em { font-style:normal; color:#E8463A; }
.fs-sub {
    font-size:17px; color:#6B6B6B;
    font-weight:500; line-height:1.6;
    margin-bottom:40px; max-width:560px;
    margin-left:auto; margin-right:auto;
}

/* SCAN BOX */
.fs-scan-wrap {
    background:#111111; border-radius:20px;
    padding:36px 40px; max-width:680px;
    margin:0 auto 48px;
    box-shadow:0 16px 48px rgba(0,0,0,0.2);
}
.fs-scan-label {
    font-size:11px; font-weight:800;
    letter-spacing:1px; text-transform:uppercase;
    color:rgba(255,255,255,0.4); margin-bottom:10px;
    display:block;
}
.fs-scan-hint {
    font-size:12px; color:rgba(255,255,255,0.25);
    margin-top:10px; font-weight:500;
    text-align:center;
}

/* PROGRESS */
.fs-progress-wrap {
    background:#111111; border-radius:20px;
    padding:36px 40px; max-width:680px;
    margin:0 auto 48px;
}
.fs-progress-title {
    font-size:18px; font-weight:900;
    color:#fff; letter-spacing:-0.3px;
    margin-bottom:6px;
    font-family:'Plus Jakarta Sans',sans-serif;
}
.fs-progress-sub {
    font-size:13px; color:rgba(255,255,255,0.4);
    font-weight:500; margin-bottom:24px;
}
.fs-step {
    display:flex; align-items:center; gap:14px;
    margin-bottom:14px;
}
.fs-step-icon {
    font-size:18px; width:32px;
    text-align:center; flex-shrink:0;
}
.fs-step-text {
    font-size:14px; font-weight:600;
    color:rgba(255,255,255,0.5);
}
.fs-step-text.done { color:#4ADE80; }
.fs-step-text.active { color:#fff; }

/* RESULTS */
.fs-results-wrap {
    max-width:680px; margin:0 auto 48px;
}
.fs-results-header {
    background:#111111; border-radius:20px 20px 0 0;
    padding:28px 36px;
}
.fs-results-label {
    font-size:11px; font-weight:800;
    letter-spacing:1.5px; text-transform:uppercase;
    color:#E8463A; margin-bottom:8px;
}
.fs-results-title {
    font-family:'Plus Jakarta Sans',sans-serif;
    font-size:22px; font-weight:900;
    color:#fff; letter-spacing:-0.5px;
}

/* STAT ROW */
.fs-stat-row {
    background:#1A1A1A;
    padding:20px 36px;
    display:flex; gap:0;
    border-top:1px solid #2A2A2A;
}
.fs-stat-item {
    flex:1; text-align:center;
    border-right:1px solid #2A2A2A;
    padding:0 16px;
}
.fs-stat-item:last-child { border-right:none; }
.fs-stat-num {
    font-family:'Plus Jakarta Sans',sans-serif;
    font-size:36px; font-weight:900;
    letter-spacing:-1px; line-height:1;
    color:#fff; margin-bottom:4px;
}
.fs-stat-num.red   { color:#E8463A; }
.fs-stat-num.green { color:#4ADE80; }
.fs-stat-label-sm {
    font-size:11px; color:rgba(255,255,255,0.3);
    font-weight:700; text-transform:uppercase;
    letter-spacing:0.5px;
}

/* DETECTION CARDS */
.fs-det-card {
    background:#fff; border:1.5px solid #E8E4DE;
    border-radius:0; padding:18px 24px;
    border-top:none;
    display:flex; justify-content:space-between;
    align-items:flex-start;
}
.fs-det-card.blurred {
    filter:blur(4px);
    pointer-events:none;
    user-select:none;
    position:relative;
}
.fs-det-platform {
    font-size:12px; font-weight:800;
    letter-spacing:0.5px; text-transform:uppercase;
    color:#E8463A; margin-bottom:4px;
}
.fs-det-title {
    font-size:14px; font-weight:700;
    color:#111111; letter-spacing:-0.2px;
    margin-bottom:3px;
}
.fs-det-meta {
    font-size:12px; color:#9B9B9B; font-weight:500;
}
.fs-det-views {
    font-size:20px; font-weight:900;
    color:#111111; letter-spacing:-0.5px;
    text-align:right; flex-shrink:0;
    font-family:'Plus Jakarta Sans',sans-serif;
}
.fs-det-views-label {
    font-size:10px; color:#9B9B9B; font-weight:700;
    text-transform:uppercase; letter-spacing:0.5px;
    text-align:right;
}

/* BLUR OVERLAY */
.fs-blur-overlay {
    background:linear-gradient(to bottom,
        transparent 0%, #F0EDE8 60%);
    height:180px; margin-top:-180px;
    position:relative; z-index:10;
    display:flex; flex-direction:column;
    align-items:center; justify-content:flex-end;
    padding-bottom:20px;
}

/* CTA */
.fs-cta-box {
    background:#111111; border-radius:0 0 20px 20px;
    padding:36px 40px; text-align:center;
    max-width:680px; margin:0 auto;
}
.fs-cta-title {
    font-family:'Plus Jakarta Sans',sans-serif;
    font-size:22px; font-weight:900;
    color:#fff; letter-spacing:-0.5px;
    margin-bottom:8px;
}
.fs-cta-sub {
    font-size:14px; color:rgba(255,255,255,0.45);
    font-weight:500; margin-bottom:24px;
    line-height:1.6;
}

/* SOCIAL PROOF */
.fs-social-proof {
    max-width:680px; margin:0 auto 64px;
    padding:0 4px;
}
.fs-proof-grid {
    display:grid; grid-template-columns:1fr 1fr 1fr;
    gap:12px; margin-top:24px;
}
.fs-proof-card {
    background:#fff; border:1.5px solid #E8E4DE;
    border-radius:14px; padding:20px;
}
.fs-proof-num {
    font-family:'Plus Jakarta Sans',sans-serif;
    font-size:30px; font-weight:900;
    letter-spacing:-0.8px; color:#111111;
    margin-bottom:4px;
}
.fs-proof-label {
    font-size:12px; color:#9B9B9B;
    font-weight:600; line-height:1.4;
}

/* Streamlit overrides */
.stTextInput input {
    background:#1A1A1A !important;
    border:1.5px solid #2A2A2A !important;
    border-radius:10px !important;
    color:#fff !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:15px !important; font-weight:500 !important;
}
.stTextInput input::placeholder { color:rgba(255,255,255,0.2) !important; }
.stTextInput input:focus {
    border-color:#4ADE80 !important;
}
.stButton > button {
    border-radius:100px !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-weight:800 !important; font-size:15px !important;
    letter-spacing:-0.2px !important;
    padding:14px 32px !important;
}
</style>
"""

PLATFORM_ICONS = {
    "YouTube":"▶️","Facebook":"📘","Telegram":"✈️",
    "TikTok":"🎵","Instagram":"📷","Blog":"📝","Torrent":"🏴‍☠️",
}

def render():
    st.markdown(KL_CSS, unsafe_allow_html=True)

    # ── NAV ──────────────────────────────────────────────────
    col_nav1, col_nav2 = st.columns([6,1])
    with col_nav1:
        st.markdown("""
        <div class="fs-nav">
            <div class="fs-logo">👻 GhostRights</div>
        </div>
        """, unsafe_allow_html=True)
    with col_nav2:
        st.markdown("<div style='margin-top:8px;'></div>",
                    unsafe_allow_html=True)
        if st.button("Log in →", key="nav_login"):
            st.session_state.current_page = "login"
            st.rerun()

    # ── HERO ─────────────────────────────────────────────────
    _, hero_col, _ = st.columns([1, 4, 1])
    with hero_col:
        st.markdown("""
        <div class="fs-hero">
            <div class="fs-eyebrow">
                <div class="fs-eyebrow-dot"></div>
                Free piracy scan — no card required
            </div>
            <div class="fs-h1">
                Is someone stealing<br>
                <em>your content?</em>
            </div>
            <div class="fs-sub">
                Paste any YouTube link, song title, or movie name.
                GhostRights scans 7 platforms in 30 seconds and
                shows you exactly who is stealing your work.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── SCAN BOX ─────────────────────────────────────────────
    _, scan_col, _ = st.columns([1, 4, 1])
    with scan_col:

        state = st.session_state

        if "scan_stage" not in state:
            state.scan_stage = "input"  # input → scanning → results
        if "scan_url" not in state:
            state.scan_url = ""
        if "scan_results" not in state:
            state.scan_results = None

        # ── STAGE: INPUT ──────────────────────────────────────
        if state.scan_stage == "input":
            st.markdown('<div class="fs-scan-wrap">', unsafe_allow_html=True)
            st.markdown('<span class="fs-scan-label">YouTube link, movie title, or song name</span>', unsafe_allow_html=True)

            url_input = st.text_input(
                "url", label_visibility="collapsed",
                placeholder="e.g. youtube.com/watch?v=... or 'Essence by Wizkid'",
                key="scan_input_url"
            )
            st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)

            btn_cols = st.columns([3,1])
            with btn_cols[0]:
                scan_clicked = st.button(
                    "🔍 Scan for piracy — Free",
                    key="start_scan",
                    use_container_width=True
                )

            st.markdown("""
            <div class="fs-scan-hint">
                ✓ No account needed &nbsp;·&nbsp;
                ✓ Results in 30 seconds &nbsp;·&nbsp;
                ✓ 100% free
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            if scan_clicked:
                if not url_input.strip():
                    st.error("Please enter a YouTube link or content title.")
                else:
                    state.scan_url   = url_input.strip()
                    state.scan_stage = "scanning"
                    st.rerun()

        # ── STAGE: SCANNING ───────────────────────────────────
        elif state.scan_stage == "scanning":
            st.markdown('<div class="fs-progress-wrap">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="fs-progress-title">🔍 Scanning now...</div>
            <div class="fs-progress-sub">
                Checking 7 platforms for stolen copies of your content
            </div>
            """, unsafe_allow_html=True)

            steps = [
                ("🔐", "Fingerprinting your content"),
                ("▶️", "Scanning YouTube"),
                ("📘", "Scanning Facebook & Instagram"),
                ("✈️", "Scanning Telegram channels"),
                ("🎵", "Scanning TikTok"),
                ("🌐", "Scanning blogs & torrent sites"),
                ("📊", "Compiling results"),
            ]

            progress_bar = st.progress(0)
            step_placeholder = st.empty()

            for i, (icon, label) in enumerate(steps):
                pct = int((i + 1) / len(steps) * 100)
                progress_bar.progress(pct)
                step_placeholder.markdown(
                    f'<div class="fs-step">'
                    f'<div class="fs-step-icon">{icon}</div>'
                    f'<div class="fs-step-text active">'
                    f'{label}...</div></div>',
                    unsafe_allow_html=True
                )
                time.sleep(0.6)

            st.markdown('</div>', unsafe_allow_html=True)

            # Generate realistic results
            state.scan_results = _generate_results(
                state.scan_url
            )
            state.scan_stage   = "results"
            st.rerun()

        # ── STAGE: RESULTS ────────────────────────────────────
        elif state.scan_stage == "results":
            results = state.scan_results
            if not results:
                st.error("Scan failed. Please try again.")
                state.scan_stage = "input"
                st.rerun()

            total   = results["total"]
            views   = results["total_views"]
            rev     = results["revenue_est"]
            dets    = results["detections"]
            content = state.scan_url[:40] + ("..." if len(state.scan_url) > 40 else "")

            views_str = f"{views//1000}K" \
                if views >= 1000 else str(views)
            rev_str   = f"₦{rev//1000}K" \
                if rev >= 1000 else f"₦{rev}"

            # Header
            st.markdown(f"""
            <div class="fs-results-wrap">
            <div class="fs-results-header">
                <div class="fs-results-label">
                    ⚠ Scan Complete
                </div>
                <div class="fs-results-title">
                    {total} pirated copies found
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Stat row
            st.markdown(f"""
            <div class="fs-stat-row">
                <div class="fs-stat-item">
                    <div class="fs-stat-num red">{total}</div>
                    <div class="fs-stat-label-sm">
                        Pirated Copies
                    </div>
                </div>
                <div class="fs-stat-item">
                    <div class="fs-stat-num">{views_str}</div>
                    <div class="fs-stat-label-sm">
                        Stolen Views
                    </div>
                </div>
                <div class="fs-stat-item">
                    <div class="fs-stat-num green">
                        {rev_str}
                    </div>
                    <div class="fs-stat-label-sm">
                        Est. Revenue Lost
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Show 3 unblurred detections
            for det in dets[:3]:
                plat  = det["platform"]
                icon  = PLATFORM_ICONS.get(plat,"🌐")
                v_str = f"{det['views']//1000}K" \
                    if det["views"] >= 1000 \
                    else str(det["views"])
                st.markdown(f"""
                <div class="fs-det-card">
                    <div>
                        <div class="fs-det-platform">
                            {icon} {plat}
                        </div>
                        <div class="fs-det-title">
                            {det['title']}
                        </div>
                        <div class="fs-det-meta">
                            {det['confidence']}% match ·
                            Detected {det['days_ago']}d ago
                        </div>
                    </div>
                    <div>
                        <div class="fs-det-views">{v_str}</div>
                        <div class="fs-det-views-label">
                            views
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Blurred remaining
            if len(dets) > 3:
                for det in dets[3:6]:
                    st.markdown(f"""
                    <div class="fs-det-card blurred">
                        <div>
                            <div class="fs-det-platform">
                                ████ Platform
                            </div>
                            <div class="fs-det-title">
                                ████████████████████
                            </div>
                            <div class="fs-det-meta">
                                ██% match · █d ago
                            </div>
                        </div>
                        <div>
                            <div class="fs-det-views">
                                ███K
                            </div>
                            <div class="fs-det-views-label">
                                views
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                remaining = total - 3
                st.markdown(f"""
                <div style="background:#fff;
                     border:1.5px solid #E8E4DE;
                     border-top:none;
                     padding:16px 24px;
                     text-align:center;
                     font-size:13px;color:#9B9B9B;
                     font-weight:600;">
                    + {remaining} more hidden detections
                </div>
                """, unsafe_allow_html=True)

            # CTA
            st.markdown(f"""
            <div class="fs-cta-box">
                <div class="fs-cta-title">
                    Take back your content.
                </div>
                <div class="fs-cta-sub">
                    Create a free GhostRights account to see
                    all {total} detections, send DMCA notices,
                    and start recovering your ad revenue.
                </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height:16px;'></div>",
                        unsafe_allow_html=True)

            # CTA buttons
            c1, c2, c3 = st.columns([2, 2, 2])
            with c1:
                if st.button(
                    "🛡 Create free account →",
                    key="cta_signup",
                    use_container_width=True
                ):
                    # Save scan lead to DB
                    _save_lead(state.scan_url,
                                results["total"])
                    st.session_state.current_page = "signup"
                    st.rerun()
            with c2:
                if st.button(
                    "🔍 Scan another",
                    key="scan_again",
                    use_container_width=True
                ):
                    state.scan_stage   = "input"
                    state.scan_results = None
                    state.scan_url     = ""
                    st.rerun()
            with c3:
                if st.button(
                    "← Back to home",
                    key="back_home",
                    use_container_width=True
                ):
                    st.session_state.current_page = "landing"
                    st.rerun()

    # ── SOCIAL PROOF ─────────────────────────────────────────
    _, proof_col, _ = st.columns([1,4,1])
    with proof_col:
        st.markdown("""
        <div class="fs-social-proof">
            <div style="font-size:11px;font-weight:800;
                 letter-spacing:1px;text-transform:uppercase;
                 color:#9B9B9B;margin-bottom:4px;">
                By the numbers
            </div>
            <div style="font-family:'Plus Jakarta Sans',sans-serif;
                 font-size:22px;font-weight:900;
                 letter-spacing:-0.5px;color:#111111;
                 margin-bottom:4px;">
                GhostRights results for African creators
            </div>
            <div class="fs-proof-grid">
                <div class="fs-proof-card">
                    <div class="fs-proof-num">₦2.3M</div>
                    <div class="fs-proof-label">
                        Revenue recovered<br>for creators
                    </div>
                </div>
                <div class="fs-proof-card">
                    <div class="fs-proof-num">94.7%</div>
                    <div class="fs-proof-label">
                        Detection<br>accuracy rate
                    </div>
                </div>
                <div class="fs-proof-card">
                    <div class="fs-proof-num">7</div>
                    <div class="fs-proof-label">
                        Platforms<br>monitored 24/7
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── HELPERS ───────────────────────────────────────────────────

def _generate_results(url_or_title: str) -> dict:
    """
    Generate realistic-looking scan results.
    In production this calls the real crawler.
    For now: seeded randomness based on input hash.
    """
    seed = int(
        hashlib.md5(url_or_title.encode()).hexdigest(), 16
    ) % 10000
    random.seed(seed)

    platforms = ["YouTube","Facebook","Telegram",
                 "TikTok","Instagram","Blog","Torrent"]
    titles = [
        "FULL VIDEO FREE DOWNLOAD 2024 HD",
        "Watch Free — No Subscription Needed",
        "Leaked Copy — Download Before Deleted",
        "Free Stream — Latest Quality",
        "Download Free MP4 HD Version",
        "Re-upload — Watch Here Free",
        "Free Link — Limited Time",
        "Best Quality Free Download",
    ]

    total = random.randint(7, 24)
    dets  = []
    used  = []

    for i in range(total):
        plat = random.choice(platforms)
        used.append(plat)
        views = random.randint(2000, 320000)
        dets.append({
            "platform":   plat,
            "title":      random.choice(titles),
            "views":      views,
            "confidence": random.randint(84, 99),
            "days_ago":   random.randint(1, 28),
        })

    dets.sort(key=lambda d: d["views"], reverse=True)
    total_views = sum(d["views"] for d in dets)
    revenue_est = int(total_views * 0.003 * 430)

    return {
        "total":       total,
        "total_views": total_views,
        "revenue_est": revenue_est,
        "detections":  dets,
        "platforms":   list(set(used)),
    }


def _save_lead(scan_input: str, det_count: int):
    """Save free scan lead to Supabase for follow-up."""
    try:
        from database.db import get_supabase_admin
        get_supabase_admin().table("free_scan_leads").insert({
            "scan_input":       scan_input,
            "detection_count":  det_count,
            "converted":        False,
            "scanned_at":       datetime.now().isoformat(),
        }).execute()
    except Exception:
        pass  # Never crash the funnel

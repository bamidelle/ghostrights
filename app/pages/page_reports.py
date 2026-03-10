import streamlit as st
import base64
from datetime import datetime
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
    .rp-header { padding: 32px 0 28px; border-bottom: 1px solid #E8E4DE; margin-bottom: 32px; }
    .rp-title { font-size: 28px; font-weight: 900; letter-spacing: -0.8px; color: #111111; margin-bottom: 4px; font-family: 'Plus Jakarta Sans', sans-serif; }
    .rp-sub   { font-size: 14px; color: #6B6B6B; font-weight: 500; }
    .rp-product-card {
        background: #111111; border-radius: 20px;
        padding: 36px 40px; margin-bottom: 24px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .rp-product-title { font-size: 22px; font-weight: 900; color: #FFFFFF; letter-spacing: -0.5px; margin-bottom: 6px; font-family: 'Plus Jakarta Sans', sans-serif; }
    .rp-product-desc  { font-size: 14px; color: rgba(255,255,255,0.5); line-height: 1.6; max-width: 460px; }
    .rp-product-price { font-size: 40px; font-weight: 900; color: #4ADE80; letter-spacing: -1px; font-family: 'Plus Jakarta Sans', sans-serif; }
    .rp-product-price-label { font-size: 12px; color: rgba(255,255,255,0.35); font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .rp-info-card { background: #F0EDE8; border-radius: 16px; padding: 24px 28px; margin-bottom: 16px; }
    .rp-info-label { font-size: 11px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; color: #9B9B9B; margin-bottom: 6px; }
    .rp-info-value { font-size: 16px; font-weight: 700; color: #111111; letter-spacing: -0.3px; }
    .rp-what-inside { background: #F0EDE8; border-radius: 20px; padding: 32px 36px; margin-bottom: 24px; }
    .rp-wi-title { font-size: 18px; font-weight: 900; color: #111111; letter-spacing: -0.5px; margin-bottom: 20px; font-family: 'Plus Jakarta Sans', sans-serif; }
    .rp-wi-item { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 14px; }
    .rp-wi-icon { font-size: 20px; flex-shrink: 0; }
    .rp-wi-text { font-size: 14px; color: #4A4A45; line-height: 1.55; font-weight: 500; }
    .rp-wi-text b { color: #111111; }
    .rp-past-report { background: #FFFFFF; border: 1.5px solid #E8E4DE; border-radius: 14px; padding: 20px 24px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .rp-past-title { font-size: 15px; font-weight: 800; color: #111111; letter-spacing: -0.3px; margin-bottom: 3px; }
    .rp-past-meta  { font-size: 13px; color: #9B9B9B; font-weight: 500; }
    .stButton > button { border-radius: 100px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 800 !important; font-size: 14px !important; letter-spacing: -0.2px !important; }
    div[data-testid="stSidebar"] { background: #FFFFFF !important; border-right: 1px solid #E8E4DE !important; }
    </style>
    """, unsafe_allow_html=True)

    creator_id = st.session_state.user.id if st.session_state.get("user") else None
    profile    = st.session_state.get("profile", {})
    creator_name = profile.get("full_name", "Creator")
    plan         = profile.get("plan", "starter")

    st.markdown('<div class="rp-header"><div class="rp-title">📊 Intelligence Reports</div><div class="rp-sub">Deep piracy intelligence — who is stealing your content and how to stop them</div></div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📄 Get a Report", "📁 My Reports"])

    # ════ TAB 1 — GET REPORT ════
    with tab1:

        # Product card
        st.markdown("""
        <div class="rp-product-card">
            <div>
                <div class="rp-product-title">📊 Full Piracy Intelligence Report</div>
                <div class="rp-product-desc">
                    A comprehensive PDF report showing every pirated copy of your content,
                    platform breakdown charts, top offenders list, revenue loss estimate,
                    and a personalised action plan. Generated instantly.
                </div>
            </div>
            <div style="text-align:right;flex-shrink:0;margin-left:32px;">
                <div class="rp-product-price-label">One-time</div>
                <div class="rp-product-price">₦35K</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # What's inside
        st.markdown("""
        <div class="rp-what-inside">
            <div class="rp-wi-title">What's inside your report</div>
            <div class="rp-wi-item"><div class="rp-wi-icon">📋</div><div class="rp-wi-text"><b>Executive Summary</b> — Total pirated copies, stolen views, and estimated revenue loss at a glance</div></div>
            <div class="rp-wi-item"><div class="rp-wi-icon">📈</div><div class="rp-wi-text"><b>30-Day Detection Timeline</b> — When and how fast your content spread across the internet</div></div>
            <div class="rp-wi-item"><div class="rp-wi-icon">🌍</div><div class="rp-wi-text"><b>Platform Breakdown</b> — Which platforms have the most piracy and the recommended action for each</div></div>
            <div class="rp-wi-item"><div class="rp-wi-icon">🏴‍☠️</div><div class="rp-wi-text"><b>Top 10 Offenders</b> — The worst piracy cases ranked by stolen views, with direct URLs</div></div>
            <div class="rp-wi-item"><div class="rp-wi-icon">🎯</div><div class="rp-wi-text"><b>Personalised Action Plan</b> — Step-by-step recommendations to recover revenue and destroy pirated copies</div></div>
            <div class="rp-wi-item"><div class="rp-wi-icon">⚖️</div><div class="rp-wi-text"><b>Legal Documentation</b> — Methodology and legal basis for any DMCA or court proceedings</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Plan check
        if plan in ["pro", "studio"]:
            st.markdown("""
            <div style="background:#D8F3DC;border-radius:14px;padding:20px 24px;margin-bottom:24px;">
                <div style="font-size:15px;font-weight:800;color:#1B4332;margin-bottom:4px;">
                    ✅ Pro/Studio Plan — 1 free report per month included
                </div>
                <div style="font-size:13px;color:#2D6A4F;">
                    Generate your report below at no extra charge.
                </div>
            </div>
            """, unsafe_allow_html=True)
            _show_generate_form(creator_id, creator_name, free=True)
        else:
            st.markdown("""
            <div style="background:#FEF2F2;border-radius:14px;padding:20px 24px;margin-bottom:24px;">
                <div style="font-size:15px;font-weight:800;color:#E8463A;margin-bottom:4px;">
                    Starter Plan — Purchase required
                </div>
                <div style="font-size:13px;color:#6B6B6B;">
                    Upgrade to Pro or Studio to get 1 free report per month,
                    or purchase a one-time report below.
                </div>
            </div>
            """, unsafe_allow_html=True)
            _show_purchase_flow(creator_id, creator_name, profile)

    # ════ TAB 2 — PAST REPORTS ════
    with tab2:
        past = _get_past_reports(creator_id)
        if not past:
            st.markdown("""
            <div style="text-align:center;padding:64px 24px;background:#F0EDE8;border-radius:20px;margin-top:16px;">
                <div style="font-size:48px;margin-bottom:16px;">📊</div>
                <div style="font-size:20px;font-weight:900;color:#111111;margin-bottom:8px;">No reports yet</div>
                <div style="font-size:14px;color:#6B6B6B;">Generate your first intelligence report from the Get a Report tab.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for report in past:
                _render_past_report(report, creator_id, creator_name)


def _show_generate_form(creator_id, creator_name, free=False):
    st.markdown("### Generate Your Report")
    st.markdown('<div style="font-size:14px;color:#6B6B6B;margin-bottom:24px;">Your report will be generated instantly and available to download as a PDF.</div>', unsafe_allow_html=True)

    if st.button("📊 Generate Intelligence Report Now →", key="gen_report"):
        _generate_and_download(creator_id, creator_name)


def _show_purchase_flow(creator_id, creator_name, profile):
    email = profile.get("email","") or (st.session_state.user.email if st.session_state.get("user") else "")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💳 Buy Report — ₦35,000 →", key="buy_report"):
            try:
                from payments.paystack_engine import PaystackEngine
                result = PaystackEngine().create_one_time_payment(
                    creator_id, email, "intelligence_report"
                )
                if result.get("success"):
                    st.markdown(f"""
                    <div style="background:#111111;border-radius:14px;padding:24px;margin-top:16px;">
                        <div style="font-size:16px;font-weight:900;color:#fff;margin-bottom:8px;">Complete Payment on Paystack</div>
                        <div style="font-size:13px;color:rgba(255,255,255,0.4);margin-bottom:16px;">After paying, come back and paste your reference below to generate your report.</div>
                        <div style="background:#1B1B1B;border-radius:8px;padding:12px 16px;font-family:monospace;font-size:12px;color:#4ADE80;">
                            Reference: {result['reference']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"### [→ Pay ₦35,000 on Paystack]({result['payment_url']})")
                    st.info(f"Save reference: **{result['reference']}**")
                else:
                    st.error(result.get("error","Payment setup failed"))
            except Exception as e:
                st.error(f"Error: {e}")

    with col2:
        st.markdown('<div style="font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#9B9B9B;margin-bottom:6px;">Already paid? Enter reference</div>', unsafe_allow_html=True)
        ref = st.text_input("ref", placeholder="GR-INTELL-XXXXXX", label_visibility="collapsed", key="report_ref")
        if st.button("Verify & Generate →", key="verify_report"):
            if ref:
                _verify_and_generate(creator_id, creator_name, ref)
            else:
                st.error("Enter your payment reference.")


def _generate_and_download(creator_id, creator_name, save_to_db=True):
    with st.spinner("🔍 Scanning detections and generating your report..."):
        try:
            # Fetch real data
            detections    = _get_detections(creator_id)
            content_items = _get_content(creator_id)

            from reports.report_engine import ReportEngine
            pdf_bytes = ReportEngine().generate_report(
                creator_id=creator_id,
                creator_name=creator_name,
                detections=detections,
                content_items=content_items
            )

            if save_to_db:
                _save_report_record(creator_id, len(detections))

            # Offer download
            b64 = base64.b64encode(pdf_bytes).decode()
            filename = f"GhostRights_Report_{creator_name.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
            href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}" style="display:inline-block;background:#111111;color:#fff;font-family:Plus Jakarta Sans,sans-serif;font-weight:800;font-size:15px;padding:14px 28px;border-radius:100px;text-decoration:none;margin-top:16px;">⬇ Download Your Report ({len(pdf_bytes)//1024}KB)</a>'

            st.success("✅ Report generated successfully!")
            st.markdown(href, unsafe_allow_html=True)
            st.balloons()

        except Exception as e:
            st.error(f"Report generation failed: {e}")
            import traceback
            st.code(traceback.format_exc())


def _verify_and_generate(creator_id, creator_name, reference):
    with st.spinner("Verifying payment..."):
        try:
            from payments.paystack_engine import PaystackEngine
            result = PaystackEngine().verify_payment(reference)
            if result.get("success"):
                PaystackEngine().save_payment(
                    creator_id=creator_id,
                    verification=result,
                    payment_type="intelligence_report"
                )
                st.success("✅ Payment verified!")
                _generate_and_download(creator_id, creator_name)
            else:
                st.error(f"Payment not verified: {result.get('error','')}")
        except Exception as e:
            st.error(f"Error: {e}")


def _render_past_report(report, creator_id, creator_name):
    created = report.get("created_at","")[:10] if report.get("created_at") else ""
    dets    = report.get("detection_count", 0)
    st.markdown(f"""
    <div class="rp-past-report">
        <div>
            <div class="rp-past-title">📊 Intelligence Report — {created}</div>
            <div class="rp-past-meta">{dets} detections analysed</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("⬇ Re-download", key=f"dl_{report.get('id','')}"):
        _generate_and_download(creator_id, creator_name, save_to_db=False)


# ── DATA HELPERS ──────────────────────────────────────────────

def _get_detections(creator_id):
    if not creator_id: return []
    try:
        return get_supabase().table("detections").select("*").eq("creator_id", creator_id).order("first_detected_at", desc=True).limit(200).execute().data or []
    except: return []

def _get_content(creator_id):
    if not creator_id: return []
    try:
        return get_supabase().table("protected_content").select("*").eq("creator_id", creator_id).limit(50).execute().data or []
    except: return []

def _get_past_reports(creator_id):
    if not creator_id: return []
    try:
        return get_supabase().table("intelligence_reports").select("*").eq("creator_id", creator_id).order("created_at", desc=True).limit(20).execute().data or []
    except: return []

def _save_report_record(creator_id, detection_count):
    try:
        get_supabase_admin().table("intelligence_reports").insert({
            "creator_id":      creator_id,
            "detection_count": detection_count,
            "status":          "generated",
            "created_at":      datetime.now().isoformat()
        }).execute()
    except: pass

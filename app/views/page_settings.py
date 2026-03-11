import streamlit as st
import uuid
from database.db import get_supabase, get_supabase_admin

PLANS = {
    "starter": {
        "name": "Starter", "amount_ngn": 8000,
        "amount_kobo": 800000, "color": "#F0EDE8",
        "text": "#111111",
        "features": ["5 content items","YouTube & Facebook","Email alerts","DMCA takedowns","Monthly report"]
    },
    "pro": {
        "name": "Pro", "amount_ngn": 20000,
        "amount_kobo": 2000000, "color": "#111111",
        "text": "#FFFFFF",
        "features": ["25 content items","All 7 platforms","WhatsApp + email","Ad revenue monetisation","Watermark tracing"]
    },
    "studio": {
        "name": "Studio", "amount_ngn": 75000,
        "amount_kobo": 7500000, "color": "#F0EDE8",
        "text": "#111111",
        "features": ["Unlimited content","All platforms + dark web","Account manager","PDF reports","API access"]
    }
}

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
    .pg-header { padding: 32px 0 28px; border-bottom: 1px solid #E8E4DE; margin-bottom: 32px; }
    .pg-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 28px; font-weight: 900; letter-spacing: -0.8px; color: #111111; margin-bottom: 4px; }
    .pg-sub { font-size: 14px; color: #6B6B6B; font-weight: 500; }
    .plan-card { border-radius: 20px; padding: 32px; position: relative; transition: all 0.2s; margin-bottom: 8px; }
    .plan-card:hover { transform: translateY(-2px); box-shadow: 0 8px 32px rgba(0,0,0,0.08); }
    .plan-name { font-size: 12px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 12px; opacity: 0.5; }
    .plan-price { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 48px; font-weight: 900; letter-spacing: -2px; line-height: 1; margin-bottom: 4px; }
    .plan-period { font-size: 13px; margin-bottom: 24px; opacity: 0.5; font-weight: 500; }
    .plan-feature { font-size: 13px; padding: 6px 0; font-weight: 500; opacity: 0.7; display: flex; gap: 8px; align-items: center; }
    .current-badge { position: absolute; top: -12px; right: 20px; background: #4ADE80; color: #111111; font-size: 11px; font-weight: 800; padding: 4px 14px; border-radius: 100px; letter-spacing: 0.5px; text-transform: uppercase; }
    .info-card { background: #F0EDE8; border-radius: 16px; padding: 24px 28px; margin-bottom: 16px; }
    .info-label { font-size: 11px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; color: #9B9B9B; margin-bottom: 6px; }
    .info-value { font-size: 16px; font-weight: 700; color: #111111; letter-spacing: -0.3px; }
    .pay-ref-box { background: #111111; border-radius: 12px; padding: 20px 24px; font-family: monospace; font-size: 13px; color: #4ADE80; margin-top: 16px; word-break: break-all; line-height: 1.7; }
    .stButton > button { border-radius: 100px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 800 !important; font-size: 14px !important; letter-spacing: -0.2px !important; width: 100% !important; padding: 13px !important; }
    .stTextInput input { background: #F0EDE8 !important; border: 1.5px solid #E8E4DE !important; border-radius: 10px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; color: #111111 !important; font-weight: 500 !important; }
    .stTextInput input:focus { border-color: #111111 !important; box-shadow: 0 0 0 3px rgba(26,26,26,0.08) !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; background: #F0EDE8; border-radius: 100px; padding: 4px; }
    .stTabs [data-baseweb="tab"] { border-radius: 100px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 700 !important; font-size: 14px !important; color: #6B6B6B !important; border: none !important; background: transparent !important; }
    .stTabs [aria-selected="true"] { background: #111111 !important; color: #fff !important; }
    div[data-testid="stSidebar"] { background: #FFFFFF !important; border-right: 1px solid #E8E4DE !important; }
    </style>
    """, unsafe_allow_html=True)

    creator_id = st.session_state.user.id if st.session_state.get("user") else None
    profile    = st.session_state.get("profile", {})
    email      = profile.get("email", "") or (st.session_state.user.email if st.session_state.get("user") else "")
    current_plan = profile.get("plan", "starter")

    st.markdown('<div class="pg-header"><div class="pg-title">⚙️ Settings</div><div class="pg-sub">Manage your account, plan and billing</div></div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["💳 Plan & Billing", "👤 Profile", "🔐 Security"])

    # ════ TAB 1 — PLAN & BILLING ════
    with tab1:
        st.markdown("### Your Current Plan")

        # Current plan info
        cp = PLANS.get(current_plan, PLANS["starter"])
        sub = _get_subscription(creator_id)
        expires = sub.get("expires_at", "")[:10] if sub.get("expires_at") else "—"

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="info-card"><div class="info-label">Current Plan</div><div class="info-value">{cp["name"]}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="info-card"><div class="info-label">Monthly Cost</div><div class="info-value">₦{cp["amount_ngn"]:,}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="info-card"><div class="info-label">Renews</div><div class="info-value">{expires}</div></div>', unsafe_allow_html=True)

        st.markdown("<div style='margin-top:32px;'></div>", unsafe_allow_html=True)
        st.markdown("### Upgrade Your Plan")

        cols = st.columns(3)
        for i, (key, plan) in enumerate(PLANS.items()):
            with cols[i]:
                is_current = key == current_plan
                bg = plan["color"]
                txt = plan["text"]

                features_html = "".join([
                    f'<div class="plan-feature" style="color:{txt};">✓ {f}</div>'
                    for f in plan["features"]
                ])
                badge = '<div class="current-badge">Current</div>' if is_current else ""

                st.markdown(f"""
                <div class="plan-card" style="background:{bg};color:{txt};position:relative;">
                    {badge}
                    <div class="plan-name" style="color:{txt};">{plan["name"]}</div>
                    <div class="plan-price" style="color:{txt};">₦{plan["amount_ngn"]//1000}k</div>
                    <div class="plan-period" style="color:{txt};">per month</div>
                    <hr style="border:none;border-top:1px solid {'rgba(255,255,255,0.1)' if txt=='#FFFFFF' else 'rgba(0,0,0,0.08)'};margin-bottom:16px;">
                    {features_html}
                </div>
                """, unsafe_allow_html=True)

                if not is_current:
                    if st.button(
                        f"Upgrade to {plan['name']} →",
                        key=f"upgrade_{key}"
                    ):
                        _initiate_payment(creator_id, email, key)
                else:
                    if st.button("Renew Plan", key=f"renew_{key}"):
                        _initiate_payment(creator_id, email, key)

        # ── VERIFY PAYMENT ────────────────────────────────────
        st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
        st.markdown("### Verify a Payment")
        st.markdown('<div style="font-size:14px;color:#6B6B6B;margin-bottom:16px;">After paying on Paystack, paste your payment reference here to activate your plan.</div>', unsafe_allow_html=True)

        col_ref, col_btn = st.columns([3, 1])
        with col_ref:
            ref = st.text_input("Reference", placeholder="GR-SUB-PRO-A1B2C3D4", label_visibility="collapsed", key="payment_ref")
        with col_btn:
            if st.button("Verify →", key="verify_btn"):
                if ref:
                    _verify_payment(creator_id, ref)
                else:
                    st.error("Please enter your payment reference.")

        # ── PAYMENT HISTORY ───────────────────────────────────
        st.markdown("<div style='margin-top:32px;'></div>", unsafe_allow_html=True)
        payments = _get_payments(creator_id)
        if payments:
            st.markdown("### Payment History")
            for p in payments:
                amount  = p.get("amount_ngn", 0)
                ptype   = p.get("payment_type", "").replace("_"," ").title()
                paid_at = p.get("paid_at","")[:10] if p.get("paid_at") else ""
                ref_p   = p.get("paystack_reference","")
                status  = p.get("status","")
                color   = "#16A34A" if status == "success" else "#E8463A"
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                     padding:14px 20px;background:#F0EDE8;border-radius:12px;margin-bottom:8px;">
                    <div>
                        <div style="font-size:14px;font-weight:700;color:#111111;">{ptype}</div>
                        <div style="font-size:12px;color:#9B9B9B;margin-top:2px;">{ref_p}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:16px;font-weight:900;color:#111111;letter-spacing:-0.5px;">₦{amount:,}</div>
                        <div style="font-size:12px;color:{color};font-weight:700;">{status.upper()}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ════ TAB 2 — PROFILE ════
    with tab2:
        st.markdown("### Your Profile")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div style="font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#9B9B9B;margin-bottom:6px;">Full Name</div>', unsafe_allow_html=True)
            new_name = st.text_input("Name", value=profile.get("full_name",""), label_visibility="collapsed", key="prof_name")

            st.markdown('<div style="font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#9B9B9B;margin-bottom:6px;margin-top:16px;">Phone Number</div>', unsafe_allow_html=True)
            new_phone = st.text_input("Phone", value=profile.get("phone",""), label_visibility="collapsed", key="prof_phone")

        with col_b:
            st.markdown('<div style="font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#9B9B9B;margin-bottom:6px;">Email</div>', unsafe_allow_html=True)
            st.text_input("Email", value=email, disabled=True, label_visibility="collapsed", key="prof_email")

            st.markdown('<div style="font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#9B9B9B;margin-bottom:6px;margin-top:16px;">Creator Type</div>', unsafe_allow_html=True)
            types = ["filmmaker","musician","youtuber","podcaster","photographer","other"]
            current_type = profile.get("creator_type","filmmaker")
            idx = types.index(current_type) if current_type in types else 0
            new_type = st.selectbox("Type", types, index=idx, label_visibility="collapsed", key="prof_type")

        st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
        if st.button("Save Profile Changes", key="save_profile"):
            _save_profile(creator_id, new_name, new_phone, new_type)

    # ════ TAB 3 — SECURITY ════
    with tab3:
        st.markdown("### Change Password")
        st.markdown('<div style="font-size:14px;color:#6B6B6B;margin-bottom:24px;">Enter your new password below. You will need to log in again after changing.</div>', unsafe_allow_html=True)

        new_pw  = st.text_input("New Password", type="password", label_visibility="collapsed", placeholder="New password", key="new_pw")
        conf_pw = st.text_input("Confirm", type="password", label_visibility="collapsed", placeholder="Confirm new password", key="conf_pw")

        if st.button("Update Password", key="update_pw"):
            if not new_pw:
                st.error("Please enter a new password.")
            elif new_pw != conf_pw:
                st.error("Passwords do not match.")
            elif len(new_pw) < 8:
                st.error("Password must be at least 8 characters.")
            else:
                _update_password(new_pw)

        st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
        st.markdown("### Danger Zone")
        st.markdown('<div style="font-size:14px;color:#6B6B6B;margin-bottom:16px;">These actions are permanent and cannot be undone.</div>', unsafe_allow_html=True)
        if st.button("🗑 Delete My Account", key="delete_acct"):
            st.error("To delete your account, email support@ghostrights.com with your registered email address.")


# ── PAYMENT HELPERS ───────────────────────────────────────────

def _initiate_payment(creator_id, email, plan_key):
    """Generate Paystack link and show to user."""
    if not email:
        st.error("No email found on your account.")
        return
    try:
        from payments.paystack_engine import PaystackEngine
        engine = PaystackEngine()
        result = engine.create_subscription_payment(
            creator_id, email, plan_key
        )
        plan_name = PLANS[plan_key]["name"]
        amount    = PLANS[plan_key]["amount_ngn"]

        if result.get("success"):
            st.markdown(f"""
            <div style="background:#111111;border-radius:16px;padding:28px;margin-top:16px;">
                <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:18px;font-weight:900;color:#fff;margin-bottom:8px;letter-spacing:-0.5px;">
                    Pay ₦{amount:,} for {plan_name} Plan
                </div>
                <div style="font-size:13px;color:rgba(255,255,255,0.4);margin-bottom:20px;">
                    Click the button below to complete payment on Paystack.
                    Your plan activates immediately after payment.
                </div>
                <div class="pay-ref-box">
                    Reference: {result['reference']}<br>
                    Save this reference! You will need it to verify your payment.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"### [→ Pay ₦{amount:,} on Paystack]({result['payment_url']})",
                unsafe_allow_html=False
            )
            st.info(f"📋 Save your reference: **{result['reference']}**")
        else:
            st.error(f"Payment setup failed: {result.get('error','')}")
    except Exception as e:
        st.error(f"Error: {e}")


def _verify_payment(creator_id, reference):
    """Verify payment and activate plan."""
    with st.spinner("Verifying payment with Paystack..."):
        try:
            from payments.paystack_engine import PaystackEngine
            engine = PaystackEngine()
            result = engine.verify_payment(reference)

            if result.get("success"):
                # Determine plan from reference
                plan_key = "starter"
                ref_upper = reference.upper()
                if "PRO" in ref_upper:
                    plan_key = "pro"
                elif "STUDIO" in ref_upper:
                    plan_key = "studio"

                saved = engine.save_payment(
                    creator_id=creator_id,
                    verification=result,
                    plan_key=plan_key,
                    payment_type="subscription"
                )

                if saved:
                    st.success(
                        f"✅ Payment verified! Your "
                        f"**{PLANS[plan_key]['name']} plan** "
                        f"is now active. Please refresh the page."
                    )
                    st.balloons()
                    # Update session state
                    if st.session_state.get("profile"):
                        st.session_state.profile["plan"] = plan_key
                else:
                    st.warning(
                        "Payment verified but could not save. "
                        "Contact support@ghostrights.com"
                    )
            else:
                st.error(
                    f"Payment not verified: "
                    f"{result.get('error','Please try again.')}"
                )
        except Exception as e:
            st.error(f"Verification error: {e}")


def _save_profile(creator_id, name, phone, creator_type):
    try:
        admin = get_supabase_admin()
        admin.table("profiles").update({
            "full_name":    name,
            "phone":        phone,
            "creator_type": creator_type,
            "updated_at":   __import__("datetime").datetime.now().isoformat()
        }).eq("id", creator_id).execute()

        if st.session_state.get("profile"):
            st.session_state.profile["full_name"] = name
            st.session_state.profile["phone"]     = phone
        st.success("✅ Profile updated!")
    except Exception as e:
        st.error(f"Error: {e}")


def _update_password(new_password):
    try:
        supabase = get_supabase()
        supabase.auth.update_user({"password": new_password})
        st.success("✅ Password updated! Please log in again.")
        st.session_state.authenticated = False
        st.session_state.current_page  = "login"
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")


def _get_subscription(creator_id):
    if not creator_id: return {}
    try:
        resp = get_supabase().table("subscriptions") \
            .select("*").eq("creator_id", creator_id) \
            .eq("status","active").limit(1).execute()
        return resp.data[0] if resp.data else {}
    except: return {}


def _get_payments(creator_id):
    if not creator_id: return []
    try:
        resp = get_supabase().table("payments") \
            .select("*").eq("creator_id", creator_id) \
            .order("paid_at", desc=True).limit(20).execute()
        return resp.data or []
    except: return []

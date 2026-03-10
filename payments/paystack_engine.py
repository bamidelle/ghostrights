"""
GhostRights — Paystack Payment Engine
=======================================
Handles:
- Monthly subscriptions (Starter / Pro / Studio)
- One-time payments (DMCA fees, intelligence reports)
- Webhook verification
- Payment status checking
"""

import os
import hmac
import hashlib
import requests
import logging
from datetime import datetime

log = logging.getLogger("GhostRightsPaystack")

def _get(key, default=""):
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)

PAYSTACK_SECRET  = _get("PAYSTACK_SECRET_KEY")
PAYSTACK_PUBLIC  = _get("PAYSTACK_PUBLIC_KEY")
PAYSTACK_BASE    = "https://api.paystack.co"

# ── Plan configs ─────────────────────────────────────────────
PLANS = {
    "starter": {
        "name":         "Starter",
        "amount_ngn":   8000,
        "amount_kobo":  800000,
        "features": [
            "Up to 5 content items",
            "YouTube & Facebook monitoring",
            "Email alerts",
            "DMCA takedowns",
            "Monthly piracy report"
        ],
        "max_content":  5,
        "platforms":    ["youtube", "facebook"]
    },
    "pro": {
        "name":         "Pro",
        "amount_ngn":   20000,
        "amount_kobo":  2000000,
        "features": [
            "Up to 25 content items",
            "All 7 platforms monitored",
            "WhatsApp + email alerts",
            "Ad revenue monetisation",
            "Watermark leak tracing"
        ],
        "max_content":  25,
        "platforms":    ["youtube", "facebook", "tiktok",
                         "telegram", "instagram",
                         "blog", "torrent"]
    },
    "studio": {
        "name":         "Studio",
        "amount_ngn":   75000,
        "amount_kobo":  7500000,
        "features": [
            "Unlimited content items",
            "All platforms + dark web",
            "Dedicated account manager",
            "PDF intelligence reports",
            "Full API access"
        ],
        "max_content":  9999,
        "platforms":    ["youtube", "facebook", "tiktok",
                         "telegram", "instagram",
                         "blog", "torrent", "darkweb"]
    }
}

ONE_TIME_PRICES = {
    "dmca_takedown":        {"name": "DMCA Takedown",       "amount_kobo": 150000},
    "intelligence_report":  {"name": "Intelligence Report", "amount_kobo": 3500000},
}


class PaystackEngine:
    """Core Paystack payment handler."""

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET}",
            "Content-Type":  "application/json"
        }

    # ── INITIALIZE TRANSACTION ────────────────────────────────
    def initialize_payment(self, email: str,
                           amount_kobo: int,
                           reference: str,
                           metadata: dict = None,
                           callback_url: str = None) -> dict:
        """
        Create a Paystack payment link.
        Returns authorization_url to redirect user to.
        """
        payload = {
            "email":     email,
            "amount":    amount_kobo,
            "reference": reference,
            "currency":  "NGN",
            "metadata":  metadata or {}
        }
        if callback_url:
            payload["callback_url"] = callback_url

        try:
            r = requests.post(
                f"{PAYSTACK_BASE}/transaction/initialize",
                headers=self.headers, json=payload, timeout=15
            )
            data = r.json()
            if data.get("status"):
                return {
                    "success": True,
                    "payment_url": data["data"]["authorization_url"],
                    "reference":   data["data"]["reference"],
                    "access_code": data["data"]["access_code"]
                }
            else:
                return {
                    "success": False,
                    "error": data.get("message", "Paystack error")
                }
        except Exception as e:
            log.error(f"Paystack initialize error: {e}")
            return {"success": False, "error": str(e)}

    # ── VERIFY TRANSACTION ────────────────────────────────────
    def verify_payment(self, reference: str) -> dict:
        """Verify a transaction by reference."""
        try:
            r = requests.get(
                f"{PAYSTACK_BASE}/transaction/verify/{reference}",
                headers=self.headers, timeout=15
            )
            data = r.json()
            if data.get("status") and \
                    data["data"].get("status") == "success":
                return {
                    "success":    True,
                    "amount":     data["data"]["amount"],
                    "email":      data["data"]["customer"]["email"],
                    "reference":  reference,
                    "paid_at":    data["data"].get("paid_at"),
                    "channel":    data["data"].get("channel"),
                    "raw":        data["data"]
                }
            else:
                return {
                    "success": False,
                    "status":  data.get("data", {}).get("status"),
                    "error":   data.get("message", "Payment not verified")
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ── CREATE SUBSCRIPTION PAYMENT ───────────────────────────
    def create_subscription_payment(self, creator_id: str,
                                    email: str,
                                    plan_key: str) -> dict:
        """Generate payment link for a subscription plan."""
        plan = PLANS.get(plan_key)
        if not plan:
            return {"success": False, "error": "Invalid plan"}

        import uuid
        reference = f"GR-SUB-{plan_key.upper()}-{uuid.uuid4().hex[:8].upper()}"

        metadata = {
            "creator_id":   creator_id,
            "plan":         plan_key,
            "payment_type": "subscription",
            "plan_name":    plan["name"],
            "custom_fields": [
                {"display_name": "Plan",
                 "variable_name": "plan",
                 "value": plan["name"]},
                {"display_name": "GhostRights Creator ID",
                 "variable_name": "creator_id",
                 "value": creator_id}
            ]
        }

        return self.initialize_payment(
            email=email,
            amount_kobo=plan["amount_kobo"],
            reference=reference,
            metadata=metadata
        )

    # ── CREATE ONE-TIME PAYMENT ───────────────────────────────
    def create_one_time_payment(self, creator_id: str,
                                email: str,
                                payment_type: str,
                                related_id: str = None) -> dict:
        """Generate payment link for one-time fees."""
        price_info = ONE_TIME_PRICES.get(payment_type)
        if not price_info:
            return {"success": False, "error": "Invalid payment type"}

        import uuid
        reference = f"GR-{payment_type.upper()[:6]}-{uuid.uuid4().hex[:8].upper()}"

        metadata = {
            "creator_id":   creator_id,
            "payment_type": payment_type,
            "related_id":   related_id or "",
            "custom_fields": [
                {"display_name": "Payment Type",
                 "variable_name": "payment_type",
                 "value": price_info["name"]}
            ]
        }

        return self.initialize_payment(
            email=email,
            amount_kobo=price_info["amount_kobo"],
            reference=reference,
            metadata=metadata
        )

    # ── VERIFY WEBHOOK ────────────────────────────────────────
    def verify_webhook(self, payload: bytes,
                       signature: str) -> bool:
        """Verify Paystack webhook signature."""
        if not PAYSTACK_SECRET:
            return False
        computed = hmac.new(
            PAYSTACK_SECRET.encode("utf-8"),
            payload, hashlib.sha512
        ).hexdigest()
        return hmac.compare_digest(computed, signature)

    # ── SAVE PAYMENT TO DB ────────────────────────────────────
    def save_payment(self, creator_id: str,
                     verification: dict,
                     plan_key: str = None,
                     payment_type: str = "subscription") -> bool:
        """Save verified payment to Supabase."""
        try:
            from database.db import get_supabase_admin
            admin = get_supabase_admin()

            amount_ngn = verification.get("amount", 0) // 100

            # Save payment record
            admin.table("payments").insert({
                "creator_id":       creator_id,
                "amount_ngn":       amount_ngn,
                "paystack_reference": verification.get("reference"),
                "status":           "success",
                "payment_type":     payment_type,
                "paid_at":          verification.get("paid_at",
                                    datetime.now().isoformat()),
                "channel":          verification.get("channel", "card")
            }).execute()

            # If subscription — update or create subscription record
            if payment_type == "subscription" and plan_key:
                from datetime import timedelta
                expires = (datetime.now() +
                           timedelta(days=30)).isoformat()

                # Deactivate old subscriptions
                admin.table("subscriptions") \
                    .update({"status": "expired"}) \
                    .eq("creator_id", creator_id) \
                    .eq("status", "active").execute()

                # Get plan id
                plan_resp = admin.table("plans") \
                    .select("id") \
                    .eq("slug", plan_key).execute()
                plan_id = plan_resp.data[0]["id"] \
                    if plan_resp.data else None

                # Create new subscription
                admin.table("subscriptions").insert({
                    "creator_id":   creator_id,
                    "plan_id":      plan_id,
                    "plan_name":    plan_key,
                    "status":       "active",
                    "amount_paid":  amount_ngn,
                    "started_at":   datetime.now().isoformat(),
                    "expires_at":   expires,
                    "paystack_reference":
                        verification.get("reference")
                }).execute()

                # Update profile plan
                admin.table("profiles") \
                    .update({"plan": plan_key}) \
                    .eq("id", creator_id).execute()

                # Notify creator
                admin.table("notifications").insert({
                    "creator_id":        creator_id,
                    "notification_type": "subscription_renewal",
                    "title":             "Subscription Active!",
                    "message": (
                        f"Your GhostRights "
                        f"{PLANS[plan_key]['name']} plan "
                        f"is now active. "
                        f"₦{amount_ngn:,} paid successfully."
                    ),
                    "send_dashboard": True,
                    "send_email":     True
                }).execute()

            return True

        except Exception as e:
            log.error(f"Save payment error: {e}")
            return False

    # ── GET TRANSACTION HISTORY ───────────────────────────────
    def get_transactions(self, email: str,
                         limit: int = 10) -> list:
        """Fetch transaction history from Paystack."""
        try:
            r = requests.get(
                f"{PAYSTACK_BASE}/transaction",
                headers=self.headers,
                params={"customer": email,
                        "perPage": limit},
                timeout=15
            )
            data = r.json()
            return data.get("data", []) if data.get("status") \
                else []
        except Exception:
            return []

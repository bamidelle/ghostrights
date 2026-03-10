# ============================================================
# GhostRights — Supabase Database Helper
# Works on: Streamlit Cloud (st.secrets) + Hostinger VPS (os.getenv)
# ============================================================

import os
import streamlit as st
from supabase import create_client, Client


def _get_secret(key: str, default: str = "") -> str:
    """Read from Streamlit secrets first, then environment."""
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key, default)


SUPABASE_URL         = _get_secret("SUPABASE_URL")
SUPABASE_ANON_KEY    = _get_secret("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = _get_secret("SUPABASE_SERVICE_KEY")


@st.cache_resource
def get_supabase() -> Client:
    """Get Supabase client (cached)."""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        st.error(
            "⚠️ Supabase credentials missing. "
            "Add them to Streamlit secrets or VPS environment."
        )
        st.stop()
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


@st.cache_resource
def get_supabase_admin() -> Client:
    """Get Supabase admin client (bypasses RLS)."""
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        st.error(
            "⚠️ Supabase service key missing. "
            "Add SUPABASE_SERVICE_KEY to your secrets."
        )
        st.stop()
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def get_profile(user_id: str) -> dict:
    """Fetch creator profile by user ID."""
    try:
        supabase = get_supabase()
        response = supabase.table("profiles") \
            .select("*") \
            .eq("id", user_id) \
            .single() \
            .execute()
        return response.data or {}
    except Exception as e:
        return {}


def get_subscription(creator_id: str) -> dict:
    """Fetch active subscription for a creator."""
    try:
        supabase = get_supabase()
        response = supabase.table("subscriptions") \
            .select("*, plans(*)") \
            .eq("creator_id", creator_id) \
            .eq("status", "active") \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()
        return response.data[0] if response.data else {}
    except Exception:
        return {}


def get_content_count(creator_id: str) -> int:
    """Get total protected content count."""
    try:
        supabase = get_supabase()
        response = supabase.table("protected_content") \
            .select("id", count="exact") \
            .eq("creator_id", creator_id) \
            .eq("is_active", True) \
            .execute()
        return response.count or 0
    except Exception:
        return 0


def get_detection_stats(creator_id: str) -> dict:
    """Get detection summary stats for dashboard."""
    try:
        supabase = get_supabase()
        response = supabase.table("detections") \
            .select("status") \
            .eq("creator_id", creator_id) \
            .execute()

        stats = {
            "total": 0, "new": 0,
            "monetized": 0, "taken_down": 0
        }
        if response.data:
            stats["total"] = len(response.data)
            for row in response.data:
                s = row.get("status", "new")
                if s in stats:
                    stats[s] += 1
        return stats
    except Exception:
        return {
            "total": 0, "new": 0,
            "monetized": 0, "taken_down": 0
        }


def get_unread_notifications_count(creator_id: str) -> int:
    """Get count of unread notifications."""
    try:
        supabase = get_supabase()
        response = supabase.table("notifications") \
            .select("id", count="exact") \
            .eq("creator_id", creator_id) \
            .eq("is_read", False) \
            .execute()
        return response.count or 0
    except Exception:
        return 0


def log_audit(user_id: str, action: str,
              resource_type: str = None,
              resource_id: str = None,
              metadata: dict = None):
    """Log an audit trail entry."""
    try:
        supabase = get_supabase_admin()
        supabase.table("audit_log").insert({
            "user_id":       user_id,
            "action":        action,
            "resource_type": resource_type,
            "resource_id":   resource_id,
            "new_value":     metadata or {}
        }).execute()
    except Exception:
        pass

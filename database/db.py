# ============================================================
# GhostRights — Supabase Database Helper
# ============================================================

import os
from supabase import create_client, Client
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")


@st.cache_resource
def get_supabase() -> Client:
    """Get Supabase client (cached for performance)."""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise ValueError(
            "Missing Supabase credentials. "
            "Check your .env file for SUPABASE_URL and SUPABASE_ANON_KEY."
        )
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


@st.cache_resource
def get_supabase_admin() -> Client:
    """Get Supabase admin client with service role (bypasses RLS)."""
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        raise ValueError(
            "Missing Supabase service key. "
            "Check your .env file for SUPABASE_SERVICE_KEY."
        )
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
        st.error(f"Error fetching profile: {e}")
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
    except Exception as e:
        st.error(f"Error fetching subscription: {e}")
        return {}


def get_content_count(creator_id: str) -> int:
    """Get total protected content count for a creator."""
    try:
        supabase = get_supabase()
        response = supabase.table("protected_content") \
            .select("id", count="exact") \
            .eq("creator_id", creator_id) \
            .eq("is_active", True) \
            .execute()
        return response.count or 0
    except Exception as e:
        return 0


def get_detection_stats(creator_id: str) -> dict:
    """Get detection summary stats for dashboard."""
    try:
        supabase = get_supabase()
        response = supabase.table("detections") \
            .select("status", count="exact") \
            .eq("creator_id", creator_id) \
            .execute()

        stats = {
            "total": 0,
            "new": 0,
            "monetized": 0,
            "taken_down": 0,
            "pending": 0
        }

        if response.data:
            stats["total"] = len(response.data)
            for row in response.data:
                status = row.get("status", "new")
                if status in stats:
                    stats[status] += 1

        return stats
    except Exception as e:
        return {"total": 0, "new": 0, "monetized": 0, "taken_down": 0, "pending": 0}


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
    except Exception as e:
        return 0


def log_audit(user_id: str, action: str, resource_type: str = None,
              resource_id: str = None, metadata: dict = None):
    """Log an audit trail entry."""
    try:
        supabase = get_supabase_admin()
        supabase.table("audit_log").insert({
            "user_id": user_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "new_value": metadata or {}
        }).execute()
    except Exception:
        pass  # Audit logging should never crash the app

# ============================================================
# GhostRights — App Configuration
# Works on: Streamlit Cloud (st.secrets) + Hostinger VPS (os.getenv)
# ============================================================

import os

try:
    import streamlit as st
    def _get(key, default=""):
        """Get secret from Streamlit Cloud first, then environment."""
        try:
            return st.secrets[key]
        except Exception:
            return os.getenv(key, default)
except Exception:
    def _get(key, default=""):
        return os.getenv(key, default)

# --- App Info ---
APP_NAME    = "GhostRights"
APP_TAGLINE = "Your content was stolen. GhostRights takes it back."
APP_VERSION = "1.0.0"
APP_ENV     = _get("APP_ENV", "development")
DEBUG       = _get("DEBUG", "True") == "True"

# --- Supabase ---
SUPABASE_URL         = _get("SUPABASE_URL")
SUPABASE_ANON_KEY    = _get("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = _get("SUPABASE_SERVICE_KEY")

# --- Paystack ---
PAYSTACK_SECRET_KEY  = _get("PAYSTACK_SECRET_KEY")
PAYSTACK_PUBLIC_KEY  = _get("PAYSTACK_PUBLIC_KEY")
PAYSTACK_BASE_URL    = "https://api.paystack.co"

# --- Twilio ---
TWILIO_ACCOUNT_SID   = _get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN    = _get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = _get("TWILIO_WHATSAPP_FROM",
                             "whatsapp:+14155238886")

# --- Email ---
SMTP_HOST      = _get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT      = int(_get("SMTP_PORT", "587"))
SMTP_USERNAME  = _get("SMTP_USERNAME")
SMTP_PASSWORD  = _get("SMTP_PASSWORD")
EMAIL_FROM     = _get("EMAIL_FROM", "noreply@ghostrights.com")
EMAIL_FROM_NAME = _get("EMAIL_FROM_NAME", "GhostRights")

# --- Gemini AI ---
GEMINI_API_KEY = _get("GEMINI_API_KEY")

# --- YouTube ---
YOUTUBE_API_KEY = _get("YOUTUBE_API_KEY")

# --- Google Search ---
GOOGLE_SEARCH_API_KEY = _get("GOOGLE_SEARCH_API_KEY")
GOOGLE_SEARCH_ENGINE_ID = _get("GOOGLE_SEARCH_ENGINE_ID")

# --- Facebook ---
FACEBOOK_APP_ID      = _get("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET  = _get("FACEBOOK_APP_SECRET")
FACEBOOK_ACCESS_TOKEN = _get("FACEBOOK_ACCESS_TOKEN")

# --- Business Rules ---
COMMISSION_RATE      = float(_get("COMMISSION_RATE", "0.20"))
TAKEDOWN_FEE_NGN     = int(_get("TAKEDOWN_FEE_NGN", "1500"))
INTELLIGENCE_REPORT_FEE_NGN = int(
    _get("INTELLIGENCE_REPORT_FEE_NGN", "35000")
)
MIN_MATCH_CONFIDENCE     = int(_get("MIN_MATCH_CONFIDENCE", "85"))
CRAWLER_INTERVAL_MINUTES = int(
    _get("CRAWLER_INTERVAL_MINUTES", "60")
)

# --- Subscription Plan Prices (in Naira) ---
PLAN_PRICES = {
    "starter": 8000,
    "pro":     20000,
    "studio":  75000,
}

# --- Storage Buckets ---
BUCKET_CONTENT      = _get("STORAGE_BUCKET_CONTENT", "gr-content")
BUCKET_WATERMARKED  = _get("STORAGE_BUCKET_WATERMARKED",
                            "gr-watermarked")
BUCKET_REPORTS      = _get("STORAGE_BUCKET_REPORTS", "gr-reports")
BUCKET_SCREENSHOTS  = _get("STORAGE_BUCKET_SCREENSHOTS",
                            "gr-screenshots")

# --- Platforms Monitored ---
MONITORED_PLATFORMS = [
    "youtube", "facebook", "instagram",
    "tiktok", "telegram", "twitter",
    "dailymotion", "vimeo", "blogs", "torrents",
]

# --- Supported File Formats ---
SUPPORTED_VIDEO_FORMATS = [".mp4", ".avi", ".mov",
                            ".mkv", ".wmv"]
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".aac",
                            ".flac", ".ogg", ".m4a"]
SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg",
                            ".png", ".webp"]
MAX_UPLOAD_SIZE_MB = 500

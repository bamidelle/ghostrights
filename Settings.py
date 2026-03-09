# ============================================================
# GhostRights — App Configuration
# ============================================================

import os
from dotenv import load_dotenv

load_dotenv()

# --- App Info ---
APP_NAME = "GhostRights"
APP_TAGLINE = "Your content was stolen. GhostRights takes it back."
APP_VERSION = "1.0.0"
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "True") == "True"

# --- Supabase ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# --- Paystack ---
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
PAYSTACK_PUBLIC_KEY = os.getenv("PAYSTACK_PUBLIC_KEY")
PAYSTACK_BASE_URL = "https://api.paystack.co"

# --- Twilio ---
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

# --- Email ---
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@ghostrights.com")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "GhostRights")

# --- Gemini AI ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- YouTube ---
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# --- Google Search ---
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

# --- Facebook ---
FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")

# --- Business Rules ---
COMMISSION_RATE = float(os.getenv("COMMISSION_RATE", 0.20))
TAKEDOWN_FEE_NGN = int(os.getenv("TAKEDOWN_FEE_NGN", 1500))
INTELLIGENCE_REPORT_FEE_NGN = int(os.getenv("INTELLIGENCE_REPORT_FEE_NGN", 35000))
MIN_MATCH_CONFIDENCE = int(os.getenv("MIN_MATCH_CONFIDENCE", 85))
CRAWLER_INTERVAL_MINUTES = int(os.getenv("CRAWLER_INTERVAL_MINUTES", 60))

# --- Subscription Plan Prices (in Naira) ---
PLAN_PRICES = {
    "starter": 8000,
    "pro": 20000,
    "studio": 75000,
}

# --- Storage Buckets ---
BUCKET_CONTENT = os.getenv("STORAGE_BUCKET_CONTENT", "gr-content")
BUCKET_WATERMARKED = os.getenv("STORAGE_BUCKET_WATERMARKED", "gr-watermarked")
BUCKET_REPORTS = os.getenv("STORAGE_BUCKET_REPORTS", "gr-reports")
BUCKET_SCREENSHOTS = os.getenv("STORAGE_BUCKET_SCREENSHOTS", "gr-screenshots")

# --- Platforms Monitored ---
MONITORED_PLATFORMS = [
    "youtube",
    "facebook",
    "instagram",
    "tiktok",
    "telegram",
    "twitter",
    "dailymotion",
    "vimeo",
    "blogs",
    "torrents",
]

# --- Supported Content Types ---
SUPPORTED_VIDEO_FORMATS = [".mp4", ".avi", ".mov", ".mkv", ".wmv"]
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"]
SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".webp"]

MAX_UPLOAD_SIZE_MB = 500

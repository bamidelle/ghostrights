"""
GhostRights — Demo Data Seeder
================================
Run this ONCE in Supabase SQL Editor or as a Python script
to populate realistic demo data for testing/demos.

Usage (local):
    python seed_demo_data.py

Or paste the SQL version into Supabase SQL Editor.

WARNING: Only run on a test account. Adds fake detections,
content, and notifications tied to a real creator_id.
"""

import sys
import os
import random
from datetime import datetime, timedelta

# ── Config ────────────────────────────────────────────────────
# Set these before running
CREATOR_ID    = "PASTE-YOUR-SUPABASE-USER-ID-HERE"
CREATOR_NAME  = "Emeka Okafor"
CREATOR_EMAIL = "emeka@example.com"


def _get_supabase():
    try:
        import streamlit as st
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_SERVICE_KEY"]
    except Exception:
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_SERVICE_KEY", "")
    from supabase import create_client
    return create_client(url, key)


# ── Sample data ───────────────────────────────────────────────

CONTENT_ITEMS = [
    {"title": "Living In Bondage: Breaking Free",
     "content_type": "movie",
     "description": "Nollywood sequel thriller",
     "duration_seconds": 6840},
    {"title": "Essence (Afrobeats Remix)",
     "content_type": "music",
     "description": "Studio single",
     "duration_seconds": 214},
    {"title": "How I Built a ₦50M Business From Lagos",
     "content_type": "video",
     "description": "YouTube documentary",
     "duration_seconds": 3120},
    {"title": "The Lagos Hustle Podcast — Ep. 47",
     "content_type": "audio",
     "description": "Business podcast episode",
     "duration_seconds": 2880},
    {"title": "Jenifa's Diary Season 8",
     "content_type": "movie",
     "description": "Comedy drama series",
     "duration_seconds": 5400},
    {"title": "Soro Soke (Protest Anthem)",
     "content_type": "music",
     "description": "Afrobeats protest song",
     "duration_seconds": 198},
]

PLATFORMS = ["youtube","facebook","telegram",
             "tiktok","instagram","blog","torrent"]

PLATFORM_URLS = {
    "youtube":   "https://youtube.com/watch?v=",
    "facebook":  "https://fb.watch/",
    "telegram":  "https://t.me/nollywoodleaks/",
    "tiktok":    "https://tiktok.com/@pirate/video/",
    "instagram": "https://instagram.com/reel/",
    "blog":      "https://naijamoviesdump.blogspot.com/",
    "torrent":   "https://1337x.to/torrent/",
}

PIRACY_TITLES = [
    "FULL MOVIE FREE DOWNLOAD 2024 HD",
    "Watch Free Online — No Subscription",
    "Leaked Version — Share Before Deleted",
    "Download MP3 Free — Latest 2024",
    "FULL ALBUM FREE DOWNLOAD",
    "Nollywood Movie Free Stream",
    "Latest Afrobeats Mix Free",
    "Watch Without Netflix — Free Link",
    "{title} — Free Download Link",
    "Download {title} HD Quality",
]

STATUSES   = ["new","new","new","takedown_requested",
               "monetized","dismissed"]
NOTIF_TYPES = [
    ("piracy_detected",  "🚨 New piracy detected",
     "A pirated copy was found on {platform}. "
     "~{views:,} views."),
    ("dmca_sent",        "⚔️ DMCA notice sent",
     "Legal notice filed for {content} on {platform}."),
    ("weekly_digest",    "📊 Weekly digest ready",
     "{count} new detections this week. "
     "₦{rev:,} estimated revenue lost."),
    ("payment_received", "💳 Payment confirmed",
     "Your Starter plan is now active."),
]


def seed(supabase, creator_id):
    print(f"\n🌱 Seeding demo data for creator: {creator_id}\n")

    # ── 1. Protected content ──────────────────────────────────
    print("📁 Creating content items...")
    content_ids = []
    for item in CONTENT_ITEMS:
        try:
            resp = supabase.table("protected_content").insert({
                "creator_id":        creator_id,
                "title":             item["title"],
                "content_type":      item["content_type"],
                "description":       item["description"],
                "duration_seconds":  item["duration_seconds"],
                "fingerprint_hash":  f"sha256_demo_{random.randint(100000,999999)}",
                "watermark_id":      f"WM-{random.randint(10000,99999)}",
                "status":            "active",
                "file_size_bytes":   random.randint(50_000_000, 4_000_000_000),
                "crawl_status":      "completed",
                "created_at":        (
                    datetime.now() - timedelta(
                        days=random.randint(5, 60)
                    )
                ).isoformat(),
            }).execute()
            content_ids.append(resp.data[0]["id"])
            print(f"  ✅ {item['title']}")
        except Exception as e:
            print(f"  ⚠️  {item['title']}: {e}")

    if not content_ids:
        print("❌ No content created — check creator_id")
        return

    # ── 2. Detections ─────────────────────────────────────────
    print(f"\n🚨 Creating detections...")
    detection_ids = []
    num_detections = 28

    for i in range(num_detections):
        content_id = random.choice(content_ids)
        platform   = random.choice(PLATFORMS)
        base_url   = PLATFORM_URLS.get(platform, "https://pirate.example.com/")
        rand_id    = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz0123456789",
                           k=11)
        )
        ptitle_tpl = random.choice(PIRACY_TITLES)

        # Find content title
        cont_title = "Your Content"
        for item in CONTENT_ITEMS:
            pass  # will use index below

        status     = random.choice(STATUSES)
        views      = random.randint(3_000, 850_000)
        conf       = random.uniform(82.0, 99.5)
        days_ago   = random.randint(0, 30)
        detected   = datetime.now() - timedelta(days=days_ago)

        try:
            resp = supabase.table("detections").insert({
                "creator_id":         creator_id,
                "content_id":         content_id,
                "platform":           platform,
                "pirated_url":        base_url + rand_id,
                "pirated_page_title": ptitle_tpl.replace(
                    "{title}", "Content"
                ),
                "estimated_views":    views,
                "match_confidence":   round(conf, 1),
                "status":             status,
                "first_detected_at":  detected.isoformat(),
                "last_seen_at":       detected.isoformat(),
                "fingerprint_type":   random.choice(
                    ["phash","chromaprint","sha256"]
                ),
                "revenue_estimate":   round(views * 0.003 * 430),
            }).execute()
            detection_ids.append(resp.data[0]["id"])
        except Exception as e:
            print(f"  ⚠️  Detection {i+1}: {e}")

    print(f"  ✅ {len(detection_ids)} detections created")

    # ── 3. Takedowns ─────────────────────────────────────────
    print(f"\n⚔️  Creating takedown records...")
    dmca_dets = [d for d in detection_ids][:6]
    PLATFORM_CONTACTS = {
        "youtube":   "copyright@youtube.com",
        "facebook":  "ip@fb.com",
        "telegram":  "dmca@telegram.org",
        "tiktok":    "copyright@tiktok.com",
        "instagram": "ip@fb.com",
        "blog":      "dmca@google.com",
        "torrent":   "abuse@cloudflare.com",
    }
    for det_id in dmca_dets[:4]:
        plat = random.choice(PLATFORMS)
        ref  = f"GR-DMCA-{random.randint(100000,999999)}"
        try:
            supabase.table("takedowns").insert({
                "creator_id":        creator_id,
                "detection_id":      det_id,
                "platform":          plat,
                "platform_contact":  PLATFORM_CONTACTS.get(
                    plat,"abuse@platform.com"
                ),
                "reference_number":  ref,
                "status":            random.choice(
                    ["sent","acknowledged","resolved"]
                ),
                "sent_at":  (
                    datetime.now() - timedelta(
                        days=random.randint(1,10)
                    )
                ).isoformat(),
                "notice_text": (
                    f"DMCA Notice — Reference {ref}. "
                    f"Infringement detected on {plat.title()}."
                ),
            }).execute()
        except Exception as e:
            print(f"  ⚠️  Takedown: {e}")
    print("  ✅ 4 takedown records created")

    # ── 4. Notifications ──────────────────────────────────────
    print(f"\n🔔 Creating notifications...")
    notif_data = [
        ("piracy_detected",
         "🚨 Piracy detected: Living In Bondage",
         "Found on YouTube with ~142,000 views. Act now.",
         False, 0),
        ("piracy_detected",
         "🚨 Piracy detected: Essence Remix",
         "Stolen copy on Telegram — 28,400 plays.",
         False, 1),
        ("dmca_sent",
         "⚔️ DMCA sent for Jenifa's Diary",
         "Notice filed with Facebook. Ref: GR-DMCA-881234.",
         False, 2),
        ("piracy_detected",
         "🚨 3 new pirated copies found",
         "TikTok (2) and a blog detected this week.",
         True,  3),
        ("weekly_digest",
         "📊 Weekly digest — 11 new detections",
         "₦2.1M estimated revenue lost this week.",
         True,  5),
        ("payment_received",
         "💳 Starter plan activated",
         "₦8,000 received. Your content is now protected 24/7.",
         True,  14),
    ]
    for ntype, title, msg, is_read, days_ago in notif_data:
        try:
            supabase.table("notifications").insert({
                "creator_id":        creator_id,
                "notification_type": ntype,
                "title":             title,
                "message":           msg,
                "is_read":           is_read,
                "send_dashboard":    True,
                "created_at": (
                    datetime.now() - timedelta(days=days_ago)
                ).isoformat(),
            }).execute()
        except Exception as e:
            print(f"  ⚠️  Notification: {e}")
    print("  ✅ 6 notifications created")

    # ── 5. Intelligence reports ───────────────────────────────
    print(f"\n📊 Creating report records...")
    try:
        supabase.table("intelligence_reports").insert({
            "creator_id":      creator_id,
            "detection_count": len(detection_ids),
            "status":          "generated",
            "created_at": (
                datetime.now() - timedelta(days=7)
            ).isoformat(),
        }).execute()
        print("  ✅ 1 report record created")
    except Exception as e:
        print(f"  ⚠️  Report: {e}")

    # ── 6. Alert preferences ─────────────────────────────────
    print(f"\n⚙️  Setting alert preferences...")
    try:
        supabase.table("alert_preferences").upsert({
            "creator_id":       creator_id,
            "wa_piracy":        True,
            "wa_dmca":          True,
            "wa_payment":       True,
            "wa_digest":        True,
            "em_piracy":        True,
            "em_dmca":          True,
            "em_payment":       True,
            "em_digest":        True,
            "whatsapp_alerts":  True,
            "email_alerts":     True,
            "whatsapp_digest":  True,
            "email_digest":     True,
        }).execute()
        print("  ✅ Alert preferences set")
    except Exception as e:
        print(f"  ⚠️  Alert prefs: {e}")

    # ── Summary ───────────────────────────────────────────────
    total_views = sum(random.randint(3000,850000)
                      for _ in range(len(detection_ids)))
    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ DEMO SEED COMPLETE

  Content items:   {len(content_ids)}
  Detections:      {len(detection_ids)}
  Takedowns:       4
  Notifications:   6
  Reports:         1

Your dashboard is now populated!
Log in at ghostrights.streamlit.app
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


if __name__ == "__main__":
    if CREATOR_ID == "PASTE-YOUR-SUPABASE-USER-ID-HERE":
        print("❌ Edit CREATOR_ID at the top of this file first.")
        print("   Find it in Supabase → Authentication → Users")
        sys.exit(1)
    supabase = _get_supabase()
    seed(supabase, CREATOR_ID)

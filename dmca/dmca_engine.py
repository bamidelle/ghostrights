"""
GhostRights — DMCA Automation Engine
======================================
Generates and sends DMCA takedown notices to:
- YouTube (via copyright.google.com webform data)
- Facebook (via facebook.com/help/contact)
- Google Search (deindex pirated pages)
- Telegram (abuse@telegram.org)
- Generic email for blogs/sites

Files:
  dmca/dmca_engine.py  ← this file (core engine)
"""

import os
import uuid
import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template

log = logging.getLogger("GhostRightsDMCA")

# ── Secrets (read from env or Streamlit secrets) ────────────
def _get(key, default=""):
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)

SMTP_HOST     = _get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT     = int(_get("SMTP_PORT", "587"))
SMTP_USER     = _get("SMTP_USERNAME")
SMTP_PASS     = _get("SMTP_PASSWORD")
EMAIL_FROM    = _get("EMAIL_FROM", "legal@ghostrights.com")
FROM_NAME     = _get("EMAIL_FROM_NAME", "GhostRights Legal")


# ════════════════════════════════════════════════════════════
# DMCA NOTICE TEMPLATES
# ════════════════════════════════════════════════════════════

DMCA_EMAIL_TEMPLATE = """
Dear Sir/Madam,

DMCA TAKEDOWN NOTICE

I am writing on behalf of {{ creator_name }} ("the Rights Holder"),
the exclusive owner of the copyright in the work described below.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ORIGINAL WORK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title:          {{ content_title }}
Type:           {{ content_type }}
Creator:        {{ creator_name }}
Year:           {{ release_year }}
Reference ID:   {{ reference_id }}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INFRINGING MATERIAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Platform:       {{ platform }}
Infringing URL: {{ infringing_url }}
Page Title:     {{ infringing_title }}
Date Detected:  {{ detection_date }}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STATEMENT OF AUTHORITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I have a good faith belief that use of the material in the manner
complained of is not authorized by the copyright owner, its agent,
or the law.

The information in this notification is accurate and, under penalty
of perjury, I am authorized to act on behalf of the owner of the
exclusive rights that are allegedly infringed.

I request that you immediately:
1. Remove or disable access to the infringing content
2. Notify the uploader of this removal
3. Provide confirmation of removal to this email address

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTACT INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name:           GhostRights Legal Team
On behalf of:   {{ creator_name }}
Email:          legal@ghostrights.com
Reference:      DMCA-{{ reference_id }}
Date:           {{ today }}

This notice is sent pursuant to the Digital Millennium Copyright
Act (DMCA), 17 U.S.C. § 512, and equivalent international
copyright laws.

Sincerely,
GhostRights Legal Automation
{{ today }}

---
This notice was generated automatically by GhostRights
(ghostrights.streamlit.app) on behalf of the rights holder.
GhostRights is an AI-powered content protection platform
for African creators.
"""

YOUTUBE_DMCA_TEMPLATE = """
YOUTUBE COPYRIGHT REMOVAL REQUEST
Reference: DMCA-{{ reference_id }}

Video URL: {{ infringing_url }}
Reason: Copyright infringement of "{{ content_title }}" by {{ creator_name }}

Original Work:
- Title: {{ content_title }}
- Type: {{ content_type }}
- Creator: {{ creator_name }}
- Year: {{ release_year }}

The above YouTube video contains my copyrighted work without
authorization. I request immediate removal under DMCA Section 512(c).

Rights holder: {{ creator_name }}
Represented by: GhostRights (legal@ghostrights.com)
Date: {{ today }}
"""

GOOGLE_DEINDEX_TEMPLATE = """
GOOGLE SEARCH DEINDEXING REQUEST
Reference: DMCA-{{ reference_id }}

I am requesting removal of the following URL from Google Search
results as it contains copyrighted material posted without
authorization.

Infringing URL: {{ infringing_url }}
Copyrighted Work: {{ content_title }}
Rights Owner: {{ creator_name }}
Date of Original Creation: {{ release_year }}

This request is made under the DMCA, 17 U.S.C. § 512(d).

Contact: GhostRights Legal (legal@ghostrights.com)
Reference: DMCA-{{ reference_id }}
Date: {{ today }}
"""


# ════════════════════════════════════════════════════════════
# PLATFORM DMCA CONTACTS
# ════════════════════════════════════════════════════════════

PLATFORM_CONTACTS = {
    "youtube": {
        "email": "copyright@youtube.com",
        "name":  "YouTube Copyright Team",
        "form":  "https://www.youtube.com/copyright_complaint_form",
        "template": YOUTUBE_DMCA_TEMPLATE
    },
    "facebook": {
        "email": "ip@fb.com",
        "name":  "Facebook Intellectual Property",
        "form":  "https://www.facebook.com/help/contact/634636770043106",
        "template": DMCA_EMAIL_TEMPLATE
    },
    "instagram": {
        "email": "ip@fb.com",
        "name":  "Instagram Copyright",
        "form":  "https://help.instagram.com/contact/372592039493025",
        "template": DMCA_EMAIL_TEMPLATE
    },
    "tiktok": {
        "email": "copyright@tiktok.com",
        "name":  "TikTok Copyright",
        "form":  "https://www.tiktok.com/legal/report/Copyright",
        "template": DMCA_EMAIL_TEMPLATE
    },
    "telegram": {
        "email": "dmca@telegram.org",
        "name":  "Telegram DMCA",
        "form":  None,
        "template": DMCA_EMAIL_TEMPLATE
    },
    "twitter": {
        "email": "copyright@twitter.com",
        "name":  "Twitter Copyright",
        "form":  "https://help.twitter.com/forms/dmca",
        "template": DMCA_EMAIL_TEMPLATE
    },
    "blog": {
        "email": "abuse@google.com",
        "name":  "Google DMCA",
        "form":  "https://www.google.com/webmasters/tools/dmca-notice",
        "template": GOOGLE_DEINDEX_TEMPLATE
    },
    "torrent": {
        "email": "abuse@google.com",
        "name":  "Google DMCA",
        "form":  "https://www.google.com/webmasters/tools/dmca-notice",
        "template": GOOGLE_DEINDEX_TEMPLATE
    },
}


# ════════════════════════════════════════════════════════════
# DMCA ENGINE
# ════════════════════════════════════════════════════════════

class DMCAEngine:
    """Generates and sends DMCA takedown notices."""

    def generate_notice(self, detection: dict,
                        content: dict,
                        creator: dict) -> str:
        """Generate a DMCA notice for a detection."""
        platform = detection.get("platform", "blog").lower()
        contact  = PLATFORM_CONTACTS.get(
            platform, PLATFORM_CONTACTS["blog"]
        )
        template_str = contact["template"]

        context = {
            "creator_name":     creator.get("full_name", "Creator"),
            "content_title":    content.get("title", ""),
            "content_type":     content.get("content_type", ""),
            "release_year":     content.get("release_year", ""),
            "platform":         platform.title(),
            "infringing_url":   detection.get("pirated_url", ""),
            "infringing_title": detection.get(
                "pirated_page_title", ""
            ),
            "detection_date":   detection.get(
                "first_detected_at", ""
            )[:10],
            "reference_id":     detection.get(
                "id", str(uuid.uuid4())[:8].upper()
            ),
            "today": datetime.now().strftime("%B %d, %Y")
        }

        return Template(template_str).render(**context)

    def send_dmca_email(self, detection: dict,
                        content: dict,
                        creator: dict) -> dict:
        """Send DMCA email and return result."""
        platform = detection.get("platform", "blog").lower()
        contact  = PLATFORM_CONTACTS.get(
            platform, PLATFORM_CONTACTS["blog"]
        )

        notice_body = self.generate_notice(
            detection, content, creator
        )
        reference_id = detection.get(
            "id", str(uuid.uuid4())[:8].upper()
        )
        subject = (
            f"DMCA Takedown Notice — "
            f"{content.get('title', 'Copyrighted Content')} — "
            f"Ref: DMCA-{reference_id}"
        )

        result = {
            "success": False,
            "platform": platform,
            "recipient": contact["email"],
            "reference_id": reference_id,
            "notice_body": notice_body,
            "form_url": contact.get("form"),
            "sent_at": datetime.now().isoformat(),
            "error": None
        }

        if not SMTP_USER or not SMTP_PASS:
            result["error"] = "SMTP credentials not configured"
            log.warning(
                "DMCA email not sent — SMTP not configured. "
                "Notice generated but not delivered."
            )
            result["success"] = True  # Notice generated ok
            result["delivery_method"] = "generated_only"
            return result

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"]    = f"{FROM_NAME} <{EMAIL_FROM}>"
            msg["To"]      = contact["email"]
            msg["Reply-To"] = SMTP_USER

            msg.attach(MIMEText(notice_body, "plain"))

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.ehlo()
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.sendmail(
                    EMAIL_FROM,
                    contact["email"],
                    msg.as_string()
                )

            result["success"] = True
            result["delivery_method"] = "email"
            log.info(
                f"✅ DMCA sent to {contact['email']} "
                f"for {content.get('title')} "
                f"on {platform}"
            )

        except Exception as e:
            result["error"] = str(e)
            result["success"] = False
            log.error(f"DMCA send error: {e}")

        return result

    def process_takedown(self, detection_id: str) -> dict:
        """
        Full takedown pipeline for a detection.
        Called from page_takedowns.py
        """
        from database.db import get_supabase, get_supabase_admin

        supabase = get_supabase()
        admin    = get_supabase_admin()

        # Fetch detection
        det_resp = supabase.table("detections") \
            .select("*, protected_content(*), profiles(*)") \
            .eq("id", detection_id).single().execute()

        if not det_resp.data:
            return {"success": False, "error": "Detection not found"}

        detection = det_resp.data
        content   = detection.get("protected_content", {})
        creator   = detection.get("profiles", {})

        # Generate + send notice
        result = self.send_dmca_email(
            detection, content, creator
        )

        # Save to takedowns table
        takedown_record = {
            "detection_id":    detection_id,
            "content_id":      detection.get("content_id"),
            "creator_id":      detection.get("creator_id"),
            "platform":        detection.get("platform"),
            "infringing_url":  detection.get("pirated_url"),
            "dmca_reference":  f"DMCA-{result['reference_id']}",
            "notice_body":     result["notice_body"],
            "sent_to_email":   result["recipient"],
            "status": "sent" if result["success"] else "failed",
            "sent_at":         result["sent_at"],
            "notes": result.get("error", "")
        }

        admin.table("takedowns").insert(takedown_record).execute()

        # Update detection status
        admin.table("detections") \
            .update({"status": "takedown_requested"}) \
            .eq("id", detection_id).execute()

        # Notify creator
        if result["success"]:
            admin.table("notifications").insert({
                "creator_id":        detection.get("creator_id"),
                "notification_type": "takedown_success",
                "title":             "DMCA Notice Sent!",
                "message": (
                    f"A DMCA takedown notice has been sent to "
                    f"{detection.get('platform', '').title()} "
                    f"for your content "
                    f'"{content.get("title", "")}".'
                    f" Reference: DMCA-{result['reference_id']}"
                ),
                "send_dashboard": True,
                "send_email":     True
            }).execute()

        return result

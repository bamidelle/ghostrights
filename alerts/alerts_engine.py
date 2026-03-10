"""
GhostRights — Alerts Engine (Step 10)
=======================================
Sends WhatsApp alerts via Twilio
Sends email alerts via SMTP (Gmail)

Triggers:
- New piracy detection found
- DMCA notice sent successfully
- Payment received / plan activated
- Weekly digest summary
"""

import os
import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

log = logging.getLogger("GhostRightsAlerts")


# ── Secrets ──────────────────────────────────────────────────
def _get(key, default=""):
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)

SMTP_HOST   = _get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT   = int(_get("SMTP_PORT", "587"))
SMTP_USER   = _get("SMTP_USERNAME")
SMTP_PASS   = _get("SMTP_PASSWORD")
FROM_EMAIL  = _get("EMAIL_FROM", "alerts@ghostrights.com")
FROM_NAME   = "GhostRights"

TWILIO_SID   = _get("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = _get("TWILIO_AUTH_TOKEN")
TWILIO_FROM  = _get("TWILIO_WHATSAPP_FROM",
                     "whatsapp:+14155238886")  # Twilio sandbox


# ════════════════════════════════════════════════════════════
# EMAIL TEMPLATES
# ════════════════════════════════════════════════════════════

def _email_html(title, subtitle, body_html,
                cta_text=None, cta_url=None):
    """Branded HTML email wrapper."""
    cta_block = ""
    if cta_text and cta_url:
        cta_block = f"""
        <div style="text-align:center;margin:32px 0;">
          <a href="{cta_url}"
             style="display:inline-block;
                    background:#111111;color:#ffffff;
                    font-family:'Helvetica Neue',sans-serif;
                    font-size:15px;font-weight:700;
                    padding:14px 32px;border-radius:100px;
                    text-decoration:none;letter-spacing:-0.2px;">
            {cta_text} →
          </a>
        </div>"""

    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width">
</head>
<body style="margin:0;padding:0;
             background:#F0EDE8;
             font-family:'Helvetica Neue',Arial,sans-serif;">

  <!-- Header -->
  <div style="background:#111111;padding:20px 40px;">
    <span style="font-size:16px;font-weight:900;
                 color:#ffffff;letter-spacing:-0.3px;">
      👻 GhostRights
    </span>
  </div>

  <!-- Card -->
  <div style="max-width:560px;margin:32px auto;
              background:#ffffff;border-radius:20px;
              overflow:hidden;
              box-shadow:0 4px 24px rgba(0,0,0,0.07);
              border:1px solid #E8E4DE;">

    <!-- Title band -->
    <div style="padding:32px 40px 24px;">
      <div style="font-size:11px;font-weight:800;
                  letter-spacing:1.2px;text-transform:uppercase;
                  color:#E8463A;margin-bottom:10px;">
        GhostRights Alert
      </div>
      <div style="font-size:24px;font-weight:900;
                  letter-spacing:-0.5px;color:#111111;
                  line-height:1.15;margin-bottom:6px;">
        {title}
      </div>
      <div style="font-size:14px;color:#6B6B6B;
                  font-weight:500;line-height:1.6;">
        {subtitle}
      </div>
    </div>

    <!-- Divider -->
    <div style="height:1px;background:#E8E4DE;
                margin:0 40px;"></div>

    <!-- Body -->
    <div style="padding:24px 40px 32px;">
      {body_html}
      {cta_block}
    </div>
  </div>

  <!-- Footer -->
  <div style="max-width:560px;margin:0 auto;
              padding:20px 40px;text-align:center;
              font-size:12px;color:#9B9B9B;">
    GhostRights — AI-powered content protection for African creators
    <br>
    <a href="https://ghostrights.streamlit.app"
       style="color:#9B9B9B;">
      ghostrights.streamlit.app
    </a>
  </div>

</body>
</html>"""


def _stat_box(num, label, color="#111111"):
    return f"""
    <div style="background:#F0EDE8;border-radius:12px;
         padding:20px;text-align:center;flex:1;">
      <div style="font-size:36px;font-weight:900;
           color:{color};letter-spacing:-1px;
           font-family:'Helvetica Neue',sans-serif;
           line-height:1;">{num}</div>
      <div style="font-size:11px;color:#9B9B9B;
           font-weight:600;margin-top:4px;
           text-transform:uppercase;
           letter-spacing:0.5px;">{label}</div>
    </div>"""


# ════════════════════════════════════════════════════════════
# WHATSAPP SENDER
# ════════════════════════════════════════════════════════════

class WhatsAppSender:

    def send(self, to_phone: str, message: str) -> dict:
        """
        Send WhatsApp message via Twilio.
        to_phone: '2348012345678' (no +, no spaces)
        """
        if not TWILIO_SID or not TWILIO_TOKEN:
            log.warning("Twilio not configured — WA not sent")
            return {"success": False,
                    "error": "Twilio not configured"}

        # Ensure E.164 format
        phone = to_phone.strip().replace(" ", "").replace("-","")
        if not phone.startswith("+"):
            phone = "+" + phone

        try:
            from twilio.rest import Client
            client  = Client(TWILIO_SID, TWILIO_TOKEN)
            msg     = client.messages.create(
                from_=TWILIO_FROM,
                to=f"whatsapp:{phone}",
                body=message
            )
            log.info(f"WhatsApp sent to {phone}: {msg.sid}")
            return {"success": True, "sid": msg.sid}
        except Exception as e:
            log.error(f"WhatsApp error: {e}")
            return {"success": False, "error": str(e)}


# ════════════════════════════════════════════════════════════
# EMAIL SENDER
# ════════════════════════════════════════════════════════════

class EmailSender:

    def send(self, to_email: str, subject: str,
             html_body: str, plain_body: str = "") -> dict:
        """Send HTML email via SMTP."""
        if not SMTP_USER or not SMTP_PASS:
            log.warning("SMTP not configured — email not sent")
            return {"success": False,
                    "error": "SMTP not configured"}
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"]    = f"{FROM_NAME} <{FROM_EMAIL}>"
            msg["To"]      = to_email

            if plain_body:
                msg.attach(MIMEText(plain_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as srv:
                srv.ehlo()
                srv.starttls()
                srv.login(SMTP_USER, SMTP_PASS)
                srv.sendmail(FROM_EMAIL, to_email,
                             msg.as_string())

            log.info(f"Email sent to {to_email}: {subject}")
            return {"success": True}
        except Exception as e:
            log.error(f"Email error: {e}")
            return {"success": False, "error": str(e)}


# ════════════════════════════════════════════════════════════
# ALERT ENGINE — high-level triggers
# ════════════════════════════════════════════════════════════

class AlertEngine:

    def __init__(self):
        self.wa    = WhatsAppSender()
        self.email = EmailSender()

    def _save_notification(self, creator_id, notif_type,
                            title, message,
                            email_sent=False,
                            wa_sent=False):
        """Save notification record to Supabase."""
        try:
            from database.db import get_supabase_admin
            get_supabase_admin().table("notifications").insert({
                "creator_id":        creator_id,
                "notification_type": notif_type,
                "title":             title,
                "message":           message,
                "send_dashboard":    True,
                "send_email":        email_sent,
                "send_whatsapp":     wa_sent,
                "is_read":           False,
                "created_at":        datetime.now().isoformat()
            }).execute()
        except Exception as e:
            log.error(f"Save notification error: {e}")

    # ── PIRACY DETECTION ALERT ────────────────────────────────
    def send_detection_alert(self, creator_id: str,
                              creator_name: str,
                              email: str,
                              phone: str,
                              content_title: str,
                              platform: str,
                              pirated_url: str,
                              estimated_views: int,
                              prefs: dict = None) -> dict:
        """Alert creator when new piracy is detected."""
        prefs = prefs or {}
        results = {"email": None, "whatsapp": None}
        platform_cap = platform.title()
        views_str = (f"{estimated_views:,}"
                     if estimated_views else "Unknown")
        short_url = pirated_url[:60] + "..." \
            if len(pirated_url) > 60 else pirated_url

        # ── WhatsApp ──────────────────────────────────────────
        if prefs.get("whatsapp_alerts", True) and phone:
            wa_msg = (
                f"🚨 *GhostRights Alert*\n\n"
                f"Piracy detected for *{content_title}*\n\n"
                f"📍 Platform: *{platform_cap}*\n"
                f"👁 Est. views: *{views_str}*\n"
                f"🔗 {short_url}\n\n"
                f"Log in to take action:\n"
                f"ghostrights.streamlit.app"
            )
            results["whatsapp"] = self.wa.send(phone, wa_msg)

        # ── Email ─────────────────────────────────────────────
        if prefs.get("email_alerts", True) and email:
            body_html = f"""
            <div style="display:flex;gap:12px;margin-bottom:24px;">
              {_stat_box(views_str, "Est. Stolen Views", "#E8463A")}
              {_stat_box(platform_cap, "Platform", "#111111")}
            </div>
            <p style="font-size:14px;color:#4A4A45;
                      line-height:1.65;margin:0 0 16px;">
              GhostRights has detected a pirated copy of
              <strong>{content_title}</strong> on
              <strong>{platform_cap}</strong>.
              Log in now to monetize it or send a DMCA notice.
            </p>
            <div style="background:#F0EDE8;border-radius:10px;
                 padding:14px 16px;margin-bottom:20px;">
              <div style="font-size:11px;font-weight:700;
                   color:#9B9B9B;text-transform:uppercase;
                   letter-spacing:1px;margin-bottom:4px;">
                Infringing URL
              </div>
              <div style="font-size:12px;color:#6B6B6B;
                   word-break:break-all;">
                {pirated_url}
              </div>
            </div>"""

            html = _email_html(
                title="Piracy Detected! 🚨",
                subtitle=(
                    f"A stolen copy of "
                    f'"{content_title}" was found on '
                    f"{platform_cap}"
                ),
                body_html=body_html,
                cta_text="Take Action Now",
                cta_url="https://ghostrights.streamlit.app"
            )
            results["email"] = self.email.send(
                to_email=email,
                subject=(
                    f"🚨 Piracy Alert: {content_title} "
                    f"found on {platform_cap}"
                ),
                html_body=html,
                plain_body=(
                    f"GhostRights Alert: Piracy detected!\n\n"
                    f"Content: {content_title}\n"
                    f"Platform: {platform_cap}\n"
                    f"Views: {views_str}\n"
                    f"URL: {pirated_url}\n\n"
                    f"Log in: ghostrights.streamlit.app"
                )
            )

        # Save to DB
        self._save_notification(
            creator_id=creator_id,
            notif_type="piracy_detected",
            title=f"Piracy detected: {content_title}",
            message=(
                f"Found on {platform_cap} with "
                f"~{views_str} views. "
                f"URL: {short_url}"
            ),
            email_sent=bool(results["email"] and
                            results["email"].get("success")),
            wa_sent=bool(results["whatsapp"] and
                         results["whatsapp"].get("success"))
        )
        return results

    # ── DMCA SUCCESS ALERT ────────────────────────────────────
    def send_dmca_alert(self, creator_id: str,
                         creator_name: str,
                         email: str,
                         phone: str,
                         content_title: str,
                         platform: str,
                         reference: str,
                         prefs: dict = None) -> dict:
        """Alert creator when DMCA notice was sent."""
        prefs = prefs or {}
        results = {}

        if prefs.get("whatsapp_alerts", True) and phone:
            wa_msg = (
                f"⚔️ *DMCA Notice Sent!*\n\n"
                f"We fired a legal takedown for "
                f"*{content_title}*\n\n"
                f"📍 Platform: *{platform.title()}*\n"
                f"📋 Reference: *{reference}*\n\n"
                f"Platforms typically respond within 72hrs.\n"
                f"ghostrights.streamlit.app"
            )
            results["whatsapp"] = self.wa.send(phone, wa_msg)

        if prefs.get("email_alerts", True) and email:
            body_html = f"""
            <div style="background:#D8F3DC;border-radius:12px;
                 padding:20px 24px;margin-bottom:24px;
                 border-left:4px solid #1B4332;">
              <div style="font-size:13px;font-weight:700;
                   color:#1B4332;margin-bottom:4px;">
                DMCA Notice Successfully Filed
              </div>
              <div style="font-size:12px;color:#2D6A4F;">
                Reference: <strong>{reference}</strong>
              </div>
            </div>
            <p style="font-size:14px;color:#4A4A45;
                      line-height:1.65;margin:0 0 16px;">
              A legal DMCA takedown notice has been filed for
              <strong>{content_title}</strong> on
              <strong>{platform.title()}</strong>.
              Most platforms respond within <strong>72 hours</strong>.
              We will notify you once the content is removed.
            </p>"""

            html = _email_html(
                title="DMCA Notice Sent ⚔️",
                subtitle=(
                    f"Legal action taken for "
                    f'"{content_title}" on {platform.title()}'
                ),
                body_html=body_html,
                cta_text="View Takedown Status",
                cta_url="https://ghostrights.streamlit.app"
            )
            results["email"] = self.email.send(
                to_email=email,
                subject=(
                    f"⚔️ DMCA Notice Sent — {content_title} "
                    f"({reference})"
                ),
                html_body=html
            )

        self._save_notification(
            creator_id=creator_id,
            notif_type="dmca_sent",
            title=f"DMCA sent for {content_title}",
            message=(
                f"Notice sent to {platform.title()}. "
                f"Ref: {reference}"
            ),
            email_sent=bool(
                results.get("email", {}).get("success")
            ),
            wa_sent=bool(
                results.get("whatsapp", {}).get("success")
            )
        )
        return results

    # ── PAYMENT SUCCESS ALERT ─────────────────────────────────
    def send_payment_alert(self, creator_id: str,
                            creator_name: str,
                            email: str,
                            phone: str,
                            plan_name: str,
                            amount_ngn: int,
                            prefs: dict = None) -> dict:
        """Alert creator when payment is confirmed."""
        prefs = prefs or {}
        results = {}

        if prefs.get("whatsapp_alerts", True) and phone:
            wa_msg = (
                f"✅ *Payment Confirmed!*\n\n"
                f"Your GhostRights *{plan_name} Plan* "
                f"is now active.\n\n"
                f"💰 Amount: *₦{amount_ngn:,}*\n"
                f"🛡 Status: *Active*\n\n"
                f"Your content is being protected 24/7.\n"
                f"ghostrights.streamlit.app"
            )
            results["whatsapp"] = self.wa.send(phone, wa_msg)

        if prefs.get("email_alerts", True) and email:
            body_html = f"""
            <div style="display:flex;gap:12px;margin-bottom:24px;">
              {_stat_box(f"₦{amount_ngn:,}", "Amount Paid",
                         "#1B4332")}
              {_stat_box(plan_name, "Plan", "#111111")}
              {_stat_box("Active", "Status", "#16A34A")}
            </div>
            <p style="font-size:14px;color:#4A4A45;
                      line-height:1.65;margin:0 0 16px;">
              Welcome to GhostRights {plan_name}!
              Your content is now being protected 24/7 across
              all monitored platforms. Our crawlers will alert
              you the moment any piracy is detected.
            </p>"""

            html = _email_html(
                title=f"You're on {plan_name}! ✅",
                subtitle=(
                    f"₦{amount_ngn:,} received — "
                    f"your plan is now active"
                ),
                body_html=body_html,
                cta_text="Go to Dashboard",
                cta_url="https://ghostrights.streamlit.app"
            )
            results["email"] = self.email.send(
                to_email=email,
                subject=(
                    f"✅ Payment confirmed — GhostRights "
                    f"{plan_name} is active"
                ),
                html_body=html
            )

        self._save_notification(
            creator_id=creator_id,
            notif_type="payment_received",
            title=f"Payment confirmed — {plan_name} active",
            message=f"₦{amount_ngn:,} received. Plan is active.",
            email_sent=bool(
                results.get("email", {}).get("success")
            ),
            wa_sent=bool(
                results.get("whatsapp", {}).get("success")
            )
        )
        return results

    # ── WEEKLY DIGEST ─────────────────────────────────────────
    def send_weekly_digest(self, creator_id: str,
                            creator_name: str,
                            email: str,
                            phone: str,
                            stats: dict,
                            prefs: dict = None) -> dict:
        """Weekly summary alert every Monday."""
        prefs  = prefs or {}
        results = {}

        new_dets   = stats.get("new_detections", 0)
        dmca_sent  = stats.get("dmca_sent", 0)
        rev_recov  = stats.get("revenue_recovered", 0)
        total_dets = stats.get("total_detections", 0)

        if prefs.get("whatsapp_digest", True) and phone:
            wa_msg = (
                f"📊 *GhostRights Weekly Report*\n\n"
                f"Here's your piracy summary, "
                f"{creator_name.split()[0]}:\n\n"
                f"🔴 New detections: *{new_dets}*\n"
                f"⚔️ DMCA notices sent: *{dmca_sent}*\n"
                f"💰 Revenue recovered: *₦{rev_recov:,}*\n"
                f"📋 Total pirated copies: *{total_dets}*\n\n"
                f"ghostrights.streamlit.app"
            )
            results["whatsapp"] = self.wa.send(phone, wa_msg)

        if prefs.get("email_digest", True) and email:
            body_html = f"""
            <p style="font-size:14px;color:#6B6B6B;
                      margin:0 0 20px;">
              Here is your GhostRights summary for the week
              ending {datetime.now().strftime('%B %d, %Y')}.
            </p>
            <div style="display:flex;gap:10px;
                        margin-bottom:24px;flex-wrap:wrap;">
              {_stat_box(str(new_dets),
                         "New Detections", "#E8463A")}
              {_stat_box(str(dmca_sent),
                         "DMCA Sent", "#111111")}
              {_stat_box(f"₦{rev_recov:,}",
                         "Recovered", "#1B4332")}
            </div>
            <p style="font-size:14px;color:#4A4A45;
                      line-height:1.65;margin:0;">
              Log in to review all detections and take action
              on any new piracy found this week.
            </p>"""

            html = _email_html(
                title=f"Your Weekly Report 📊",
                subtitle=(
                    f"{new_dets} new detections this week, "
                    f"{creator_name.split()[0]}"
                ),
                body_html=body_html,
                cta_text="View Full Report",
                cta_url="https://ghostrights.streamlit.app"
            )
            results["email"] = self.email.send(
                to_email=email,
                subject=(
                    f"📊 Weekly Piracy Report — "
                    f"{new_dets} new detections"
                ),
                html_body=html
            )

        self._save_notification(
            creator_id=creator_id,
            notif_type="weekly_digest",
            title=f"Weekly digest — {new_dets} new detections",
            message=(
                f"{dmca_sent} DMCA sent, "
                f"₦{rev_recov:,} recovered"
            ),
            email_sent=bool(
                results.get("email", {}).get("success")
            ),
            wa_sent=bool(
                results.get("whatsapp", {}).get("success")
            )
        )
        return results

    # ── TEST ALERT ────────────────────────────────────────────
    def send_test_alert(self, email: str,
                         phone: str) -> dict:
        """Send a test alert to verify config."""
        results = {}

        if phone:
            results["whatsapp"] = self.wa.send(
                phone,
                "✅ *GhostRights Test Alert*\n\n"
                "Your WhatsApp alerts are working! "
                "You will be notified here whenever "
                "piracy is detected for your content.\n\n"
                "ghostrights.streamlit.app"
            )

        if email:
            html = _email_html(
                title="Test Alert ✅",
                subtitle="Your GhostRights alerts are configured correctly",
                body_html="""
                <p style="font-size:14px;color:#4A4A45;
                          line-height:1.65;">
                  This is a test alert from GhostRights.
                  If you received this, your email alerts
                  are working correctly.
                  You will be notified here when:
                </p>
                <ul style="font-size:14px;color:#4A4A45;
                            line-height:2;
                            padding-left:20px;">
                  <li>New piracy is detected for your content</li>
                  <li>A DMCA notice is sent</li>
                  <li>A payment is confirmed</li>
                  <li>Your weekly digest is ready</li>
                </ul>""",
                cta_text="Go to Dashboard",
                cta_url="https://ghostrights.streamlit.app"
            )
            results["email"] = self.email.send(
                to_email=email,
                subject="✅ GhostRights Alerts — Test Successful",
                html_body=html
            )

        return results

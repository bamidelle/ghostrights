# 👻 GhostRights

> **AI-powered content protection and piracy monetization platform for African creators.**

GhostRights hunts stolen content across the internet 24/7 and either **makes it pay you** or **destroys it** — automatically.

---

## 🌍 Built For Africa. Ready For The World.

Nollywood, Afrobeats, African YouTube creators and podcasters lose **$2,000,000,000+** to piracy every year. GhostRights is the first platform built specifically to fix that.

---

## ⚡ Core Features

- 🔍 **Piracy Detection** — AI crawlers scan YouTube, Facebook, TikTok, Telegram, blogs & torrents 24/7
- 🎯 **Content Fingerprinting** — Video (pHash) + Audio (Chromaprint) fingerprinting survives cropping, compression & re-encoding
- 💧 **Invisible Watermarking** — Trace exactly who leaked your content
- 💰 **Monetization** — Claim ad revenue from pirated copies on YouTube & Facebook automatically
- ⚔️ **DMCA Takedowns** — Auto-generate and send takedown notices at scale
- 📊 **Piracy Intelligence Reports** — Full PDF report of everywhere your content lives illegally
- 📱 **WhatsApp Alerts** — Get notified the moment piracy is detected
- 🏢 **Multi-tier Plans** — Starter, Pro, Studio & Enterprise

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (Python) |
| Backend | Python |
| Database | Supabase (PostgreSQL) |
| Auth | Supabase Auth |
| Storage | Supabase Storage |
| Payments | Paystack |
| Video Fingerprint | OpenCV + ImageHash |
| Audio Fingerprint | Chromaprint + pyacoustid |
| Watermarking | OpenCV + PyWavelets |
| Crawler | Scrapy + Playwright |
| PDF Reports | ReportLab |
| Notifications | Twilio (WhatsApp) + SMTP |
| AI Insights | Google Gemini API |
| Hosting | Hostinger VPS |

---

## 📁 Project Structure

```
ghostrights/
├── app/                    # Streamlit frontend
│   ├── main.py             # App entry point
│   ├── pages/              # All page modules
│   └── components/         # Reusable UI components
├── crawler/                # Piracy detection crawlers
├── fingerprint/            # Video & audio fingerprinting
├── watermark/              # Invisible watermark engine
├── dmca/                   # DMCA notice automation
├── reports/                # PDF intelligence reports
├── notifications/          # Email & WhatsApp alerts
├── database/               # Supabase schema & helpers
├── config/                 # App configuration
├── tests/                  # Unit tests
└── assets/                 # Images, templates, logos
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOURUSERNAME/ghostrights.git
cd ghostrights
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
# Fill in your keys in .env
```

### 4. Set up database
```bash
# Run ghostrights_schema.sql in your Supabase SQL Editor
```

### 5. Run the app
```bash
streamlit run app/main.py
```

---

## 💰 Revenue Model

| Stream | How |
|---|---|
| Monthly Subscriptions | Starter ₦8k / Pro ₦20k / Studio ₦75k |
| Ad Revenue Commission | 20% of recovered ad revenue |
| Pay-Per-Takedown | ₦1,500 per successful takedown |
| Intelligence Reports | ₦35,000 one-time scan |
| Enterprise Licensing | ₦500k - ₦2M/month |

---

## 📜 License

Proprietary — All rights reserved © GhostRights 2026

---

## 👤 Author

Built with 🤍 for African creators.

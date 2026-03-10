"""
GhostRights — Cron Job Scheduler
==================================
Runs continuously on Hostinger VPS.
Triggers the crawler automatically every hour.

Start it:  python cron_runner.py
Keep alive: use screen or supervisor on VPS

Example VPS setup:
  screen -S ghostrights_cron
  python cron_runner.py
  Ctrl+A then D  (detach — keeps running)
"""

import time
import logging
import schedule
from datetime import datetime
from crawler.crawler import (
    run_pending_jobs,
    run_full_scan_for_all_creators
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [CRON] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("cron.log")
    ]
)
log = logging.getLogger("GhostRightsCron")


def job_pending():
    """Run pending crawler jobs every 15 minutes."""
    log.info("⏰ Running pending jobs...")
    try:
        run_pending_jobs()
    except Exception as e:
        log.error(f"Pending jobs error: {e}")


def job_full_scan():
    """Full scan of all content every hour."""
    log.info("⏰ Running full platform scan...")
    try:
        run_full_scan_for_all_creators()
    except Exception as e:
        log.error(f"Full scan error: {e}")


def job_health_check():
    """Log that the scheduler is still alive."""
    log.info(
        f"💚 GhostRights Crawler alive — "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )


# ── Schedule Setup ────────────────────────────────────────────

# Process new upload jobs every 15 minutes
schedule.every(15).minutes.do(job_pending)

# Full scan of all creators' content every hour
schedule.every(1).hours.do(job_full_scan)

# Health check log every 30 minutes
schedule.every(30).minutes.do(job_health_check)

# ── Run ───────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("🚀 GhostRights Cron Scheduler started")
    log.info("Pending jobs: every 15 minutes")
    log.info("Full scan:    every 1 hour")
    log.info("Press Ctrl+C to stop")

    # Run immediately on startup
    job_pending()

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

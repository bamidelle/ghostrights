"""
GhostRights — Piracy Crawler Engine
====================================
Hunts stolen content across:
- YouTube (via YouTube Data API)
- Google Search (via Custom Search API)
- Facebook public pages
- Telegram public channels
- Blogs & websites (via Scrapy/requests)

Run manually:   python crawler/crawler.py
Run on schedule: via APScheduler on VPS (cron_runner.py)
"""

import os
import time
import hashlib
import logging
import requests
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# ── Logging Setup ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("crawler/crawler.log")
    ]
)
log = logging.getLogger("GhostRightsCrawler")

# ── Config ────────────────────────────────────────────────────
YOUTUBE_API_KEY      = os.getenv("YOUTUBE_API_KEY")
GOOGLE_SEARCH_KEY    = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_SEARCH_CX     = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
SUPABASE_URL         = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
MIN_CONFIDENCE       = int(os.getenv("MIN_MATCH_CONFIDENCE", 75))


# ════════════════════════════════════════════════════════════════
# SUPABASE CLIENT (direct REST — no streamlit dependency)
# ════════════════════════════════════════════════════════════════

class SupabaseClient:
    """Lightweight Supabase REST client for crawler use."""

    def __init__(self):
        self.url = SUPABASE_URL
        self.key = SUPABASE_SERVICE_KEY
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

    def select(self, table: str, filters: dict = None,
               limit: int = 100) -> list:
        """Fetch rows from a table."""
        url = f"{self.url}/rest/v1/{table}"
        params = {"limit": limit}
        if filters:
            for key, val in filters.items():
                params[key] = f"eq.{val}"
        try:
            r = requests.get(url, headers=self.headers,
                             params=params, timeout=15)
            return r.json() if r.ok else []
        except Exception as e:
            log.error(f"Supabase select error: {e}")
            return []

    def insert(self, table: str, data: dict) -> Optional[dict]:
        """Insert a row into a table."""
        url = f"{self.url}/rest/v1/{table}"
        try:
            r = requests.post(url, headers=self.headers,
                              json=data, timeout=15)
            result = r.json()
            return result[0] if isinstance(result, list) \
                and result else None
        except Exception as e:
            log.error(f"Supabase insert error: {e}")
            return None

    def update(self, table: str, match: dict,
               data: dict) -> bool:
        """Update rows in a table."""
        url = f"{self.url}/rest/v1/{table}"
        params = {k: f"eq.{v}" for k, v in match.items()}
        try:
            r = requests.patch(url, headers=self.headers,
                               json=data, params=params,
                               timeout=15)
            return r.ok
        except Exception as e:
            log.error(f"Supabase update error: {e}")
            return False


db = SupabaseClient()


# ════════════════════════════════════════════════════════════════
# FINGERPRINT MATCHER
# ════════════════════════════════════════════════════════════════

class FingerprintMatcher:
    """Compares content fingerprints to detect piracy."""

    @staticmethod
    def title_similarity(original: str, found: str) -> float:
        """
        Calculate similarity between two titles.
        Returns 0.0 to 100.0 confidence score.
        """
        if not original or not found:
            return 0.0

        orig = original.lower().strip()
        fnd = found.lower().strip()

        # Exact match
        if orig == fnd:
            return 100.0

        # Check if original title is contained in found title
        if orig in fnd or fnd in orig:
            return 90.0

        # Word overlap scoring
        orig_words = set(orig.split())
        fnd_words  = set(fnd.split())

        # Remove common stop words
        stop_words = {
            "the", "a", "an", "in", "on", "at",
            "of", "and", "or", "ft", "feat",
            "official", "video", "full", "movie",
            "nollywood", "latest", "new", "2024", "2025"
        }
        orig_words -= stop_words
        fnd_words  -= stop_words

        if not orig_words:
            return 0.0

        overlap = len(orig_words & fnd_words)
        score = (overlap / len(orig_words)) * 85.0
        return round(score, 2)

    @staticmethod
    def url_already_detected(url: str,
                             content_id: str) -> bool:
        """Check if this URL was already logged."""
        results = db.select(
            "detections",
            {"pirated_url": url, "content_id": content_id},
            limit=1
        )
        return len(results) > 0


# ════════════════════════════════════════════════════════════════
# YOUTUBE CRAWLER
# ════════════════════════════════════════════════════════════════

class YouTubeCrawler:
    """Searches YouTube for pirated copies using Data API v3."""

    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def search(self, query: str,
               max_results: int = 25) -> list:
        """Search YouTube for videos matching the query."""
        if not YOUTUBE_API_KEY:
            log.warning("YouTube API key not configured")
            return []

        try:
            url = f"{self.BASE_URL}/search"
            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": max_results,
                "key": YOUTUBE_API_KEY,
                "order": "relevance"
            }
            r = requests.get(url, params=params, timeout=15)
            if not r.ok:
                log.error(f"YouTube search error: {r.text}")
                return []

            items = r.json().get("items", [])
            results = []

            for item in items:
                video_id = item["id"]["videoId"]
                snippet  = item["snippet"]
                results.append({
                    "platform":      "youtube",
                    "url":           f"https://youtube.com/watch?v={video_id}",
                    "title":         snippet.get("title", ""),
                    "channel":       snippet.get("channelTitle", ""),
                    "description":   snippet.get("description", ""),
                    "published_at":  snippet.get("publishedAt", ""),
                    "thumbnail":     snippet.get("thumbnails", {})
                                     .get("default", {})
                                     .get("url", "")
                })

            log.info(f"YouTube: found {len(results)} results "
                     f"for '{query}'")
            return results

        except Exception as e:
            log.error(f"YouTube crawler error: {e}")
            return []

    def get_video_stats(self, video_id: str) -> dict:
        """Get view count and stats for a specific video."""
        if not YOUTUBE_API_KEY:
            return {}
        try:
            url = f"{self.BASE_URL}/videos"
            params = {
                "part": "statistics,snippet",
                "id": video_id,
                "key": YOUTUBE_API_KEY
            }
            r = requests.get(url, params=params, timeout=15)
            items = r.json().get("items", [])
            if items:
                stats = items[0].get("statistics", {})
                return {
                    "views": int(stats.get("viewCount", 0)),
                    "likes": int(stats.get("likeCount", 0)),
                    "comments": int(stats.get("commentCount", 0))
                }
            return {}
        except Exception:
            return {}


# ════════════════════════════════════════════════════════════════
# GOOGLE SEARCH CRAWLER
# ════════════════════════════════════════════════════════════════

class GoogleSearchCrawler:
    """
    Uses Google Custom Search API to find pirated content
    on blogs, streaming sites, and download portals.
    Free tier: 100 queries/day
    """

    BASE_URL = "https://www.googleapis.com/customsearch/v1"

    # Sites commonly hosting pirated African content
    PIRACY_SITE_PATTERNS = [
        "nollywooddownload", "9jarocks", "waploaded",
        "tooxclusive", "fzmovies", "netnaija",
        "naijaextra", "bellanaijadownload",
        "o2tvmovies", "moviesrex", "filmyworld",
        "downloadhub", "tamilrockers"
    ]

    def search(self, query: str,
               num_results: int = 10) -> list:
        """Search Google for pirated copies."""
        if not GOOGLE_SEARCH_KEY or not GOOGLE_SEARCH_CX:
            log.warning("Google Search API not configured")
            return []

        try:
            params = {
                "key": GOOGLE_SEARCH_KEY,
                "cx":  GOOGLE_SEARCH_CX,
                "q":   query,
                "num": num_results,
                "safe": "off"
            }
            r = requests.get(self.BASE_URL,
                             params=params, timeout=15)
            if not r.ok:
                log.error(f"Google search error: {r.text}")
                return []

            items = r.json().get("items", [])
            results = []

            for item in items:
                url   = item.get("link", "")
                title = item.get("title", "")
                snippet = item.get("snippet", "")

                # Flag if URL matches known piracy patterns
                is_piracy_site = any(
                    p in url.lower()
                    for p in self.PIRACY_SITE_PATTERNS
                )

                results.append({
                    "platform":       "blog",
                    "url":            url,
                    "title":          title,
                    "snippet":        snippet,
                    "is_piracy_site": is_piracy_site
                })

            log.info(f"Google: found {len(results)} results "
                     f"for '{query}'")
            return results

        except Exception as e:
            log.error(f"Google crawler error: {e}")
            return []


# ════════════════════════════════════════════════════════════════
# TELEGRAM CRAWLER
# ════════════════════════════════════════════════════════════════

class TelegramCrawler:
    """
    Searches public Telegram channels via web preview.
    Does not require Telegram API key for public channels.
    """

    # Known Nollywood/music piracy Telegram patterns
    PIRACY_CHANNELS = [
        "nollywoodmovies", "naijamovies", "africamovies",
        "nollywoodnew", "nigerianmovies", "afrobeatsmp3",
        "naijamusicdownload", "africanmusic"
    ]

    def search_web_for_telegram(self, query: str) -> list:
        """
        Search Google for content shared on Telegram.
        This finds public Telegram posts indexed by Google.
        """
        if not GOOGLE_SEARCH_KEY or not GOOGLE_SEARCH_CX:
            return []

        try:
            telegram_query = f"site:t.me {query}"
            params = {
                "key": GOOGLE_SEARCH_KEY,
                "cx":  GOOGLE_SEARCH_CX,
                "q":   telegram_query,
                "num": 10
            }
            r = requests.get(
                "https://www.googleapis.com/customsearch/v1",
                params=params, timeout=15
            )
            items = r.json().get("items", []) if r.ok else []
            results = []

            for item in items:
                results.append({
                    "platform": "telegram",
                    "url":      item.get("link", ""),
                    "title":    item.get("title", ""),
                    "snippet":  item.get("snippet", "")
                })

            log.info(f"Telegram: found {len(results)} "
                     f"results for '{query}'")
            return results

        except Exception as e:
            log.error(f"Telegram crawler error: {e}")
            return []


# ════════════════════════════════════════════════════════════════
# FACEBOOK CRAWLER
# ════════════════════════════════════════════════════════════════

class FacebookCrawler:
    """
    Searches for pirated content shared publicly on Facebook.
    Uses Google Search targeting facebook.com.
    """

    def search(self, query: str) -> list:
        """Find content shared on Facebook via Google Search."""
        if not GOOGLE_SEARCH_KEY or not GOOGLE_SEARCH_CX:
            return []

        try:
            fb_query = f"site:facebook.com {query} movie OR song"
            params = {
                "key": GOOGLE_SEARCH_KEY,
                "cx":  GOOGLE_SEARCH_CX,
                "q":   fb_query,
                "num": 10
            }
            r = requests.get(
                "https://www.googleapis.com/customsearch/v1",
                params=params, timeout=15
            )
            items = r.json().get("items", []) if r.ok else []
            results = []

            for item in items:
                results.append({
                    "platform": "facebook",
                    "url":      item.get("link", ""),
                    "title":    item.get("title", ""),
                    "snippet":  item.get("snippet", "")
                })

            log.info(f"Facebook: found {len(results)} "
                     f"results for '{query}'")
            return results

        except Exception as e:
            log.error(f"Facebook crawler error: {e}")
            return []


# ════════════════════════════════════════════════════════════════
# TIKTOK CRAWLER
# ════════════════════════════════════════════════════════════════

class TikTokCrawler:
    """Searches TikTok for pirated clips via Google Search."""

    def search(self, query: str) -> list:
        if not GOOGLE_SEARCH_KEY or not GOOGLE_SEARCH_CX:
            return []
        try:
            tiktok_query = f"site:tiktok.com {query}"
            params = {
                "key": GOOGLE_SEARCH_KEY,
                "cx":  GOOGLE_SEARCH_CX,
                "q":   tiktok_query,
                "num": 10
            }
            r = requests.get(
                "https://www.googleapis.com/customsearch/v1",
                params=params, timeout=15
            )
            items = r.json().get("items", []) if r.ok else []
            results = []

            for item in items:
                results.append({
                    "platform": "tiktok",
                    "url":      item.get("link", ""),
                    "title":    item.get("title", ""),
                    "snippet":  item.get("snippet", "")
                })

            return results
        except Exception as e:
            log.error(f"TikTok crawler error: {e}")
            return []


# ════════════════════════════════════════════════════════════════
# DETECTION LOGGER
# ════════════════════════════════════════════════════════════════

class DetectionLogger:
    """Saves confirmed piracy detections to Supabase."""

    def log_detection(self, content: dict,
                      result: dict,
                      confidence: float,
                      method: str) -> bool:
        """Save a piracy detection to the database."""
        try:
            url = result.get("url", "")
            content_id = content.get("id")
            creator_id = content.get("creator_id")

            # Skip if already logged
            if FingerprintMatcher.url_already_detected(
                url, content_id
            ):
                log.info(f"Already detected: {url[:60]}...")
                return False

            # Estimate views
            views = 0
            if result.get("platform") == "youtube":
                video_id = url.split("v=")[-1].split("&")[0] \
                    if "v=" in url else ""
                if video_id:
                    stats = YouTubeCrawler().get_video_stats(
                        video_id
                    )
                    views = stats.get("views", 0)

            # Build detection record
            detection = {
                "content_id":       content_id,
                "creator_id":       creator_id,
                "platform":         result.get("platform", "other"),
                "pirated_url":      url,
                "pirated_page_title": result.get("title", ""),
                "pirated_channel_name": result.get("channel", ""),
                "match_confidence": confidence,
                "detection_method": method,
                "estimated_views":  views,
                "status":           "new",
                "first_detected_at": datetime.now().isoformat()
            }

            saved = db.insert("detections", detection)

            if saved:
                # Update content piracy count
                db.update(
                    "protected_content",
                    {"id": content_id},
                    {
                        "total_pirated_copies_found":
                            content.get(
                                "total_pirated_copies_found", 0
                            ) + 1
                    }
                )

                # Send notification to creator
                db.insert("notifications", {
                    "creator_id":        creator_id,
                    "notification_type": "new_detection",
                    "title":             "Piracy Detected!",
                    "message": (
                        f'We found a pirated copy of '
                        f'"{content.get("title", "your content")}" '
                        f'on {result.get("platform", "").title()}. '
                        f'Confidence: {confidence:.0f}%'
                    ),
                    "send_dashboard": True,
                    "send_email":     True,
                    "send_whatsapp":  True,
                    "detection_id":   saved.get("id")
                })

                log.info(
                    f"✅ Detection logged: "
                    f"{content.get('title')} on "
                    f"{result.get('platform')} "
                    f"({confidence:.0f}% confidence)"
                )
                return True

            return False

        except Exception as e:
            log.error(f"Detection log error: {e}")
            return False


# ════════════════════════════════════════════════════════════════
# MAIN CRAWLER ORCHESTRATOR
# ════════════════════════════════════════════════════════════════

class GhostRightsCrawler:
    """
    Main crawler that coordinates all platform crawlers
    for a single piece of content.
    """

    def __init__(self):
        self.youtube   = YouTubeCrawler()
        self.google    = GoogleSearchCrawler()
        self.telegram  = TelegramCrawler()
        self.facebook  = FacebookCrawler()
        self.tiktok    = TikTokCrawler()
        self.matcher   = FingerprintMatcher()
        self.logger    = DetectionLogger()

    def scan_content(self, content: dict) -> dict:
        """
        Full scan of one content item across all platforms.
        Returns summary of findings.
        """
        title      = content.get("title", "")
        content_id = content.get("id")
        creator_id = content.get("creator_id")

        log.info(f"🔍 Scanning: '{title}' [{content_id}]")

        summary = {
            "content_id":    content_id,
            "title":         title,
            "total_found":   0,
            "new_detections": 0,
            "platforms":     {}
        }

        # Build search queries
        queries = self._build_search_queries(content)

        all_results = []

        # ── YouTube ──────────────────────────────────────────
        for query in queries[:2]:
            results = self.youtube.search(query)
            all_results.extend(results)
            time.sleep(0.5)  # Rate limiting

        # ── Google (blogs/sites) ─────────────────────────────
        for query in queries[:2]:
            results = self.google.search(query)
            all_results.extend(results)
            time.sleep(0.5)

        # ── Telegram ─────────────────────────────────────────
        results = self.telegram.search_web_for_telegram(
            queries[0]
        )
        all_results.extend(results)
        time.sleep(0.5)

        # ── Facebook ─────────────────────────────────────────
        results = self.facebook.search(queries[0])
        all_results.extend(results)
        time.sleep(0.5)

        # ── TikTok ───────────────────────────────────────────
        results = self.tiktok.search(queries[0])
        all_results.extend(results)

        log.info(f"Total raw results: {len(all_results)}")

        # ── Analyse & Filter Results ─────────────────────────
        for result in all_results:
            found_title = result.get("title", "")
            platform    = result.get("platform", "other")

            # Calculate match confidence
            confidence = self.matcher.title_similarity(
                title, found_title
            )

            # Additional boost for known piracy sites
            if result.get("is_piracy_site"):
                confidence = min(confidence + 15, 100)

            # Skip low confidence matches
            if confidence < MIN_CONFIDENCE:
                continue

            summary["total_found"] += 1
            summary["platforms"][platform] = \
                summary["platforms"].get(platform, 0) + 1

            # Log the detection
            logged = self.logger.log_detection(
                content=content,
                result=result,
                confidence=confidence,
                method="keyword_search"
            )
            if logged:
                summary["new_detections"] += 1

        log.info(
            f"✅ Scan complete for '{title}': "
            f"{summary['total_found']} matches, "
            f"{summary['new_detections']} new"
        )

        return summary

    def _build_search_queries(self, content: dict) -> list:
        """Build optimised search queries for this content."""
        title   = content.get("title", "")
        ctype   = content.get("content_type", "")
        year    = content.get("release_year", "")

        # Content type search terms
        type_terms = {
            "movie":        ["movie", "full movie", "download"],
            "short_film":   ["short film", "watch"],
            "music_track":  ["mp3", "download", "audio"],
            "album":        ["album", "zip download"],
            "podcast":      ["podcast", "episode"],
            "youtube_video": ["video", "watch"],
        }
        terms = type_terms.get(ctype, ["download", "watch"])

        queries = [
            f'"{title}" {terms[0]}',
            f'{title} {year} free download',
            f'{title} nollywood {terms[0]}',
        ]

        return queries


# ════════════════════════════════════════════════════════════════
# JOB RUNNER
# ════════════════════════════════════════════════════════════════

def run_pending_jobs():
    """
    Process all queued crawler jobs from the database.
    Called by the scheduler every hour.
    """
    log.info("🚀 GhostRights Crawler starting...")

    # Get queued jobs
    jobs = db.select(
        "crawler_jobs",
        {"status": "queued"},
        limit=10
    )

    if not jobs:
        log.info("No pending jobs. Crawler idle.")
        return

    log.info(f"Processing {len(jobs)} jobs...")
    crawler = GhostRightsCrawler()

    for job in jobs:
        job_id     = job.get("id")
        content_id = job.get("content_id")

        # Mark job as running
        db.update(
            "crawler_jobs",
            {"id": job_id},
            {
                "status":     "running",
                "started_at": datetime.now().isoformat()
            }
        )

        try:
            # Get content details
            contents = db.select(
                "protected_content",
                {"id": content_id},
                limit=1
            )

            if not contents:
                log.warning(
                    f"Content {content_id} not found"
                )
                db.update(
                    "crawler_jobs",
                    {"id": job_id},
                    {"status": "failed",
                     "error_message": "Content not found"}
                )
                continue

            content = contents[0]
            start   = time.time()

            # Run the scan
            summary = crawler.scan_content(content)

            duration = int(time.time() - start)

            # Mark job complete
            db.update(
                "crawler_jobs",
                {"id": job_id},
                {
                    "status":          "complete",
                    "completed_at":    datetime.now().isoformat(),
                    "duration_seconds": duration,
                    "matches_found":   summary["total_found"],
                    "new_detections":  summary["new_detections"]
                }
            )

            log.info(
                f"✅ Job {job_id} complete in {duration}s"
            )

        except Exception as e:
            log.error(f"Job {job_id} failed: {e}")
            db.update(
                "crawler_jobs",
                {"id": job_id},
                {
                    "status":        "failed",
                    "error_message": str(e)
                }
            )

    log.info("Crawler run complete.")


def run_full_scan_for_all_creators():
    """
    Scheduled job: scan ALL active content for ALL creators.
    Runs every hour via cron.
    """
    log.info("Running full platform scan for all creators...")

    all_content = db.select(
        "protected_content",
        {"is_active": "true"},
        limit=500
    )

    log.info(f"Scanning {len(all_content)} content items...")
    crawler = GhostRightsCrawler()

    for content in all_content:
        try:
            crawler.scan_content(content)
            time.sleep(2)  # Polite crawling delay
        except Exception as e:
            log.error(
                f"Error scanning {content.get('title')}: {e}"
            )

    log.info("Full scan complete.")


# ════════════════════════════════════════════════════════════════
# ENTRY POINT
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "full":
        run_full_scan_for_all_creators()
    else:
        run_pending_jobs()

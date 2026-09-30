"""
Scraper for MakerWorld User Profile metrics and point totals.
"""

import json
import re
import urllib.request
import urllib.error
from typing import Dict, Any, Optional
from core.database import Database
from tracker.points_calculator import PointsCalculator


class MetricsScraper:
    def __init__(self, user_id: str, db: Optional[Database] = None):
        self.user_id = user_id
        self.db = db
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }

    def fetch_user_stats(self) -> Dict[str, Any]:
        """
        Scrapes user metrics (downloads, prints, boosts, models).
        """
        if not self.user_id or self.user_id == "YOUR_MAKERWORLD_USER_ID":
            # Return demo statistics if user hasn't set their ID yet
            latest = self.db.get_latest_metrics() if self.db else None
            if latest:
                return {
                    "downloads": latest["total_downloads"],
                    "prints": latest["total_prints"],
                    "boosts": latest["total_boosts"],
                    "points": latest["total_points"],
                    "note": "Loaded from local database history."
                }
            return {
                "downloads": 0,
                "prints": 0,
                "boosts": 0,
                "points": 0,
                "note": "Sin estadísticas previas. Conecta tu perfil en config.yaml para sincronizar."
            }

        url = f"https://makerworld.com/en/u/{self.user_id}"
        req = urllib.request.Request(url, headers=self.headers)
        
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
                
                # Extract stats from HTML or JSON script tags
                downloads = 0
                prints = 0
                boosts = 0

                dl_match = re.search(r'([0-9,]+)\s*(?:Downloads|downloads)', html)
                if dl_match:
                    downloads = int(dl_match.group(1).replace(",", ""))

                pr_match = re.search(r'([0-9,]+)\s*(?:Prints|prints)', html)
                if pr_match:
                    prints = int(pr_match.group(1).replace(",", ""))

                # Points estimation: approximately 2-3 points per download/print + 12 points per boost
                estimated_points = int(downloads * 1.5 + prints * 2.0 + boosts * 12)

                if self.db:
                    self.db.record_metrics(
                        total_points=estimated_points,
                        available_points=estimated_points,
                        downloads=downloads,
                        prints=prints,
                        boosts=boosts
                    )

                return {
                    "downloads": downloads,
                    "prints": prints,
                    "boosts": boosts,
                    "points": estimated_points
                }
        except Exception as e:
            # Fallback to last recorded metrics
            latest = self.db.get_latest_metrics() if self.db else None
            return {
                "downloads": latest["total_downloads"] if latest else 0,
                "prints": latest["total_prints"] if latest else 0,
                "boosts": latest["total_boosts"] if latest else 0,
                "points": latest["total_points"] if latest else 0,
                "error": f"Failed to fetch live page: {e}"
            }

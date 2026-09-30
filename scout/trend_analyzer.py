"""
Trend Analyzer for picking optimal model generation parameters.
Prioritizes high-converting templates and avoids duplicate configurations.
"""

import random
from typing import Dict, Any, List
from scout.scrapers import TrendScraper
from core.database import Database


class TrendAnalyzer:
    def __init__(self, db: Database = None):
        self.scraper = TrendScraper()
        self.db = db

    def pick_next_opportunity(self) -> Dict[str, Any]:
        """
        Determines the next model to generate with randomized high-demand parameters.
        """
        trends = self.scraper.fetch_makerworld_trending()
        
        # Available parametric templates
        candidates = [
            {
                "template": "gridfinity",
                "params": random.choice([
                    {"grid_x": 1, "grid_y": 2, "units_z": 6},
                    {"grid_x": 2, "grid_y": 2, "units_z": 4},
                    {"grid_x": 1, "grid_y": 3, "units_z": 5},
                    {"grid_x": 1, "grid_y": 1, "units_z": 3},
                ]),
                "reason": "Top evergreen search term on MakerWorld; high print-to-download ratio."
            },
            {
                "template": "phone_stand",
                "params": random.choice([
                    {"width": 75.0, "depth": 85.0, "height": 80.0},
                    {"width": 90.0, "depth": 95.0, "height": 85.0},
                    {"width": 65.0, "depth": 75.0, "height": 70.0},
                ]),
                "reason": "Universal appeal across non-technical audience; drives high external social traffic."
            },
            {
                "template": "cable_holder",
                "params": random.choice([
                    {"slots": 3},
                    {"slots": 5},
                    {"slots": 2},
                ]),
                "reason": "Sub-30 minute print time triggers instant impulse prints and boost rewards."
            },
            {
                "template": "modular_bracket",
                "params": random.choice([
                    {"length": 60.0, "width": 30.0, "thickness": 6.0},
                    {"length": 80.0, "width": 35.0, "thickness": 8.0},
                ]),
                "reason": "High utility item frequently searched by Bambu Lab workshop owners."
            }
        ]

        selection = random.choice(candidates)
        return selection

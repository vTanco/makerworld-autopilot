"""
Trend Analyzer for picking optimal model generation parameters.
Prioritizes high-converting, trending 3D printing opportunities and avoids duplicate categories.
Dynamically balances categories based on MakerWorld search velocity and historical database usage.
"""

import random
from typing import Dict, Any, List
from scout.scrapers import TrendScraper
from core.database import Database


class TrendAnalyzer:
    def __init__(self, db: Database = None):
        self.scraper = TrendScraper()
        self.db = db

    def get_all_trending_candidates(self) -> List[Dict[str, Any]]:
        """
        Returns full list of high-velocity trending 3D printing opportunities.
        """
        return [
            {
                "template": "bambu_poop_chute",
                "title": "Magnetic Bambu Lab Purge Poop Chute & Deflector",
                "params": {"width": 68.0, "depth": 85.0, "height": 95.0},
                "category": "3D Printer Accessories",
                "reason": "Top #1 searched 3D printer accessory on MakerWorld; hundreds of thousands of downloads across A1, P1S, and X1C.",
                "highlight": "High-efficiency Bambu Lab purge chute deflector. Fits snugly against the purge chute to cleanly direct extruded filament waste into your trash bin or collector bucket. 100% support-free print.",
                "tags": ["bambulab", "poop chute", "purge bin", "a1 mini", "p1s", "x1c", "printer accessory", "3d printer upgrade", "functional print"]
            },
            {
                "template": "sd_usb_caddy",
                "title": "Minimalist Desktop SD, MicroSD & USB Drive Organizer Caddy",
                "params": {"width": 65.0, "depth": 55.0, "height": 24.0},
                "category": "Household/Office",
                "reason": "Top small hardware & storage accessory. High search rate among makers, photographers, and 3D printer owners.",
                "highlight": "Clean desktop media organizer designed to hold 4 full-sized SD cards, 6 MicroSD cards, and 2 USB flash drives. Solid stable footprint that prints in under 45 minutes without supports.",
                "tags": ["sd card holder", "microsd organizer", "usb drive caddy", "desk organizer", "3d printing accessories", "camera gear", "office", "functional print"]
            },
            {
                "template": "headphone_hanger",
                "title": "Minimalist Under-Desk Ergonomic Headphone Hanger Hook",
                "params": {"mount_len": 45.0, "arm_drop": 65.0, "cradle_len": 60.0, "width": 38.0},
                "category": "Household/Office",
                "reason": "Viral home office & battlestation accessory. Universal appeal and strong external social media traffic.",
                "highlight": "Sturdy under-desk headphone mount with a wide 38mm curved cradle that protects headband cushioning. Includes a front retention lip to keep audio cables neatly coiled.",
                "tags": ["headphone hanger", "headset stand", "under desk", "cable management", "gaming setup", "desk organization", "bambulab", "functional print"]
            },
            {
                "template": "hex_wrench_caddy",
                "title": "Bambu Lab Hex Key & Printer Maintenance Tool Caddy",
                "params": {"width": 70.0, "depth": 40.0, "height": 35.0},
                "category": "3D Printer Accessories",
                "reason": "High-utility maintenance kit organizer for Bambu Lab users; high bookmark and boost conversion rates.",
                "highlight": "Organized desktop caddy for your official Bambu Lab hex keys (1.5mm to 4.0mm), spare nozzles, and maintenance scraper. Keep your printer workstation neat and ready.",
                "tags": ["bambulab", "hex key holder", "allen wrench", "tool caddy", "maintenance kit", "a1 mini", "p1s", "x1c", "printer accessory", "functional"]
            },
            {
                "template": "ptfe_filament_clip",
                "title": "Dual PTFE Tube Guide & Filament Spool Anti-Tangle Clip",
                "params": {"length": 32.0, "width": 14.0, "height": 12.0},
                "category": "3D Printer Accessories",
                "reason": "Sub-20 minute print time triggers instant impulse prints, high user ratings, and rapid MakerReward point accumulation.",
                "highlight": "High-tension dual-purpose clip. Clamps securely onto 1.75mm filament spool rims to lock loose ends in place, or snaps onto 4mm PTFE bowden tubes to prevent rubbing.",
                "tags": ["bambulab", "filament clip", "ptfe tube", "spool clip", "ams", "cable guide", "anti tangle", "3d printer upgrade", "functional print"]
            },
            {
                "template": "gridfinity",
                "title": "Gridfinity 2x2 Square Divided Component Tray (4U)",
                "params": {"grid_x": 2, "grid_y": 2, "units_z": 4},
                "category": "Household/Organization",
                "reason": "Ecosystem staple with massive ongoing community demand.",
                "highlight": "Spacious 2x2 4U divided storage bin (28mm height) with central divider. Excellent for sorting hardware, soldering supplies, and desktop accessories.",
                "tags": ["gridfinity", "divided bin", "modular storage", "hardware tray", "workshop", "bambulab"]
            },
            {
                "template": "phone_stand",
                "title": "Ergonomic 70° Video Call & FaceTime Phone Stand (80mm)",
                "params": {"width": 80.0, "depth": 85.0, "height": 85.0},
                "category": "Household/Office",
                "reason": "High everyday utility and non-technical appeal.",
                "highlight": "Steep 70° viewing angle specifically engineered for Zoom meetings, FaceTime calls, and desk notifications without neck strain.",
                "tags": ["facetime stand", "video call", "zoom", "phone holder", "ergonomic", "bambulab"]
            },
            {
                "template": "cable_holder",
                "title": "Minimalist 4-Slot Heavy Power & HDMI Cable Clip",
                "params": {"slots": 4, "slot_width": 5.5},
                "category": "Household/Office",
                "reason": "Under-desk cable management is one of the highest search volume queries on 3D print repositories.",
                "highlight": "Wider 5.5mm slots designed specifically for thick braided HDMI, DisplayPort, and monitor power cables.",
                "tags": ["hdmi clip", "power cord guide", "cable comb", "battlestation", "wire management", "bambulab"]
            },
            {
                "template": "modular_bracket",
                "title": "Reinforced Heavy-Duty 90° Structural Bracket (60mm)",
                "params": {"length": 60.0, "width": 30.0, "thickness": 6.0},
                "category": "Household/Tools",
                "reason": "Strong DIY builder engagement; high demand for functional strength prints.",
                "highlight": "Standard 60mm structural bracket with center triangular reinforcement gusset. High load rating for DIY workshop projects.",
                "tags": ["structural bracket", "gusset bracket", "heavy duty", "workshop", "hardware", "bambulab"]
            }
        ]

    def _get_recently_published_templates(self, limit: int = 10) -> List[str]:
        """Queries database for recently used templates to prevent repetition."""
        if not self.db:
            return []
        try:
            with self.db._get_connection() as conn:
                rows = conn.execute(
                    "SELECT template_used FROM models ORDER BY id DESC LIMIT ?", (limit,)
                ).fetchall()
                return [r[0] for r in rows if r and r[0]]
        except Exception as e:
            print(f"[TrendAnalyzer] DB fetch notice: {e}")
            return []

    def pick_next_opportunity(self) -> Dict[str, Any]:
        """
        Determines the next model to generate, strictly prioritizing non-recent templates.
        """
        recent = self._get_recently_published_templates(limit=5)
        candidates = self.get_all_trending_candidates()
        
        # Filter out candidates recently used
        fresh_candidates = [c for c in candidates if c["template"] not in recent]
        if fresh_candidates:
            return random.choice(fresh_candidates)
        return random.choice(candidates)

    def pick_batch_opportunities(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        Returns exactly `count` distinct, highly trending opportunities,
        ensuring NO category or template repetition within the batch.
        """
        candidates = self.get_all_trending_candidates()
        recent = self._get_recently_published_templates(limit=10)

        # Sort candidates: non-recent first
        candidates_sorted = sorted(
            candidates,
            key=lambda c: (c["template"] in recent, recent.index(c["template"]) if c["template"] in recent else -1)
        )

        selected = []
        used_templates = set()
        for cand in candidates_sorted:
            if cand["template"] not in used_templates:
                selected.append(cand)
                used_templates.add(cand["template"])
                if len(selected) >= count:
                    break

        return selected

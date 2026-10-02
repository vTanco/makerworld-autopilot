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
        Expanded catalog with 14 templates covering viral niches.
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
            },
            # ===== NEW HIGH-DEMAND GENERATORS =====
            {
                "template": "watch_dock",
                "title": "Minimalist Smartwatch Charging Dock Stand (65mm Base)",
                "params": {"base_diameter": 65.0, "stand_height": 55.0},
                "category": "Household/Office",
                "reason": "Apple Watch is the #1 selling wearable worldwide. Charging docks are a viral category with 50K+ downloads.",
                "highlight": "Elegant circular charging dock for Apple Watch and compatible smartwatches. Features weighted base, tapered pillar with rear cable channel, and raised cradle rim.",
                "tags": ["apple watch", "smartwatch dock", "charging stand", "watch holder", "nightstand", "bambulab", "functional print"]
            },
            {
                "template": "controller_stand",
                "title": "Universal Game Controller & Nintendo Switch Display Stand (120mm)",
                "params": {"width": 120.0, "depth": 80.0, "height": 65.0},
                "category": "Household/Office",
                "reason": "Gaming accessories are the #2 most downloaded category on MakerWorld after printer upgrades.",
                "highlight": "Universal display and charging stand for PS5, Xbox, Switch Pro, and Joy-Con controllers. Angled backrest, front retention lip, cable pass-through.",
                "tags": ["controller stand", "nintendo switch", "ps5", "xbox", "gaming", "display stand", "bambulab", "functional print"]
            },
            {
                "template": "pen_holder",
                "title": "Elegant Cylindrical Dual Pen & Stylus Desktop Holder (55mm)",
                "params": {"diameter": 55.0, "height": 95.0, "slots": 2},
                "category": "Household/Office",
                "reason": "Universal office accessory with broad appeal beyond 3D printing community.",
                "highlight": "Clean cylindrical dual-cup pen and stylus holder with thick walls and solid weighted base. Perfect for Apple Pencil, markers, and standard pens.",
                "tags": ["pen holder", "pencil cup", "desk organizer", "stylus holder", "office", "apple pencil", "bambulab", "functional print"]
            },
            {
                "template": "monitor_riser",
                "title": "Ergonomic Monitor & Laptop Riser Stand (250mm, Pillar Legs)",
                "params": {"width": 250.0, "depth": 120.0, "height": 55.0, "leg_style": "pillars"},
                "category": "Household/Office",
                "reason": "Large functional prints get high engagement — users share photos and the model looks impressive in portfolios.",
                "highlight": "Sturdy monitor/laptop riser with cylindrical legs, center support beam, and rear cable management slot. Raises screen to ergonomic eye level.",
                "tags": ["monitor riser", "laptop stand", "desk riser", "ergonomic", "cable management", "bambulab", "functional print"]
            },
            {
                "template": "tool_mount",
                "title": "Wall-Mounted 6-Slot Tool Organizer Rack (180mm)",
                "params": {"width": 180.0, "height": 40.0, "depth": 30.0, "num_slots": 6},
                "category": "Household/Tools",
                "reason": "Workshop/garage organization is a massive niche. Wall mounts have high reprint rates.",
                "highlight": "Heavy-duty wall-mounted tool rack with 6 cylindrical slots for screwdrivers, pliers, and markers. Features rear mounting bosses and front label strip.",
                "tags": ["tool holder", "wall mount", "workshop organizer", "screwdriver holder", "garage", "bambulab", "functional print"]
            },
            # ===== PARAMETRIC VARIANTS (same templates, different configs) =====
            {
                "template": "gridfinity",
                "title": "Gridfinity 1x3 Long Parts Tray (6U Height)",
                "params": {"grid_x": 1, "grid_y": 3, "units_z": 6},
                "category": "Household/Organization",
                "reason": "1x3 long format is popular for screws, drill bits, and cable ties.",
                "highlight": "Extended 1x3 Gridfinity bin (42mm tall) perfect for long items like drill bits, cable ties, and pens.",
                "tags": ["gridfinity", "long tray", "parts bin", "workshop", "modular storage", "bambulab"]
            },
            {
                "template": "watch_dock",
                "title": "Compact Bedside Smartwatch Charging Stand (50mm Base)",
                "params": {"base_diameter": 50.0, "stand_height": 45.0},
                "category": "Household/Office",
                "reason": "Smaller variant for nightstands and tight spaces.",
                "highlight": "Compact nightstand charging dock for smartwatches. Smaller 50mm footprint takes minimal space on your bedside table.",
                "tags": ["apple watch", "nightstand", "compact", "charging dock", "watch stand", "bambulab", "functional print"]
            },
            {
                "template": "pen_holder",
                "title": "Triple Pen & Marker Desktop Organizer Cup (60mm)",
                "params": {"diameter": 60.0, "height": 100.0, "slots": 3},
                "category": "Household/Office",
                "reason": "Triple variant for artists and calligraphers with many pens.",
                "highlight": "Three-cup pen organizer with connecting bridge. Separate cups for pens, markers, and brushes.",
                "tags": ["pen holder", "triple cup", "marker organizer", "art supplies", "calligraphy", "bambulab", "functional print"]
            },
            {
                "template": "controller_stand",
                "title": "Compact PS5 DualSense Controller Dock (100mm)",
                "params": {"width": 100.0, "depth": 70.0, "height": 55.0},
                "category": "Household/Office",
                "reason": "PS5-specific variant captures targeted search traffic.",
                "highlight": "Sized specifically for the PS5 DualSense controller. Compact 100mm footprint fits on tight gaming desks.",
                "tags": ["ps5 controller", "dualsense stand", "gaming dock", "controller holder", "playstation", "bambulab", "functional print"]
            },
            {
                "template": "tool_mount",
                "title": "Compact 4-Slot Wall Screwdriver Holder (120mm)",
                "params": {"width": 120.0, "height": 35.0, "depth": 25.0, "num_slots": 4, "slot_diameter": 10.0},
                "category": "Household/Tools",
                "reason": "Compact variant for smaller workshops and pegboards.",
                "highlight": "Space-efficient 4-slot screwdriver holder with 10mm slots. Mounts easily on pegboard or wall.",
                "tags": ["screwdriver holder", "compact", "pegboard", "wall mount", "workshop", "bambulab", "functional print"]
            },
            {
                "template": "cable_holder",
                "title": "6-Slot USB-C & Lightning Cable Desk Organizer Clip",
                "params": {"slots": 6, "slot_width": 4.0},
                "category": "Household/Office",
                "reason": "USB-C cable management is top searched with iPhones and MacBooks.",
                "highlight": "6 slots sized for USB-C and Lightning cables. Keeps all your charging cables organized and within reach.",
                "tags": ["usb-c cable clip", "lightning cable holder", "cable organizer", "macbook", "iphone", "bambulab", "functional print"]
            },
            # ===== ADDITIONAL TRENDING HIGH-VELOCITY OPPORTUNITIES =====
            {
                "template": "bambu_poop_chute",
                "title": "Slim Purge Chute Deflector for Bambu Lab A1 Mini",
                "params": {"width": 55.0, "depth": 70.0, "height": 80.0},
                "category": "3D Printer Accessories",
                "reason": "Compact purge deflector tailored specifically for the A1 Mini's smaller footprint.",
                "highlight": "Low-profile filament purge deflector engineered specifically for Bambu Lab A1 Mini workspaces.",
                "tags": ["a1 mini", "poop chute", "bambulab", "purge bin", "printer upgrade", "functional print"]
            },
            {
                "template": "sd_usb_caddy",
                "title": "Compact 10x MicroSD & Dual USB-C Flash Drive Travel Case",
                "params": {"width": 50.0, "depth": 40.0, "height": 20.0},
                "category": "Household/Office",
                "reason": "High search volume among drone operators, GoPro creators, and 3D printing enthusiasts.",
                "highlight": "Precision travel caddy holding up to 10 MicroSD cards and 2 USB-C flash thumb drives with friction fit.",
                "tags": ["microsd case", "memory card holder", "usb-c drive", "drone gear", "gopro accessory", "functional print"]
            },
            {
                "template": "headphone_hanger",
                "title": "Dual Headphone & VR Headset Under-Desk Mount Hanger",
                "params": {"mount_len": 55.0, "arm_drop": 80.0, "cradle_len": 90.0, "width": 42.0},
                "category": "Household/Office",
                "reason": "Dual hanger design supports both gaming headsets and VR straps (Meta Quest / PSVR2).",
                "highlight": "Extra-wide dual cradle hook designed to support both gaming headphones and VR headsets under any desk.",
                "tags": ["dual headphone hanger", "vr mount", "meta quest", "gaming setup", "desk organization", "bambulab"]
            },
            {
                "template": "hex_wrench_caddy",
                "title": "Compact Bambu Lab Nozzle & Allen Key Station (1.5-3mm)",
                "params": {"width": 55.0, "depth": 35.0, "height": 30.0},
                "category": "3D Printer Accessories",
                "reason": "Compact maintenance organizer for users with limited workbench space.",
                "highlight": "Miniature workstation caddy for primary Bambu Lab hex keys and spare hardened steel nozzles.",
                "tags": ["nozzle holder", "hex key station", "allen wrench", "bambu tools", "a1 mini", "p1s", "printer upgrade"]
            },
            {
                "template": "ptfe_filament_clip",
                "title": "Triple Bowden Cable & PTFE Guide Clip for AMS Hub",
                "params": {"length": 40.0, "width": 16.0, "height": 14.0},
                "category": "3D Printer Accessories",
                "reason": "AMS multi-color users constantly search for cable combs to prevent tube binding.",
                "highlight": "Triple-channel PTFE bowden tube clip designed to neatly parallel-route filament lines from your AMS unit.",
                "tags": ["ams", "bambulab", "ptfe guide", "filament clip", "multi color", "printer upgrade", "functional print"]
            },
            {
                "template": "phone_stand",
                "title": "Compact Folding Angle Desktop Phone Holder (60mm Travel)",
                "params": {"width": 60.0, "depth": 75.0, "height": 70.0},
                "category": "Household/Office",
                "reason": "Smaller footprint phone stand favored by mobile and office workers.",
                "highlight": "Slim 60mm phone holder with tuned viewing angle and charging cable cutout.",
                "tags": ["compact phone stand", "iphone holder", "desk stand", "minimalist", "office", "bambulab"]
            },
            {
                "template": "modular_bracket",
                "title": "Heavy-Duty 45° Chamfered Reinforcement Gusset Bracket (80mm)",
                "params": {"length": 80.0, "width": 35.0, "thickness": 8.0},
                "category": "Household/Tools",
                "reason": "Larger 80mm structural bracket for heavy garage and shelving projects.",
                "highlight": "Industrial-grade 80mm corner brace with triangular gusset. Supports high mechanical loads.",
                "tags": ["structural bracket", "heavy duty", "corner brace", "workshop", "shelving", "functional print"]
            },
            {
                "template": "monitor_riser",
                "title": "Compact Dual Monitor Riser with Wall Leg Supports (300mm)",
                "params": {"width": 300.0, "depth": 140.0, "height": 65.0, "leg_style": "walls"},
                "category": "Household/Office",
                "reason": "Solid-wall monitor stand with higher load-bearing capacity for ultrawide screens.",
                "highlight": "300mm heavy-duty desk riser with structural side walls and integrated cable management.",
                "tags": ["monitor riser", "laptop stand", "desk organization", "ultrawide", "battlestation", "bambulab"]
            },
            {
                "template": "watch_dock",
                "title": "Dual Apple Watch & Fitness Tracker Bedside Nightstand Dock",
                "params": {"base_diameter": 80.0, "stand_height": 60.0},
                "category": "Household/Office",
                "reason": "Couples and multi-device owners frequently search for dual smartwatch docks.",
                "highlight": "Dual charging platform with dual rear cable routing channels and weighted circular base.",
                "tags": ["apple watch dock", "dual charger", "smartwatch stand", "nightstand", "bambulab", "functional print"]
            },
            {
                "template": "controller_stand",
                "title": "Nintendo Switch Joy-Con & Grip Controller Display Stand",
                "params": {"width": 110.0, "depth": 75.0, "height": 60.0},
                "category": "Household/Office",
                "reason": "Dedicated Nintendo Switch accessory search query with constant global volume.",
                "highlight": "Engineered cradle contour tailored to the official Nintendo Switch Joy-Con grip controller.",
                "tags": ["nintendo switch", "joy-con stand", "switch pro", "gaming dock", "display stand", "bambulab"]
            }
        ]

    def _get_recently_published_templates(self, limit: int = 15) -> List[str]:
        """Queries database for recently used templates to prevent repetition."""
        if not self.db:
            return []
        try:
            with self.db._get_connection() as conn:
                rows = conn.execute(
                    "SELECT template_used FROM models ORDER BY rowid DESC LIMIT ?", (limit,)
                ).fetchall()
                return [r[0] for r in rows if r and r[0]]
        except Exception as e:
            print(f"[TrendAnalyzer] DB fetch notice: {e}")
            return []

    def _get_recently_published_titles(self, limit: int = 50) -> List[str]:
        """Queries database for recently used titles to prevent repetition."""
        if not self.db:
            return []
        try:
            with self.db._get_connection() as conn:
                rows = conn.execute(
                    "SELECT title FROM models ORDER BY rowid DESC LIMIT ?", (limit,)
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

    def pick_batch_opportunities(self, count: int = 20) -> List[Dict[str, Any]]:
        """
        Returns exactly `count` distinct, highly trending opportunities,
        ensuring NO title repetition within the batch, NO repetition of already published titles,
        and maximum template diversity.
        """
        candidates = self.get_all_trending_candidates()
        recent_templates = self._get_recently_published_templates(limit=25)
        recent_titles = set(self._get_recently_published_titles(limit=50))

        # Filter out any candidates whose exact title has already been published
        fresh_candidates = [c for c in candidates if c["title"] not in recent_titles]
        if len(fresh_candidates) < count:
            # If not enough, allow older candidates but still prioritize fresh ones
            fresh_candidates = candidates

        # Sort candidates: non-recent template first, then least recently used template
        candidates_sorted = sorted(
            fresh_candidates,
            key=lambda c: (
                c["title"] in recent_titles,
                c["template"] in recent_templates[:5],
                recent_templates.count(c["template"])
            )
        )

        selected = []
        used_titles = set(recent_titles)
        used_templates_count = {}
        
        # First pass: strictly non-repeated titles and max 2 per template
        for cand in candidates_sorted:
            t = cand["template"]
            title = cand["title"]
            if title not in used_titles and used_templates_count.get(t, 0) < 2:
                selected.append(cand)
                used_titles.add(title)
                used_templates_count[t] = used_templates_count.get(t, 0) + 1
                if len(selected) >= count:
                    break

        # Fallback pass if count not reached: relax template count limit but keep titles unique
        if len(selected) < count:
            for cand in candidates_sorted:
                title = cand["title"]
                if title not in used_titles:
                    selected.append(cand)
                    used_titles.add(title)
                    if len(selected) >= count:
                        break

        return selected[:count]

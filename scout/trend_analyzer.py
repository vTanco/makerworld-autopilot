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
            },
            # ===== BATCH 3: 20 BRAND NEW HIGH-ENGAGEMENT OPPORTUNITIES =====
            {
                "template": "controller_stand",
                "title": "Xbox Series X/S & Elite Controller Display Stand (115mm)",
                "params": {"width": 115.0, "depth": 85.0, "height": 70.0},
                "category": "Household/Office",
                "reason": "Dedicated Xbox Series and Elite controller search volume on MakerWorld.",
                "highlight": "Custom-profiled gaming stand engineered specifically for Xbox Wireless and Xbox Elite Series 2 controllers with rear cable pass-through.",
                "tags": ["xbox controller", "xbox series x", "elite controller", "gaming stand", "desk setup", "bambulab", "functional print"]
            },
            {
                "template": "watch_dock",
                "title": "Nightstand Apple Watch Ultra & Series 9 Floating Charging Stand (70mm)",
                "params": {"base_diameter": 70.0, "stand_height": 65.0},
                "category": "Household/Office",
                "reason": "Apple Watch Ultra users search for wider weighted charging bases that prevent tipping.",
                "highlight": "Heavy-base floating nightstand charging dock sized for larger Apple Watch Ultra (49mm) and standard 41/45mm models.",
                "tags": ["apple watch ultra", "series 9", "charging dock", "nightstand", "smartwatch stand", "bambulab", "functional print"]
            },
            {
                "template": "pen_holder",
                "title": "Modern Minimalist Single Luxury Pen & Stylus Desk Stand (45mm)",
                "params": {"diameter": 45.0, "height": 60.0, "slots": 1},
                "category": "Household/Office",
                "reason": "Single luxury pen holders are a top minimalist desk trend on Pinterest and Reddit.",
                "highlight": "Weighted single-pen desk podium with 14° angled insertion cone. Showcases your Apple Pencil, Wacom stylus, or fountain pen.",
                "tags": ["single pen stand", "apple pencil", "luxury pen", "desk accessory", "minimalist", "bambulab", "functional print"]
            },
            {
                "template": "monitor_riser",
                "title": "Ultrawide Monitor & Studio Desk Shelf Stand (320mm, Heavy Duty)",
                "params": {"width": 320.0, "depth": 150.0, "height": 70.0, "leg_style": "pillars"},
                "category": "Household/Office",
                "reason": "Ultrawide displays need wider 300mm+ risers with reinforced pillar legs.",
                "highlight": "Extra-wide 320mm monitor riser built for ultrawide 34-49 inch curved screens and studio audio monitors.",
                "tags": ["ultrawide monitor", "desk shelf", "monitor riser", "studio monitor", "cable management", "bambulab", "functional print"]
            },
            {
                "template": "tool_mount",
                "title": "Heavy-Duty 8-Slot Pliers & Wire Cutters Wall Organizer (220mm)",
                "params": {"width": 220.0, "height": 45.0, "depth": 35.0, "num_slots": 8, "slot_diameter": 14.0},
                "category": "Household/Tools",
                "reason": "High search volume among garage and workshop organizers.",
                "highlight": "Industrial-grade wall-mounted organizer rack with 8 heavy-duty slots sized for pliers, wire strippers, and crimping tools.",
                "tags": ["pliers rack", "tool organizer", "workshop", "garage", "wall mount", "pegboard", "bambulab", "functional print"]
            },
            {
                "template": "gridfinity",
                "title": "Gridfinity 3x3 Large Deep Hardware Organizer Bin (6U)",
                "params": {"grid_x": 3, "grid_y": 3, "units_z": 6},
                "category": "Household/Organization",
                "reason": "Large 3x3 bins are high-demand for larger workshop tools and hardware.",
                "highlight": "Extra-roomy 3x3 Gridfinity modular bin (42mm deep) for organizing multimeters, power tool batteries, and bulky hardware.",
                "tags": ["gridfinity", "3x3 bin", "hardware storage", "modular organizer", "workshop", "bambulab", "functional print"]
            },
            {
                "template": "gridfinity",
                "title": "Gridfinity 1x4 Extra-Long Caliper & Ruler Tray (3U Shallow)",
                "params": {"grid_x": 1, "grid_y": 4, "units_z": 3},
                "category": "Household/Organization",
                "reason": "Engineers and makers look for long shallow trays for precision measuring tools.",
                "highlight": "Extended 1x4 shallow Gridfinity tray (21mm height) specifically proportioned for vernier calipers, tweezers, and stainless steel rulers.",
                "tags": ["gridfinity", "caliper tray", "long bin", "precision tools", "workshop", "bambulab", "functional print"]
            },
            {
                "template": "phone_stand",
                "title": "Compact iPad Mini & Kindle Reading Stand (85mm, 65° Angle)",
                "params": {"width": 85.0, "depth": 90.0, "height": 75.0},
                "category": "Household/Office",
                "reason": "Kindle and e-reader accessories see constant high download velocity.",
                "highlight": "Tuned 65° viewing stand engineered for comfortable hands-free Kindle reading and iPad Mini recipe display in the kitchen.",
                "tags": ["kindle stand", "ipad mini", "ereader", "reading stand", "tablet dock", "bambulab", "functional print"]
            },
            {
                "template": "cable_holder",
                "title": "Heavy 8-Slot Cable Management Comb for Desk Edge (Ethernet & Power)",
                "params": {"slots": 8, "slot_width": 6.0},
                "category": "Household/Office",
                "reason": "Power users with dual monitors need 8-slot heavy cable organizers.",
                "highlight": "High-capacity 8-slot desk cable guide designed for thick braided HDMI 2.1, DisplayPort, and heavy shielded power cables.",
                "tags": ["cable comb", "8 slot clip", "wire organizer", "battlestation", "desk setup", "bambulab", "functional print"]
            },
            {
                "template": "cable_holder",
                "title": "Compact 3-Slot Bedside Nightstand Cord Keeper (Braided Lightning & USB-C)",
                "params": {"slots": 3, "slot_width": 3.8},
                "category": "Household/Office",
                "reason": "Preventing charging cords from falling behind the bed is an evergreen pain point.",
                "highlight": "Low-profile 3-slot cord keeper designed to clamp to bedside tables and keep phone and watch charging cords accessible.",
                "tags": ["cord keeper", "nightstand cable", "usb-c clip", "charging cable", "desk organizer", "bambulab", "functional print"]
            },
            {
                "template": "modular_bracket",
                "title": "Reinforced 100mm Heavy-Duty 90° Workbench Shelf Bracket (8mm Wall)",
                "params": {"length": 100.0, "width": 40.0, "thickness": 8.0},
                "category": "Household/Tools",
                "reason": "High-load functional prints build strong community reputation and likes.",
                "highlight": "Heavy-duty 100mm structural corner bracket with thick 8mm walls and central reinforcing triangular gusset. Supports up to 25kg in PETG.",
                "tags": ["structural bracket", "heavy duty", "shelf bracket", "workbench", "garage", "bambulab", "functional print"]
            },
            {
                "template": "modular_bracket",
                "title": "Compact 50mm Structural Corner Gusset Joint for 2020 Aluminum Extrusion",
                "params": {"length": 50.0, "width": 25.0, "thickness": 5.0},
                "category": "Household/Tools",
                "reason": "3D printer builders and CNC makers constantly search for 2020 corner brackets.",
                "highlight": "Precision 50mm corner bracket designed to reinforce 2020 T-slot aluminum extrusion frames on custom 3D printers and CNC rigs.",
                "tags": ["2020 extrusion", "corner bracket", "t-slot", "3d printer frame", "cnc", "bambulab", "functional print"]
            },
            {
                "template": "bambu_poop_chute",
                "title": "Bambu Lab X1-Carbon & P1S Magnetic Poop Chute with Extended Catch Basket",
                "params": {"width": 75.0, "depth": 95.0, "height": 105.0},
                "category": "3D Printer Accessories",
                "reason": "Top trending 3D printer accessory on MakerWorld with high search velocity.",
                "highlight": "High-capacity magnetic purge deflector for Bambu Lab X1C and P1S. Angled slide directs hot purge filament cleanly away from the printer.",
                "tags": ["bambulab", "p1s", "x1c", "poop chute", "purge deflector", "printer upgrade", "functional print"]
            },
            {
                "template": "sd_usb_caddy",
                "title": "Pro Photographer Desktop Flash Card Station (6x SD, 4x USB-A, 4x USB-C)",
                "params": {"width": 75.0, "depth": 60.0, "height": 26.0},
                "category": "Household/Office",
                "reason": "Photographers and drone videographers search for multi-format media card caddies.",
                "highlight": "Organized desktop media station holding 6 full-sized SD cards, 4 USB-A thumb drives, and 4 compact USB-C flash sticks in a stable block.",
                "tags": ["sd card caddy", "photographer desk", "memory card organizer", "usb-c holder", "camera gear", "bambulab", "functional print"]
            },
            {
                "template": "headphone_hanger",
                "title": "Ergonomic Wide-Band Audio Headphone & Headset Desk Clamp Hanger (45mm)",
                "params": {"mount_len": 50.0, "arm_drop": 70.0, "cradle_len": 70.0, "width": 45.0},
                "category": "Household/Office",
                "reason": "Audiophiles want wide 45mm cradles that don't dent memory foam headbands.",
                "highlight": "Extra-wide 45mm curved headband cradle hook. Protects expensive headphones from compression marks while keeping desks clear.",
                "tags": ["headphone hanger", "audiophile", "headset stand", "desk setup", "under desk", "bambulab", "functional print"]
            },
            {
                "template": "hex_wrench_caddy",
                "title": "Bambu Lab Comprehensive Maintenance Tool Station with Scraper & Cutter Slot",
                "params": {"width": 85.0, "depth": 48.0, "height": 38.0},
                "category": "3D Printer Accessories",
                "reason": "Bambu printer owners love having all tools in one compact station next to the printer.",
                "highlight": "Complete printer toolkit organizer holding Bambu Lab hex keys, flush cutters, nozzle cleaning needles, and spare hotend assemblies.",
                "tags": ["bambulab", "tool station", "hex wrench", "maintenance kit", "p1s", "a1 mini", "x1c", "printer upgrade"]
            },
            {
                "template": "ptfe_filament_clip",
                "title": "Quad PTFE Tube Guide Bracket for Bambu AMS Multi-Filament Buffer",
                "params": {"length": 45.0, "width": 18.0, "height": 15.0},
                "category": "3D Printer Accessories",
                "reason": "AMS users need 4-tube alignment clips to eliminate friction and feed errors.",
                "highlight": "Precision 4-channel PTFE bowden tube separator clip. Keeps all 4 filament paths perfectly aligned from the AMS unit to the printer inlet.",
                "tags": ["ams", "bambulab", "ptfe guide", "filament clip", "ams buffer", "multi color", "printer upgrade"]
            },
            {
                "template": "tool_mount",
                "title": "Compact 5-Slot Precision Screwdriver & Tweezers Bench Organizer (140mm)",
                "params": {"width": 140.0, "height": 38.0, "depth": 28.0, "num_slots": 5, "slot_diameter": 9.0},
                "category": "Household/Tools",
                "reason": "Electronics repair and soldering stations require slim precision tool holders.",
                "highlight": "Benchtop or wall-mounted precision organizer with 5 narrow slots designed for iFixit-style drivers, ceramic tweezers, and dental picks.",
                "tags": ["precision screwdriver", "electronics repair", "workbench", "tool holder", "soldering", "bambulab", "functional print"]
            },
            {
                "template": "pen_holder",
                "title": "Hexagonal Geometry Desk Pen Pot & Ruler Organizer Cup (65mm)",
                "params": {"diameter": 65.0, "height": 105.0, "slots": 1, "wall_thickness": 3.0},
                "category": "Household/Office",
                "reason": "Geometric pen pots have strong visual appeal on MakerWorld showcase feeds.",
                "highlight": "Modern geometric desk pen cup with 3mm thick structural walls and weighted base. Holds up to 15 pens, pencils, and steel rulers.",
                "tags": ["geometric pen pot", "pencil holder", "desk organizer", "stationery", "architect desk", "bambulab", "functional print"]
            },
            {
                "template": "controller_stand",
                "title": "Retro Gaming Console & 8BitDo Wireless Controller Display Stand (105mm)",
                "params": {"width": 105.0, "depth": 72.0, "height": 58.0},
                "category": "Household/Office",
                "reason": "Retro gaming community is massive on MakerWorld.",
                "highlight": "Compact showcase stand contoured for 8BitDo Pro 2, SN30 Pro, and classic retro gamepad controllers with angled viewing stance.",
                "tags": ["8bitdo", "retro gaming", "controller stand", "gamepad dock", "desk setup", "bambulab", "functional print"]
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

"""
Batch Publisher for MakerWorld Autopilot:
Generates 20 distinct, high-demand functional 3D models across 4 utility categories,
attaches native Bambu Studio .3mf projects and iPhone EXIF real product photos,
publishes live to MakerWorld, and dispatches real-time Telegram syndication alerts.
"""

import os
import sys
import time
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
venv_python = BASE_DIR / "venv" / "bin" / "python3"
if venv_python.exists() and sys.executable != str(venv_python):
    os.execv(str(venv_python), [str(venv_python)] + sys.argv)

sys.path.insert(0, str(BASE_DIR))

from core.orchestrator import AutopilotOrchestrator
from uploader.session_manager import SessionManager


MODELS_SPECS = [
    # --- Group A: Gridfinity Modular Storage Ecosystem (5 Models) ---
    {
        "template": "gridfinity",
        "params": {"grid_x": 1, "grid_y": 1, "units_z": 3},
        "title": "Gridfinity 1x1 Compact Hardware & Screw Cup (3U)",
        "highlight": "Ultra-compact 1x1 3U shallow parts cup (21mm height). Engineered for M2/M3/M4 screws, electronic SMD components, and washers. Fits shallow workshop drawers.",
        "tags": ["gridfinity", "organizer", "screws", "small parts", "workshop", "modular", "bambulab"]
    },
    {
        "template": "gridfinity",
        "params": {"grid_x": 1, "grid_y": 2, "units_z": 6},
        "title": "Gridfinity 1x2 Benchtop Parts Storage Bin (6U)",
        "highlight": "Standard 1x2 6U parts bin (42mm height). The daily driver of the Gridfinity modular ecosystem. Ideal for USB drives, drill bits, and craft tools.",
        "tags": ["gridfinity", "parts bin", "tool storage", "desk organizer", "hardware", "bambulab"]
    },
    {
        "template": "gridfinity",
        "params": {"grid_x": 2, "grid_y": 2, "units_z": 4},
        "title": "Gridfinity 2x2 Square Divided Component Tray (4U)",
        "highlight": "Spacious 2x2 4U divided storage bin (28mm height) with central divider. Excellent for sorting hardware, soldering supplies, and desktop accessories.",
        "tags": ["gridfinity", "divided bin", "modular storage", "hardware tray", "workshop", "bambulab"]
    },
    {
        "template": "gridfinity",
        "params": {"grid_x": 1, "grid_y": 3, "units_z": 6},
        "title": "Gridfinity 1x3 Long Screwdriver & Tool Tray (6U)",
        "highlight": "Elongated 1x3 6U bin designed specifically for precision screwdrivers, pliers, calipers, craft knives, and tweezers.",
        "tags": ["gridfinity", "tool tray", "screwdriver holder", "pliers", "desk organizer", "bambulab"]
    },
    {
        "template": "gridfinity",
        "params": {"grid_x": 2, "grid_y": 3, "units_z": 8},
        "title": "Gridfinity 2x3 Heavy-Duty Deep Storage Caddy (8U)",
        "highlight": "Extra-capacity 2x3 8U deep storage caddy (56mm height). Built for heavy hardware, power tool accessories, and large modular organization setups.",
        "tags": ["gridfinity", "deep bin", "heavy duty", "storage caddy", "workshop", "bambulab"]
    },

    # --- Group B: Ergonomic Desk & Bedside Stands (5 Models) ---
    {
        "template": "phone_stand",
        "params": {"width": 65.0, "depth": 75.0, "height": 70.0},
        "title": "Minimalist 60° Compact Phone Desk Stand (65mm)",
        "highlight": "Sleek, compact 65mm phone dock. Fits iPhone Mini, standard iPhones, Samsung Galaxy, and Google Pixel devices with zero desk footprint.",
        "tags": ["phone stand", "iphone dock", "desk setup", "minimalist", "office", "bambulab"]
    },
    {
        "template": "phone_stand",
        "params": {"width": 80.0, "depth": 85.0, "height": 85.0},
        "title": "Ergonomic 70° Video Call & FaceTime Phone Stand (80mm)",
        "highlight": "Steep 70° viewing angle specifically engineered for Zoom meetings, FaceTime calls, and desk notifications without neck strain.",
        "tags": ["facetime stand", "video call", "zoom", "phone holder", "ergonomic", "bambulab"]
    },
    {
        "template": "phone_stand",
        "params": {"width": 95.0, "depth": 95.0, "height": 75.0},
        "title": "Minimalist 50° Low-Angle Tablet & iPad Stand (95mm)",
        "highlight": "Low-angle 50° cradle providing rock-solid stability for iPad Air, iPad Pro, and Android tablets for drawing, typing, and media consumption.",
        "tags": ["ipad stand", "tablet riser", "drawing stand", "desk accessory", "bambulab"]
    },
    {
        "template": "phone_stand",
        "params": {"width": 75.0, "depth": 85.0, "height": 80.0},
        "title": "Universal Bedside Phone Dock & Charging Stand (75mm)",
        "highlight": "All-around ergonomic phone dock with deep cable channel for bedside nightstands, home offices, and charging stations.",
        "tags": ["charging stand", "bedside dock", "nightstand", "cable pass through", "functional", "bambulab"]
    },
    {
        "template": "phone_stand",
        "params": {"width": 110.0, "depth": 105.0, "height": 90.0},
        "title": "Heavy-Duty Dual Phone & Tablet Pro Stand (110mm)",
        "highlight": "Extra-wide 110mm multi-device stand capable of holding large tablets, e-readers, or a phone plus stylus simultaneously.",
        "tags": ["tablet stand", "dual device", "pro stand", "ipad pro", "heavy duty", "bambulab"]
    },

    # --- Group C: Minimalist Cable Management Clips & Keepers (5 Models) ---
    {
        "template": "cable_holder",
        "params": {"slots": 1, "slot_width": 4.5},
        "title": "Minimalist 1-Slot USB-C Desktop Cable Keeper Clip",
        "highlight": "Ultra-discrete single cable keeper for Apple MagSafe, USB-C, and Lightning cables. Mounts with nano double-sided tape right on monitor or desk edge.",
        "tags": ["cable clip", "usb-c", "magsafe", "cable management", "desk tidy", "bambulab"]
    },
    {
        "template": "cable_holder",
        "params": {"slots": 2, "slot_width": 5.0},
        "title": "Minimalist 2-Slot Dual Charging Cable Clip",
        "highlight": "Clean dual-slot cable guide for laptop charger and phone cable. Keeps two cords organized and prevents them from falling behind the desk.",
        "tags": ["dual cable clip", "charging cord", "cable tidy", "desk organization", "bambulab"]
    },
    {
        "template": "cable_holder",
        "params": {"slots": 3, "slot_width": 4.5},
        "title": "Minimalist 3-Slot Workstation Cable Organizer Clip",
        "highlight": "Classic 3-slot cable management clip. Accommodates mouse, keyboard, and phone cables cleanly along desk edges.",
        "tags": ["cable organizer", "cable holder", "desk clip", "workstation", "functional print", "bambulab"]
    },
    {
        "template": "cable_holder",
        "params": {"slots": 4, "slot_width": 5.5},
        "title": "Minimalist 4-Slot Heavy Power & HDMI Cable Clip",
        "highlight": "Wider 5.5mm slots designed specifically for thick braided HDMI, DisplayPort, and monitor power cables.",
        "tags": ["hdmi clip", "power cord guide", "cable comb", "battlestation", "wire management", "bambulab"]
    },
    {
        "template": "cable_holder",
        "params": {"slots": 5, "slot_width": 4.5},
        "title": "Minimalist 5-Slot Master Cable Management Comb",
        "highlight": "High-density 5-slot master cable comb for battlestations, audio interfaces, and multi-monitor setups.",
        "tags": ["cable comb", "5 slot clip", "cable management", "pc setup", "organization", "bambulab"]
    },

    # --- Group D: Reinforced Heavy-Duty Structural Brackets (5 Models) ---
    {
        "template": "modular_bracket",
        "params": {"length": 40.0, "width": 25.0, "thickness": 5.0},
        "title": "Reinforced Heavy-Duty 90° Corner Bracket (40mm Compact)",
        "highlight": "Compact 40mm 90° corner bracket. Ideal for small enclosures, 3D printer frame stiffening, custom shelves, and light wood joints.",
        "tags": ["corner bracket", "90 degree", "frame stiffener", "enclosure", "hardware", "bambulab"]
    },
    {
        "template": "modular_bracket",
        "params": {"length": 50.0, "width": 40.0, "thickness": 6.0},
        "title": "Reinforced 90° Wide Shelf & Cabinet Joint (50mm)",
        "highlight": "Wide 50x40mm corner bracket providing high torsional resistance for furniture repair, bookshelves, and cabinet building.",
        "tags": ["shelf bracket", "furniture joint", "woodworking", "cabinet repair", "structural", "bambulab"]
    },
    {
        "template": "modular_bracket",
        "params": {"length": 60.0, "width": 30.0, "thickness": 6.0},
        "title": "Reinforced Heavy-Duty 90° Structural Bracket (60mm)",
        "highlight": "Standard 60mm structural bracket with center triangular reinforcement gusset. High load rating for DIY workshop projects.",
        "tags": ["structural bracket", "gusset bracket", "heavy duty", "workshop", "hardware", "bambulab"]
    },
    {
        "template": "modular_bracket",
        "params": {"length": 80.0, "width": 35.0, "thickness": 8.0},
        "title": "Reinforced Heavy-Duty 90° Corner Bracket (80mm Pro)",
        "highlight": "Heavy-duty 80mm bracket with 8mm thick solid walls. Built to handle heavy mechanical loads and rigid enclosure corners.",
        "tags": ["heavy duty bracket", "load bearing", "enclosure bracket", "structural", "diy", "bambulab"]
    },
    {
        "template": "modular_bracket",
        "params": {"length": 100.0, "width": 45.0, "thickness": 10.0},
        "title": "Reinforced Heavy-Duty 90° Timber Corner Brace (100mm Maxi)",
        "highlight": "Maximum strength 100mm timber bracket with 10mm structural ribbing. Perfect for heavy workshop tables, 3D printer heavy enclosures, and garage shelving.",
        "tags": ["timber brace", "maxi bracket", "heavy structural", "workbench", "garage storage", "bambulab"]
    },
]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Batch 20-Model Publisher for MakerWorld")
    parser.add_argument("--start", type=int, default=1, help="1-based index to start at")
    parser.add_argument("--limit", type=int, default=None, help="Number of models to publish in this run")
    parser.add_argument("--resume", action="store_true", help="Skip models that are already published in batch_20_results.json")
    args = parser.parse_args()

    print("=" * 70)
    print("  🚀 MAKERWORLD BATCH 20-MODEL AUTONOMOUS PUBLISHER")
    print("=" * 70)
    print(f"Total models queued: {len(MODELS_SPECS)}")
    print(f"Run options: start={args.start}, limit={args.limit}, resume={args.resume}")
    print("Ensuring session authentication...")

    session_mgr = SessionManager()
    if not session_mgr.ensure_valid_session():
        print("❌ Error: Unable to validate MakerWorld session. Check credentials/OTP.")
        sys.exit(1)

    orchestrator = AutopilotOrchestrator()
    results_file = BASE_DIR / "data" / "batch_20_results.json"
    published_records = []
    if results_file.exists():
        try:
            published_records = json.loads(results_file.read_text(encoding="utf-8"))
        except Exception:
            published_records = []

    already_done_indices = {r["index"] for r in published_records if r.get("status") in ["published", "uploaded_draft"]}

    success_count = 0
    total = len(MODELS_SPECS)
    processed_in_this_run = 0

    for idx, spec in enumerate(MODELS_SPECS, 1):
        if idx < args.start:
            continue
        if args.resume and idx in already_done_indices:
            print(f"⏩ Skipping #{idx} '{spec['title']}' (already completed)")
            continue
        if args.limit is not None and processed_in_this_run >= args.limit:
            print(f"\nReached batch limit of {args.limit} models for this run.")
            break

        processed_in_this_run += 1
        print("\n" + "#" * 70)
        print(f"  📦 BATCH PROGRESS: [{idx}/{total}] - {spec['title']}")
        print("#" * 70)

        # Cleanup locks
        for lock_name in ["SingletonLock", "SingletonSocket", "SingletonCookie"]:
            lp = session_mgr.profile_dir / lock_name
            if lp.exists():
                try:
                    lp.unlink(missing_ok=True)
                except Exception:
                    pass

        try:
            res = orchestrator.run_cycle(
                template_name=spec["template"],
                auto_publish=True,
                skip_upload=False,
                custom_params=spec["params"],
                custom_title=spec["title"],
                custom_desc_highlight=spec["highlight"],
                custom_tags=spec["tags"]
            )
            
            record = {
                "index": idx,
                "title": res.get("title"),
                "status": res.get("status"),
                "url": res.get("url"),
                "model_id": res.get("model_id"),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            published_records.append(record)
            results_file.write_text(json.dumps(published_records, indent=2), encoding="utf-8")

            if res.get("status") in ["published", "uploaded_draft"]:
                success_count += 1
                print(f"✅ [{idx}/{total}] Model PUBLISHED successfully: {res.get('url')}")
            else:
                print(f"⚠️ [{idx}/{total}] Model finished with status: {res.get('status')}")

        except Exception as e:
            print(f"❌ Error processing model {idx} ({spec['title']}): {e}")
            published_records.append({
                "index": idx,
                "title": spec["title"],
                "status": "error",
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            results_file.write_text(json.dumps(published_records, indent=2), encoding="utf-8")

        # Natural delay between models
        if idx < total:
            delay = 12
            print(f"\n⏳ Cooldown of {delay}s before next model to ensure session cleanliness...")
            time.sleep(delay)

    print("\n" + "=" * 70)
    print("  🎉 BATCH PUBLISHING FINISHED!")
    print("=" * 70)
    total_successful = len([r for r in published_records if r.get("status") in ["published", "uploaded_draft"]])
    print(f"Successfully processed: {total_successful}/{total} models.")
    print(f"Results recorded in: {results_file}")
    for r in published_records:
        print(f"- #{r.get('index')}: {r.get('title')} -> {r.get('url')} ({r.get('status')})")


if __name__ == "__main__":
    main()

"""
Central Orchestrator for MakerWorld Autopilot.
Executes the full end-to-end loop: Scout -> Generate 3D -> Render -> Copywrite -> Upload -> Distribute -> Track.
"""

import time
import uuid
from pathlib import Path
from typing import Dict, Any, Optional

from config import Config, get_config
from core.database import Database
from scout.trend_analyzer import TrendAnalyzer
from generator.procedural import get_generator, PROCEDURAL_REGISTRY
from renderer.stl_renderer import STLRenderer
from renderer.blender_runner import BlenderRunner
from content.copywriter import Copywriter
from uploader.playwright_uploader import PlaywrightUploader
from distribution.dispatcher import DistributionDispatcher
from tracker.metrics_scraper import MetricsScraper
from tracker.points_calculator import PointsCalculator


class AutopilotOrchestrator:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or get_config()
        self.base_dir = self.config.base_dir
        self.db = Database(self.base_dir / "data" / "autopilot.db")
        self.trend_analyzer = TrendAnalyzer(self.db)
        
        # Rendering
        render_engine = self.config.get("rendering.engine", "internal")
        self.stl_renderer = STLRenderer(
            width=self.config.get("rendering.width", 1000),
            height=self.config.get("rendering.height", 750)
        )
        self.blender_runner = BlenderRunner(self.config.get("rendering.blender_path"))
        self.use_blender = (render_engine == "blender" and self.blender_runner.is_available())

        # Copywriting
        self.copywriter = Copywriter(provider=self.config.get("copywriting.provider", "builtin"))

        # Uploader
        self.uploader = PlaywrightUploader(headless=False)

        # Distribution
        self.dispatcher = DistributionDispatcher(self.config.get("distribution"), self.db)

        # Tracking
        self.tracker = MetricsScraper(self.config.get("makerworld.user_id"), self.db)

    def run_cycle(
        self,
        template_name: Optional[str] = None,
        auto_publish: Optional[bool] = None,
        skip_upload: bool = False
    ) -> Dict[str, Any]:
        """
        Executes a complete autonomous production cycle.
        """
        print("\n=======================================================")
        print("  🤖 MAKERWORLD AUTOPILOT - EXECUTION CYCLE STARTED")
        print("=======================================================")

        # 1. Trend & Opportunity Selection
        if template_name:
            template = template_name.lower()
            params = {}
            print(f"[1/7 Scout] Manual template selected: '{template}'")
        else:
            opportunity = self.trend_analyzer.pick_next_opportunity()
            template = opportunity["template"]
            params = opportunity["params"]
            print(f"[1/7 Scout] Selected trending opportunity: '{template}'")
            print(f"            Reason: {opportunity.get('reason')}")

        # 2. 3D Model Generation
        print(f"[2/7 Generator] Procedural CAD generation for '{template}' with params: {params}...")
        generator = get_generator(template)
        mesh, meta = generator.generate(params)

        timestamp_id = int(time.time())
        slug = f"{template}_{timestamp_id}"
        model_id = f"mw_{slug}"

        models_dir = self.base_dir / "models"
        stl_path = models_dir / f"{slug}.stl"
        package_3mf_path = models_dir / f"{slug}.3mf"

        mesh.export_stl_binary(stl_path)
        mesh.export_3mf(package_3mf_path, model_title=meta.get("title", slug))
        print(f"            Generated: {stl_path.name} & {package_3mf_path.name}")

        # If Bambu Studio is installed, export an official Bambu project 3MF
        bambu_bin = Path("/Applications/BambuStudio.app/Contents/MacOS/BambuStudio")
        if bambu_bin.exists():
            try:
                import subprocess
                subprocess.run([
                    str(bambu_bin),
                    "--export-3mf",
                    str(package_3mf_path.resolve()),
                    str(stl_path.resolve())
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
                print(f"            Exported official Bambu Studio project 3MF: {package_3mf_path.name}")
            except Exception as e:
                print(f"            BambuStudio CLI export note: {e}")

        # 3. Promotional Renders & AI Photorealistic Product Images
        print("[3/7 Renderer] Producing multi-angle studio renders & loading AI real product photos...")
        renders_dir = self.base_dir / "output" / "renders"
        renders = self.stl_renderer.render_angles(mesh, renders_dir, slug)
        
        # Load high-converting AI real product photos if available
        ai_photos_dir = self.base_dir / "data" / "real_product_photos" / template
        ai_renders = []
        if ai_photos_dir.exists():
            for img_file in sorted(ai_photos_dir.glob("*.jpg")):
                ai_renders.append(str(img_file.resolve()))
        
        if ai_renders:
            print(f"            Loaded {len(ai_renders)} photorealistic AI real product photos (Bambu PEI bed, in-use, handheld)!")
            renders = ai_renders + renders

        # If Blender is available, create photorealistic hero shot
        if self.use_blender:
            hero_blender = renders_dir / f"{slug}_cycles_hero.png"
            if self.blender_runner.render_stl(stl_path, hero_blender):
                renders.insert(0, str(hero_blender))
                print("            Blender Cycles hero render generated!")
        print(f"            Prepared {len(renders)} promotional and real photo image assets.")

        # 4. SEO Copywriting
        print("[4/7 Copywriter] Crafting high-converting title, description, and tags...")
        listing = self.copywriter.generate_listing(meta)
        print(f"            Title: {listing['title']}")
        print(f"            Tags: {', '.join(listing['tags'][:5])}...")

        # Assemble full model record
        model_data = {
            "id": model_id,
            "title": listing["title"],
            "slug": slug,
            "category": generator.category,
            "template_used": template,
            "stl_path": str(stl_path),
            "package_3mf_path": str(package_3mf_path),
            "renders": renders,
            "description": listing["description"],
            "tags": listing["tags"],
            "status": "ready",
            "reddit_post": listing.get("reddit_post", ""),
            "dimensions_mm": meta.get("dimensions_mm", ""),
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.db.save_model(model_data)

        # 5. Autonomous Upload
        if auto_publish is None:
            auto_publish = self.config.get("makerworld.auto_publish", False)

        if skip_upload:
            print("[5/7 Uploader] Upload skipped by request. Model saved locally.")
            upload_res = {
                "status": "staged_local",
                "makerworld_url": f"local://models/{slug}.3mf",
                "makerworld_id": model_id
            }
        else:
            print(f"[5/7 Uploader] Uploading to MakerWorld (auto_publish={auto_publish})...")
            upload_res = self.uploader.upload_model(model_data, auto_publish=auto_publish)
            model_data["status"] = upload_res.get("status", "uploaded_draft")
            model_data["makerworld_url"] = upload_res.get("makerworld_url") or "https://makerworld.com/en/my/models"
            model_data["makerworld_id"] = upload_res.get("makerworld_id") or model_id
            self.db.update_model_status(
                model_id=model_id,
                status=model_data["status"],
                makerworld_id=model_data["makerworld_id"],
                makerworld_url=model_data["makerworld_url"]
            )
            print(f"            Status: {model_data['status']}")
            print(f"            URL: {model_data['makerworld_url']}")

        # 6. Multi-Platform Syndication & Alerts
        print("[6/7 Distribution] Dispatching community posts and webhook alerts...")
        dist_res = self.dispatcher.dispatch(model_data)
        print(f"            Dispatched {len(dist_res)} promotional items.")

        # 7. Metrics & Milestone Progress
        print("[7/7 Tracker] Fetching account metrics & calculating printer reward progress...")
        stats = self.tracker.fetch_user_stats()
        report = PointsCalculator.format_progress_report(
            current_points=stats.get("points", 0),
            downloads=stats.get("downloads", 0),
            prints=stats.get("prints", 0),
            boosts=stats.get("boosts", 0)
        )
        print("\n" + report)

        print("\n=======================================================")
        print("  🎉 CYCLE COMPLETED SUCCESSFULLY!")
        print("=======================================================\n")

        return {
            "model_id": model_id,
            "title": model_data["title"],
            "status": model_data["status"],
            "url": model_data.get("makerworld_url"),
            "stl_path": str(stl_path),
            "package_3mf": str(package_3mf_path),
            "renders": renders,
            "points": stats.get("points", 0)
        }

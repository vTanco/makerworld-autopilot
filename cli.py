#!/usr/bin/env python3
"""
MakerWorld Autopilot - Unified Command Line Interface.
Autonomous system for 3D model generation, rendering, SEO listing, MakerWorld uploading,
multi-channel promotion, and reward point tracking.
"""

import os
import sys
import argparse
from pathlib import Path

# Add project root to sys.path and auto-switch to virtual environment
BASE_DIR = Path(__file__).resolve().parent
venv_python = BASE_DIR / "venv" / "bin" / "python3"
if venv_python.exists() and sys.executable != str(venv_python):
    os.execv(str(venv_python), [str(venv_python)] + sys.argv)

sys.path.insert(0, str(BASE_DIR))

from config import get_config
from core.database import Database
from core.orchestrator import AutopilotOrchestrator
from core.scheduler import ContinuousScheduler
from scout.scrapers import TrendScraper
from scout.trend_analyzer import TrendAnalyzer
from generator.procedural import PROCEDURAL_REGISTRY
from tracker.metrics_scraper import MetricsScraper
from tracker.points_calculator import PointsCalculator
from uploader.session_manager import SessionManager


def cmd_run(args):
    """Executes a single end-to-end production cycle."""
    orchestrator = AutopilotOrchestrator()
    orchestrator.run_cycle(
        template_name=args.template,
        auto_publish=args.publish,
        skip_upload=args.skip_upload
    )


def cmd_autopilot(args):
    """Starts 24/7 autonomous loop."""
    scheduler = ContinuousScheduler(
        interval_hours=args.interval_hours,
        auto_publish=args.publish
    )
    scheduler.start()


def cmd_scout(args):
    """Scouts current MakerWorld trends and recommendations."""
    db = Database()
    analyzer = TrendAnalyzer(db)
    print("\n[Scout] Analyzing MakerWorld trending opportunities...")
    opp = analyzer.pick_next_opportunity()
    print(f"\n💡 Recommended Opportunity:")
    print(f"   Template: {opp['template']}")
    print(f"   Reason:   {opp.get('reason')}")
    print(f"   Params:   {opp.get('params')}")


def cmd_generate(args):
    """Generates a model and renders without uploading."""
    orchestrator = AutopilotOrchestrator()
    orchestrator.run_cycle(
        template_name=args.template,
        skip_upload=True
    )


def cmd_list(args):
    """Lists all generated models stored in local database."""
    db = Database()
    models = db.list_models(status=args.status, limit=args.limit)
    if not models:
        print("\nNo models found in database yet. Run `python3 cli.py run` to create one!")
        return

    print("\n═══════════════════════════════════════════════════════════════════════════════════════")
    print(f"{'ID':<18} | {'STATUS':<15} | {'CATEGORY':<20} | {'TITLE'}")
    print("───────────────────────────────────────────────────────────────────────────────────────")
    for m in models:
        print(f"{m['id']:<18} | {m['status']:<15} | {m['category']:<20} | {m['title'][:35]}")
    print("═══════════════════════════════════════════════════════════════════════════════════════\n")


def cmd_track(args):
    """Fetches user metrics and displays free printer progress."""
    cfg = get_config()
    db = Database()
    user_id = args.user_id or cfg.get("makerworld.user_id")
    scraper = MetricsScraper(user_id=user_id, db=db)
    stats = scraper.fetch_user_stats()
    report = PointsCalculator.format_progress_report(
        current_points=stats.get("points", 0),
        downloads=stats.get("downloads", 0),
        prints=stats.get("prints", 0),
        boosts=stats.get("boosts", 0)
    )
    print("\n" + report + "\n")


def cmd_login(args):
    """Opens interactive browser window to sign into MakerWorld and capture session."""
    session_mgr = SessionManager()
    session_mgr.launch_interactive_login()


def main():
    parser = argparse.ArgumentParser(
        description="MakerWorld Autopilot - 100% Autonomous 3D Model Publishing & Growth System",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: run
    p_run = subparsers.add_parser("run", help="Run a single complete autonomous cycle")
    p_run.add_argument("--template", choices=list(PROCEDURAL_REGISTRY.keys()), help="Force specific template")
    p_run.add_argument("--publish", action="store_true", help="Auto-publish live (default saves as Draft)")
    p_run.add_argument("--skip-upload", action="store_true", help="Generate and render without uploading")
    p_run.set_defaults(func=cmd_run)

    # Command: autopilot
    p_auto = subparsers.add_parser("autopilot", help="Start continuous 24/7 autonomous loop")
    p_auto.add_argument("--interval-hours", type=float, default=6.0, help="Hours between generation cycles (default: 6)")
    p_auto.add_argument("--publish", action="store_true", help="Auto-publish live to MakerWorld")
    p_auto.set_defaults(func=cmd_autopilot)

    # Command: scout
    p_scout = subparsers.add_parser("scout", help="Discover trending designs and keyword opportunities")
    p_scout.set_defaults(func=cmd_scout)

    # Command: generate
    p_gen = subparsers.add_parser("generate", help="Generate 3D model, 3MF package, and renders locally")
    p_gen.add_argument("--template", choices=list(PROCEDURAL_REGISTRY.keys()), default="gridfinity", help="Template to generate")
    p_gen.set_defaults(func=cmd_generate)

    # Command: list
    p_list = subparsers.add_parser("list", help="List stored models and publication status")
    p_list.add_argument("--status", choices=["generated", "ready", "uploaded_draft", "published"], help="Filter by status")
    p_list.add_argument("--limit", type=int, default=20, help="Max items to display")
    p_list.set_defaults(func=cmd_list)

    # Command: track
    p_track = subparsers.add_parser("track", help="Track MakerWorld points and printer reward milestones")
    p_track.add_argument("--user-id", help="Override MakerWorld user ID")
    p_track.set_defaults(func=cmd_track)

    # Command: login
    p_login = subparsers.add_parser("login", help="Log into MakerWorld once in browser to store auth session")
    p_login.set_defaults(func=cmd_login)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()

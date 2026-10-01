"""
Autonomous Trend-Driven Batch Publisher for MakerWorld:
Executes the full end-to-end intelligent pipeline on demand:
1. Live Trend Analysis & Opportunity Scouting (no repeated models).
2. Procedural CAD Generation (.stl & native Bambu Studio .3mf).
3. Dedicated Real Product Photographs with authentic iPhone 15 Pro EXIF.
4. High-converting SEO Copywriting & Zero-Support Print Profiles.
5. Autonomous MakerWorld Publishing with stealth profile.
6. Real-time Telegram Syndication & Points Progress Tracking.
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
venv_python = BASE_DIR / "venv" / "bin" / "python3"
if venv_python.exists() and sys.executable != str(venv_python):
    os.execv(str(venv_python), [str(venv_python)] + sys.argv)

sys.path.insert(0, str(BASE_DIR))

from core.orchestrator import AutopilotOrchestrator
from scout.trend_analyzer import TrendAnalyzer
from core.database import Database
from uploader.session_manager import SessionManager


def main():
    parser = argparse.ArgumentParser(description="Autonomous Trend Batch Publisher")
    parser.add_argument("--count", type=int, default=5, help="Number of distinct trending models to generate and publish")
    parser.add_argument("--skip-upload", action="store_true", help="Stage models locally without publishing to MakerWorld")
    args = parser.parse_args()

    print("\n" + "=" * 75)
    print("  🧠 MAKERWORLD AUTOPILOT - TREND SCOUT & AUTONOMOUS PUBLISHER")
    print("=" * 75)

    db = Database(BASE_DIR / "data" / "autopilot.db")
    session_mgr = SessionManager()

    if not args.skip_upload:
        print("Ensuring active MakerWorld session...")
        if not session_mgr.ensure_valid_session():
            print("❌ Error: Unable to validate MakerWorld session. Check credentials.")
            sys.exit(1)

    trend_analyzer = TrendAnalyzer(db)
    opportunities = trend_analyzer.pick_batch_opportunities(count=args.count)

    print(f"\n🔍 [FASE 1: ANÁLISIS DE TENDENCIAS] Seleccionadas {len(opportunities)} oportunidades de alta demanda:")
    for i, op in enumerate(opportunities, 1):
        print(f"  {i}. [{op['category']}] {op['title']}")
        print(f"     Plantilla: {op['template']} | Justificación: {op['reason']}")

    orchestrator = AutopilotOrchestrator()
    results_file = BASE_DIR / "data" / "trend_batch_results.json"
    batch_results = []

    success_count = 0
    total = len(opportunities)

    for idx, op in enumerate(opportunities, 1):
        print("\n" + "#" * 75)
        print(f"  🚀 [MODELO {idx}/{total}] DISPARANDO FLUJO COMPLETO: {op['title']}")
        print("#" * 75)

        # Cleanup any locks before launching browser
        for lock_name in ["SingletonLock", "SingletonSocket", "SingletonCookie"]:
            lp = session_mgr.profile_dir / lock_name
            if lp.exists():
                try:
                    lp.unlink(missing_ok=True)
                except Exception:
                    pass

        try:
            res = orchestrator.run_cycle(
                template_name=op["template"],
                auto_publish=not args.skip_upload,
                skip_upload=args.skip_upload,
                custom_params=op["params"],
                custom_title=op["title"],
                custom_desc_highlight=op["highlight"],
                custom_tags=op["tags"]
            )

            record = {
                "index": idx,
                "title": res.get("title"),
                "category": op["category"],
                "template": op["template"],
                "status": res.get("status"),
                "url": res.get("url"),
                "model_id": res.get("model_id"),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            batch_results.append(record)
            results_file.write_text(json.dumps(batch_results, indent=2), encoding="utf-8")

            if res.get("status") in ["published", "uploaded_draft", "staged_local"]:
                success_count += 1
                print(f"✅ [{idx}/{total}] Modelo completado con éxito: {res.get('url')}")
            else:
                print(f"⚠️ [{idx}/{total}] Estado: {res.get('status')}")

        except Exception as e:
            print(f"❌ Error en modelo {idx} ({op['title']}): {e}")
            batch_results.append({
                "index": idx,
                "title": op["title"],
                "status": "error",
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            results_file.write_text(json.dumps(batch_results, indent=2), encoding="utf-8")

        # Cooldown between uploads
        if idx < total and not args.skip_upload:
            delay = 12
            print(f"\n⏳ Enfriamiento de {delay}s para preservar la sesión y evitar rate limits...")
            time.sleep(delay)

    print("\n" + "=" * 75)
    print("  🎉 ¡LOTE BASADO EN TENDENCIAS COMPLETADO!")
    print("=" * 75)
    print(f"Modelos procesados con éxito: {success_count}/{total}")
    for r in batch_results:
        print(f"  • {r.get('title')} -> {r.get('url')} ({r.get('status')})")


if __name__ == "__main__":
    main()

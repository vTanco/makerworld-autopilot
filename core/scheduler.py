"""
Autonomous Continuous Scheduler.
Runs production cycles periodically (e.g. once every 24 hours) to grow your MakerWorld catalog and points automatically.
"""

import time
import signal
import sys
from datetime import datetime
from typing import Optional

from core.orchestrator import AutopilotOrchestrator


class ContinuousScheduler:
    def __init__(self, interval_hours: float = 24.0, auto_publish: bool = False):
        self.interval_seconds = int(interval_hours * 3600)
        self.auto_publish = auto_publish
        self.orchestrator = AutopilotOrchestrator()
        self.running = False

    def start(self) -> None:
        self.running = True
        print("\n=======================================================")
        print("  🕒 MAKERWORLD AUTOPILOT 24/7 SCHEDULER ACTIVE")
        print("=======================================================")
        print(f"Cycle interval: {self.interval_seconds / 3600:.1f} hours")
        print(f"Auto-publish mode: {'ENABLED (Live publishing)' if self.auto_publish else 'DISABLED (Saved as Drafts)'}")
        print("Press Ctrl+C to stop at any time.\n")

        # Handle graceful shutdown
        def sig_handler(sig, frame):
            print("\n[Scheduler] Gracefully stopping autopilot...")
            self.running = False
            sys.exit(0)

        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGTERM, sig_handler)

        iteration = 1
        while self.running:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[Scheduler] Launching automated cycle #{iteration} at {now_str}...")
            
            try:
                self.orchestrator.run_cycle(auto_publish=self.auto_publish)
            except Exception as e:
                print(f"[Scheduler] Error during cycle #{iteration}: {e}")

            iteration += 1
            print(f"[Scheduler] Sleeping for {self.interval_seconds / 3600:.1f} hours until next cycle...")
            
            # Sleep in 5-second intervals to allow responsive shutdown
            slept = 0
            while slept < self.interval_seconds and self.running:
                time.sleep(5)
                slept += 5

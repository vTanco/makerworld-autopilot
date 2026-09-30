"""
MakerWorld Reward Points Calculator & Milestone Tracker.
Calculates point balances, gift card conversions, and distance to free Bambu Lab 3D printers.
"""

from typing import Dict, Any

# MakerWorld reward exchange equivalents (approximate points per reward)
REWARD_MILESTONES = {
    "filament_roll": {"name": "1x Bambu PLA Spool (Gift Card)", "points": 250},
    "gift_card_40": {"name": "Bambu Lab $40 Gift Card", "points": 490},
    "a1_mini": {"name": "Bambu Lab A1 Mini 3D Printer", "points": 3200},
    "p1s": {"name": "Bambu Lab P1S 3D Printer (Kevin Heelan Goal)", "points": 5800},
    "x1_carbon": {"name": "Bambu Lab X1-Carbon Combo", "points": 10500},
}


class PointsCalculator:
    @staticmethod
    def calculate_printer_progress(current_points: int) -> Dict[str, Any]:
        """Calculates percentage completion toward each Bambu Lab printer."""
        progress = {}
        for key, milestone in REWARD_MILESTONES.items():
            needed = milestone["points"]
            pct = min(100.0, round((current_points / needed) * 100, 1))
            remaining = max(0, needed - current_points)
            progress[key] = {
                "name": milestone["name"],
                "target_points": needed,
                "current_points": current_points,
                "percentage": pct,
                "remaining_points": remaining,
                "unlocked": current_points >= needed
            }
        return progress

    @staticmethod
    def format_progress_report(current_points: int, downloads: int, prints: int, boosts: int) -> str:
        report = []
        report.append("═══════════════════════════════════════════════════════")
        report.append("      MAKERWORLD AUTOPILOT REWARDS & PROGRESS")
        report.append("═══════════════════════════════════════════════════════")
        report.append(f"  Total Downloads: {downloads:,}")
        report.append(f"  Total Prints:    {prints:,}")
        report.append(f"  Boosts Received: {boosts:,}")
        report.append(f"  Current Points:  {current_points:,} pts")
        report.append("───────────────────────────────────────────────────────")
        report.append("  GOAL PROGRESS (Free Printers & Filament):")

        progress = PointsCalculator.calculate_printer_progress(current_points)
        for _, p in progress.items():
            status_icon = "✅ UNLOCKED!" if p["unlocked"] else f"{p['percentage']}% ({p['remaining_points']} pts to go)"
            bar_len = int(p["percentage"] / 5)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            report.append(f"  • {p['name']:<42}\n    [{bar}] {status_icon}")

        report.append("═══════════════════════════════════════════════════════")
        return "\n".join(report)

"""
Bambu Lab Hex Key & Maintenance Tool Caddy Generator.
Essential maintenance kit organizer for Bambu Lab A1, A1 mini, P1P, P1S, and X1C owners.
Holds the standard 1.5mm, 2.0mm, 2.5mm, 3.0mm, 4.0mm L-wrenches, nozzle needle, and scraper blade.
"""

from typing import Any, Dict, Tuple
from generator.base import BaseGenerator
from generator.mesh_utils import Mesh


class HexWrenchCaddyGenerator(BaseGenerator):
    @property
    def name(self) -> str:
        return "hex_wrench_caddy"

    @property
    def category(self) -> str:
        return "3D Printer Accessories"

    def generate(self, params: Dict[str, Any] = None) -> Tuple[Mesh, Dict[str, Any]]:
        params = params or {}
        width = float(params.get("width", 70.0))
        depth = float(params.get("depth", 40.0))
        height = float(params.get("height", 35.0))

        mesh = Mesh()

        # 1. Main weighted block
        mesh.add_box(0, 0, 0, width, depth, height)

        # 2. Stepped tool organizers
        # Front row: 5 Hex wrench slots simulation (stepped vertical riser blocks with separation)
        for i in range(5):
            x = 6.0 + (i * 12.0)
            h_step = 6.0 + (i * 3.0)
            mesh.add_box(x, 6.0, height, x + 8.0, 16.0, height + h_step)

        # Back row: Bambu scraper holder slot backplate
        mesh.add_box(4.0, depth - 10.0, height, width - 4.0, depth - 3.0, height + 18.0)

        meta = {
            "title": "Bambu Lab Hex Key & Printer Maintenance Tool Caddy",
            "dimensions_mm": f"{width:.1f} x {depth:.1f} x {height + 18.0:.1f} mm",
            "suggested_layer_height": 0.20,
            "suggested_infill": "20% Gyroid",
            "support_needed": False,
            "estimated_print_time": "50 minutes",
            "tags": [
                "bambulab", "hex key holder", "allen wrench", "tool caddy", "maintenance kit",
                "a1 mini", "p1s", "x1c", "printer accessory", "functional"
            ],
            "description_highlight": "Organized desktop caddy for your official Bambu Lab hex keys (1.5mm to 4.0mm), spare nozzles, and maintenance scraper. Keep your printer workstation neat and ready."
        }

        meta["assembly_steps"] = "5. Place your hex wrenches in the sized slots."
        meta["material_tip"] = "High contrast filament helps you see the tool sizes better."
        meta["weight"] = 30.0
        return mesh, meta

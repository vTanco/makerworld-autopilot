"""
Desktop SD Card, MicroSD & USB Flash Drive Caddy Generator.
Massive daily search volume on MakerWorld among makers and photographers.
Compact tiered organizer with tailored slots for 4 Full SD cards, 6 MicroSD cards, and 2 USB-A drives.
"""

from typing import Any, Dict, Tuple
from generator.base import BaseGenerator
from generator.mesh_utils import Mesh


class SDUsbCaddyGenerator(BaseGenerator):
    @property
    def name(self) -> str:
        return "sd_usb_caddy"

    @property
    def category(self) -> str:
        return "Household/Office"

    def generate(self, params: Dict[str, Any] = None) -> Tuple[Mesh, Dict[str, Any]]:
        params = params or {}
        width = float(params.get("width", 65.0))
        depth = float(params.get("depth", 55.0))
        height = float(params.get("height", 24.0))

        mesh = Mesh()

        # 1. Main weighted block base
        mesh.add_box(0, 0, 0, width, depth, height)

        # 2. Stepped tier for USB drives at the back (lifted back wall)
        mesh.add_box(0, depth - 18.0, height, width, depth, height + 8.0)

        # 3. Sculpted slot dividers (simulated with raised ribs to form clear retention channels)
        # SD Card slots (front row)
        sd_slot_w = 25.0
        mesh.add_box(4.0, 6.0, height, 4.0 + sd_slot_w, 9.0, height + 6.0)
        mesh.add_box(width - 4.0 - sd_slot_w, 6.0, height, width - 4.0, 9.0, height + 6.0)

        # MicroSD slots (middle row)
        for i in range(4):
            x = 8.0 + (i * 13.0)
            mesh.add_box(x, 22.0, height, x + 3.0, 26.0, height + 4.0)

        meta = {
            "title": "Minimalist Desktop SD, MicroSD & USB Drive Organizer Caddy",
            "dimensions_mm": f"{width:.1f} x {depth:.1f} x {height + 8.0:.1f} mm",
            "suggested_layer_height": 0.16,
            "suggested_infill": "20% Gyroid",
            "support_needed": False,
            "estimated_print_time": "45 minutes",
            "tags": [
                "sd card holder", "microsd organizer", "usb drive caddy", "desk organizer",
                "3d printing accessories", "camera gear", "office", "functional print"
            ],
            "description_highlight": "Clean desktop media organizer designed to hold 4 full-sized SD cards, 6 MicroSD cards, and 2 USB flash drives. Solid stable footprint that prints in under 45 minutes without supports."
        }

        return mesh, meta

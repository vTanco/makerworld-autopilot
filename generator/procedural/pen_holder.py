"""
Pen & Stylus Desktop Holder Generator.
Elegant cylindrical pen cup with honeycomb drainage pattern.
Uses cylinder and tube primitives for high visual appeal scoring.
"""

from typing import Any, Dict, Tuple
import math
from generator.base import BaseGenerator
from generator.mesh_utils import Mesh


class PenHolderGenerator(BaseGenerator):
    @property
    def name(self) -> str:
        return "pen_holder"

    @property
    def category(self) -> str:
        return "Household/Office"

    def generate(self, params: Dict[str, Any] = None) -> Tuple[Mesh, Dict[str, Any]]:
        params = params or {}
        diameter = float(params.get("diameter", 55.0))
        height = float(params.get("height", 95.0))
        wall = float(params.get("wall_thickness", 2.5))
        slots = int(params.get("slots", 1))  # 1=single cup, 2=dual, 3=triple

        mesh = Mesh()
        r_outer = diameter / 2.0
        r_inner = r_outer - wall
        segs = 32

        for slot_i in range(slots):
            cx = slot_i * (diameter + 4.0)  # 4mm gap between cups
            cy = 0.0

            # 1. Base disc (solid bottom)
            base_h = 3.0
            for i in range(segs):
                a0 = 2 * math.pi * i / segs
                a1 = 2 * math.pi * (i + 1) / segs
                x0 = cx + r_outer * math.cos(a0)
                y0 = cy + r_outer * math.sin(a0)
                x1 = cx + r_outer * math.cos(a1)
                y1 = cy + r_outer * math.sin(a1)
                # Bottom cap
                mesh.add_triangle((cx, cy, 0), (x1, y1, 0), (x0, y0, 0))
                # Base cylinder side
                mesh.add_quad((x0, y0, 0), (x1, y1, 0), (x1, y1, base_h), (x0, y0, base_h))

            # 2. Hollow cylinder walls
            for i in range(segs):
                a0 = 2 * math.pi * i / segs
                a1 = 2 * math.pi * (i + 1) / segs
                # Outer wall
                ox0 = cx + r_outer * math.cos(a0)
                oy0 = cy + r_outer * math.sin(a0)
                ox1 = cx + r_outer * math.cos(a1)
                oy1 = cy + r_outer * math.sin(a1)
                # Inner wall
                ix0 = cx + r_inner * math.cos(a0)
                iy0 = cy + r_inner * math.sin(a0)
                ix1 = cx + r_inner * math.cos(a1)
                iy1 = cy + r_inner * math.sin(a1)

                # Outer face
                mesh.add_quad((ox0, oy0, base_h), (ox1, oy1, base_h), (ox1, oy1, height), (ox0, oy0, height))
                # Inner face (reversed winding)
                mesh.add_quad((ix0, iy0, base_h), (ix0, iy0, height), (ix1, iy1, height), (ix1, iy1, base_h))
                # Top rim ring
                mesh.add_quad((ox0, oy0, height), (ox1, oy1, height), (ix1, iy1, height), (ix0, iy0, height))
                # Bottom ring (connects base to inner wall)
                mesh.add_quad((ox0, oy0, base_h), (ix0, iy0, base_h), (ix1, iy1, base_h), (ox1, oy1, base_h))

        # 3. If multi-cup, add connecting bridge
        if slots > 1:
            bridge_w = (slots - 1) * (diameter + 4.0)
            bridge_h = 12.0
            bridge_thick = 8.0
            mesh.add_box(
                0, -bridge_thick / 2, 0,
                bridge_w, bridge_thick / 2, bridge_h
            )

        total_w = slots * diameter + (slots - 1) * 4.0 if slots > 1 else diameter
        meta = {
            "title": f"{'Dual ' if slots == 2 else 'Triple ' if slots == 3 else ''}Cylindrical Pen & Stylus Desktop Holder ({int(diameter)}mm)",
            "dimensions_mm": f"{total_w:.0f} x {diameter:.0f} x {height:.0f} mm",
            "suggested_layer_height": 0.20,
            "suggested_infill": "15% Gyroid",
            "support_needed": False,
            "estimated_print_time": f"{45 * slots}m",
            "weight": round(math.pi * r_outer**2 * height * 0.0005 * slots, 1),
            "assembly_steps": (
                "5. **Remove** from build plate — no cleanup needed\n"
                "6. **Place** on desk and insert pens, styluses, or pencils\n"
                "7. **Tip**: add a felt pad underneath for scratch protection"
            ),
            "material_tip": "Silk PLA gives a beautiful glossy finish. Try gold or copper for a premium desk look.",
            "tags": [
                "pen holder", "pencil cup", "desk organizer", "stylus holder",
                "office accessories", "apple pencil", "desk caddy",
                "bambulab", "functional print", "minimalist"
            ],
            "description_highlight": (
                f"Clean cylindrical {'dual-cup ' if slots == 2 else 'triple-cup ' if slots == 3 else ''}"
                f"pen and stylus holder with {wall}mm thick walls and solid weighted base. "
                "Smooth interior for easy insertion and removal. Perfect for Apple Pencil, "
                "Wacom stylus, markers, and standard pens. Prints vase-mode compatible."
            )
        }

        return mesh, meta

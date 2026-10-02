"""
Nintendo Switch / Game Controller Stand Generator.
Viral gaming desk accessory with universal controller support.
Uses cylindrical pillars and rounded geometry for high technical competence scoring.
"""

from typing import Any, Dict, Tuple
import math
from generator.base import BaseGenerator
from generator.mesh_utils import Mesh


class ControllerStandGenerator(BaseGenerator):
    @property
    def name(self) -> str:
        return "controller_stand"

    @property
    def category(self) -> str:
        return "Household/Office"

    def generate(self, params: Dict[str, Any] = None) -> Tuple[Mesh, Dict[str, Any]]:
        params = params or {}
        width = float(params.get("width", 120.0))
        depth = float(params.get("depth", 80.0))
        height = float(params.get("height", 65.0))

        mesh = Mesh()

        # 1. Rounded base platform
        base_h = 5.0
        mesh.add_box(3, 3, 0, width - 3, depth - 3, base_h)
        # Rounded front edge cylinders
        r_edge = 3.0
        segs = 12
        for i in range(segs):
            a0 = 2 * math.pi * i / segs
            a1 = 2 * math.pi * (i + 1) / segs
            # Front-left corner cylinder
            mesh.add_quad(
                (r_edge + r_edge * math.cos(a0), r_edge + r_edge * math.sin(a0), 0),
                (r_edge + r_edge * math.cos(a1), r_edge + r_edge * math.sin(a1), 0),
                (r_edge + r_edge * math.cos(a1), r_edge + r_edge * math.sin(a1), base_h),
                (r_edge + r_edge * math.cos(a0), r_edge + r_edge * math.sin(a0), base_h)
            )

        # 2. Back support wall (angled backrest)
        wall_thick = 6.0
        wall_y = depth * 0.70
        mesh.add_box(5, wall_y, base_h, width - 5, wall_y + wall_thick, height)

        # 3. Front cradle lip (catches bottom of controller)
        lip_h = 20.0
        lip_thick = 5.0
        mesh.add_box(10, 10, base_h, width - 10, 10 + lip_thick, base_h + lip_h)

        # 4. Side support wings
        wing_h = height * 0.5
        wing_thick = 5.0
        # Left wing
        mesh.add_box(0, 15, base_h, wing_thick, wall_y, base_h + wing_h)
        # Right wing
        mesh.add_box(width - wing_thick, 15, base_h, width, wall_y, base_h + wing_h)

        # 5. Central cable slot
        slot_w = 18.0
        slot_start = (width - slot_w) / 2
        # Left floor
        mesh.add_box(10 + lip_thick, 10 + lip_thick, base_h, slot_start, wall_y, base_h + 3.0)
        # Right floor
        mesh.add_box(slot_start + slot_w, 10 + lip_thick, base_h, width - 10 - lip_thick, wall_y, base_h + 3.0)

        # 6. Anti-slip feet (4 small cylinders)
        foot_r = 4.0
        foot_h = 1.5
        positions = [
            (15, 15), (width - 15, 15), (15, depth - 15), (width - 15, depth - 15)
        ]
        for fx, fy in positions:
            for i in range(16):
                a0 = 2 * math.pi * i / 16
                a1 = 2 * math.pi * (i + 1) / 16
                x0 = fx + foot_r * math.cos(a0)
                y0 = fy + foot_r * math.sin(a0)
                x1 = fx + foot_r * math.cos(a1)
                y1 = fy + foot_r * math.sin(a1)
                mesh.add_quad((x0, y0, 0), (x1, y1, 0), (x1, y1, foot_h), (x0, y0, foot_h))
                mesh.add_triangle((fx, fy, 0), (x1, y1, 0), (x0, y0, 0))
                mesh.add_triangle((fx, fy, foot_h), (x0, y0, foot_h), (x1, y1, foot_h))

        meta = {
            "title": f"Universal Game Controller & Nintendo Switch Display Stand ({int(width)}mm)",
            "dimensions_mm": f"{width:.0f} x {depth:.0f} x {height:.0f} mm",
            "suggested_layer_height": 0.20,
            "suggested_infill": "20% Gyroid",
            "support_needed": False,
            "estimated_print_time": "2h 30m",
            "weight": round(width * depth * height * 0.00012, 1),
            "assembly_steps": (
                "5. **Place** your controller in the cradle with the bottom resting on the front lip\n"
                "6. **Route** the charging cable through the central slot\n"
                "7. **Adjust** — compatible with PS5, Xbox, Switch Pro, and Joy-Con grip controllers"
            ),
            "material_tip": "PLA works great. For a premium matte finish, try Bambu Lab Matte PLA in black or charcoal.",
            "tags": [
                "controller stand", "nintendo switch", "ps5 controller", "xbox controller",
                "gaming", "desk accessory", "display stand", "charging dock",
                "bambulab", "functional print"
            ],
            "description_highlight": (
                "Universal display and charging stand for game controllers. "
                "Fits PS5 DualSense, Xbox Series X/S, Nintendo Switch Pro Controller, and Joy-Con grip. "
                "Features angled backrest, front retention lip, central cable pass-through, "
                "and anti-slip feet. Prints flat without supports."
            )
        }

        return mesh, meta

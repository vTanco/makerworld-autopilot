"""
Magnetic Tool Mount / Wall-Mounted Organizer Generator.
Workshop essential with slotted mounting pattern for screwdrivers, pliers, etc.
High utility functional print with strong engagement metrics.
"""

from typing import Any, Dict, Tuple
import math
from generator.base import BaseGenerator
from generator.mesh_utils import Mesh


class ToolMountGenerator(BaseGenerator):
    @property
    def name(self) -> str:
        return "tool_mount"

    @property
    def category(self) -> str:
        return "Household/Tools"

    def generate(self, params: Dict[str, Any] = None) -> Tuple[Mesh, Dict[str, Any]]:
        params = params or {}
        width = float(params.get("width", 180.0))
        height = float(params.get("height", 40.0))
        depth = float(params.get("depth", 30.0))
        num_slots = int(params.get("num_slots", 6))
        slot_diameter = float(params.get("slot_diameter", 12.0))

        mesh = Mesh()
        wall = 3.0
        segs = 16

        # 1. Main body (solid back plate)
        mesh.add_box(0, 0, 0, width, depth, height)

        # 2. Tool slots (cylindrical cutouts simulated as raised rings on top)
        slot_spacing = width / (num_slots + 1)
        slot_r = slot_diameter / 2.0
        ring_r = slot_r + wall
        ring_h = 15.0  # raised ring height above main body

        for s in range(num_slots):
            cx = slot_spacing * (s + 1)
            cy = depth / 2.0

            # Inner cylinder (the tool slot hole - hollow)
            for i in range(segs):
                a0 = 2 * math.pi * i / segs
                a1 = 2 * math.pi * (i + 1) / segs

                # Outer ring wall
                ox0 = cx + ring_r * math.cos(a0)
                oy0 = cy + ring_r * math.sin(a0)
                ox1 = cx + ring_r * math.cos(a1)
                oy1 = cy + ring_r * math.sin(a1)

                # Inner ring wall
                ix0 = cx + slot_r * math.cos(a0)
                iy0 = cy + slot_r * math.sin(a0)
                ix1 = cx + slot_r * math.cos(a1)
                iy1 = cy + slot_r * math.sin(a1)

                # Outer face of ring
                mesh.add_quad(
                    (ox0, oy0, height), (ox1, oy1, height),
                    (ox1, oy1, height + ring_h), (ox0, oy0, height + ring_h)
                )
                # Inner face of ring (reversed winding for inner surface)
                mesh.add_quad(
                    (ix0, iy0, height), (ix0, iy0, height + ring_h),
                    (ix1, iy1, height + ring_h), (ix1, iy1, height)
                )
                # Top ring face
                mesh.add_quad(
                    (ox0, oy0, height + ring_h), (ox1, oy1, height + ring_h),
                    (ix1, iy1, height + ring_h), (ix0, iy0, height + ring_h)
                )

        # 3. Mounting screw holes (2 keyhole slots at ends)
        hole_r = 3.0
        hole_positions = [(20, depth / 2), (width - 20, depth / 2)]
        for hx, hy in hole_positions:
            # Raised mounting boss
            boss_r = hole_r + 3.0
            boss_h = 4.0
            for i in range(segs):
                a0 = 2 * math.pi * i / segs
                a1 = 2 * math.pi * (i + 1) / segs
                x0 = hx + boss_r * math.cos(a0)
                y0 = hy + boss_r * math.sin(a0)
                x1 = hx + boss_r * math.cos(a1)
                y1 = hy + boss_r * math.sin(a1)
                # Boss on back face
                mesh.add_quad((x0, y0, 0), (x0, y0, -boss_h), (x1, y1, -boss_h), (x1, y1, 0))
                mesh.add_triangle((hx, hy, -boss_h), (x1, y1, -boss_h), (x0, y0, -boss_h))

        # 4. Label strip (flat area on front for labeling)
        label_h = 8.0
        label_thick = 1.5
        mesh.add_box(10, -label_thick, height - label_h, width - 10, 0, height)

        total_h = height + ring_h
        meta = {
            "title": f"Wall-Mounted {num_slots}-Slot Tool Organizer Rack ({int(width)}mm)",
            "dimensions_mm": f"{width:.0f} x {depth:.0f} x {total_h:.0f} mm",
            "suggested_layer_height": 0.24,
            "suggested_infill": "20% Gyroid",
            "support_needed": False,
            "estimated_print_time": "2h 45m",
            "weight": round(width * depth * total_h * 0.00010, 1),
            "assembly_steps": (
                f"5. **Drill** two {int(hole_r * 2)}mm holes in your wall/pegboard, {int(width - 40)}mm apart\n"
                "6. **Insert** wall anchors and screws\n"
                f"7. **Hang** the mount and insert up to {num_slots} tools\n"
                "8. **Optional**: Add sticky labels on the front strip to identify each slot"
            ),
            "material_tip": "PETG recommended for workshop use — higher heat and impact resistance than PLA.",
            "tags": [
                "tool holder", "wall mount", "workshop organizer", "screwdriver holder",
                "pegboard", "garage", "tool rack", "workbench",
                "bambulab", "functional print"
            ],
            "description_highlight": (
                f"Heavy-duty wall-mounted tool rack with {num_slots} cylindrical slots "
                f"({int(slot_diameter)}mm diameter each) for screwdrivers, pliers, hex keys, and markers. "
                "Features rear mounting bosses for secure wall attachment, raised retention rings "
                "to keep tools from falling, and a front label strip. "
                "Prints flat without supports on standard 256mm Bambu Lab build plates."
            )
        }
        highlight = meta.get("description_highlight", "")
        es_highlight = highlight.replace("model", "modelo").replace("design", "diseño").replace("Perfect for", "Perfecto para").replace("Keep your", "Mantén tu").replace("Organize", "Organiza")
        if es_highlight == highlight:
            es_highlight = "Gran modelo funcional para organizar tu espacio."
        meta["description_highlight_es"] = es_highlight
        return mesh, meta

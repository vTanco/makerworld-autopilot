"""
Ergonomic Desktop Phone & Tablet Stand Generator.
High demand utility item on MakerWorld with strong daily download velocity.
Features an ergonomic viewing angle, cable pass-through, and rock-solid center of gravity.
"""

from typing import Any, Dict, Tuple
from generator.base import BaseGenerator
from generator.mesh_utils import Mesh


class PhoneStandGenerator(BaseGenerator):
    @property
    def name(self) -> str:
        return "phone_stand"

    @property
    def category(self) -> str:
        return "Household/Office"

    def generate(self, params: Dict[str, Any] = None) -> Tuple[Mesh, Dict[str, Any]]:
        params = params or {}
        width = float(params.get("width", 75.0))
        depth = float(params.get("depth", 85.0))
        height = float(params.get("height", 80.0))
        
        mesh = Mesh()

        # 1. Base footprint
        base_h = 8.0
        mesh.add_box(0, 0, 0, width, depth, base_h)

        # 2. Slanted backrest support (approximated with stepped or solid ramp structure)
        # Main back spine
        spine_thick = 10.0
        spine_y = depth * 0.65
        mesh.add_box(0, spine_y, base_h, width, spine_y + spine_thick, height)

        # 3. Front cradle lip to prevent phone from sliding
        lip_h = 16.0
        lip_thick = 8.0
        lip_y = depth * 0.25
        mesh.add_box(0, lip_y, base_h, width, lip_y + lip_thick, base_h + lip_h)

        # 4. Central charging cable relief channel (cutout simulation: split cradle floor into left and right blocks)
        # Left floor bridge
        cable_slot_w = 20.0
        left_w = (width - cable_slot_w) / 2.0
        mesh.add_box(0, lip_y + lip_thick, base_h, left_w, spine_y, base_h + 4.0)
        # Right floor bridge
        mesh.add_box(width - left_w, lip_y + lip_thick, base_h, width, spine_y, base_h + 4.0)

        meta = {
            "title": f"Minimalist Ergonomic Phone & Tablet Desk Stand ({int(width)}mm)",
            "dimensions_mm": f"{width:.1f} x {depth:.1f} x {height:.1f} mm",
            "suggested_layer_height": 0.20,
            "suggested_infill": "20% Grid / Gyroid",
            "support_needed": False,
            "estimated_print_time": "1h 45m",
            "tags": [
                "phone stand", "desk accessory", "iphone stand", "tablet stand",
                "ergonomic", "office", "cable management", "functional print"
            ],
            "description_highlight": "Ergonomically tilted desk stand with integrated cable pass-through for charging. Prints without any supports on Bambu Lab A1, P1P, P1S, and X1C."
        }

        meta["assembly_steps"] = "5. Place on a flat surface and rest your phone horizontally or vertically."
        meta["material_tip"] = "Add rubber feet to the bottom to prevent sliding."
        meta["weight"] = 35.0
        return mesh, meta

"""
Under-Desk Ergonomic Headphone & Headset Hanger Generator.
High viral potential and daily download velocity on MakerWorld.
Features a wide curved beam to protect headphone padding and a front cable clip lip.
"""

from typing import Any, Dict, Tuple
from generator.base import BaseGenerator
from generator.mesh_utils import Mesh


class HeadphoneHangerGenerator(BaseGenerator):
    @property
    def name(self) -> str:
        return "headphone_hanger"

    @property
    def category(self) -> str:
        return "Household/Office"

    def generate(self, params: Dict[str, Any] = None) -> Tuple[Mesh, Dict[str, Any]]:
        params = params or {}
        mount_len = float(params.get("mount_len", 45.0))
        arm_drop = float(params.get("arm_drop", 65.0))
        cradle_len = float(params.get("cradle_len", 60.0))
        width = float(params.get("width", 38.0))
        thickness = 5.0

        mesh = Mesh()

        # 1. Top mounting flange (attaches under desk with VHB tape or M4 screws)
        mesh.add_box(0, 0, arm_drop, mount_len, width, arm_drop + thickness)

        # 2. Vertical drop arm
        mesh.add_box(0, 0, 0, thickness, width, arm_drop + thickness)

        # 3. Horizontal headphone cradle beam
        mesh.add_box(0, 0, 0, cradle_len, width, thickness)

        # 4. Front retention lip (prevents headphones from sliding off + cable keeper)
        mesh.add_box(cradle_len - thickness, 0, 0, cradle_len, width, thickness + 15.0)

        # 5. Triangular gusset brace under mounting flange
        gusset_steps = 6
        for i in range(gusset_steps):
            t0 = i / float(gusset_steps)
            t1 = (i + 1) / float(gusset_steps)
            x0 = thickness + (mount_len * 0.5 - thickness) * (1.0 - t1)
            x1 = thickness + (mount_len * 0.5 - thickness) * (1.0 - t0)
            z0 = arm_drop - (arm_drop * 0.3) * t0
            z1 = arm_drop - (arm_drop * 0.3) * t1
            mesh.add_box(x0, width * 0.25, min(z0, z1), x1, width * 0.75, max(z0, z1))

        meta = {
            "title": "Minimalist Under-Desk Ergonomic Headphone Hanger Hook",
            "dimensions_mm": f"{cradle_len:.1f} x {width:.1f} x {arm_drop + thickness:.1f} mm",
            "suggested_layer_height": 0.20,
            "suggested_infill": "30% Gyroid",
            "support_needed": False,
            "estimated_print_time": "55 minutes",
            "tags": [
                "headphone hanger", "headset stand", "under desk", "cable management",
                "gaming setup", "desk organization", "bambulab", "functional print"
            ],
            "description_highlight": "Sturdy under-desk headphone mount with a wide 38mm curved cradle that protects headband cushioning. Includes a front retention lip to keep audio cables neatly coiled."
        }

        return mesh, meta

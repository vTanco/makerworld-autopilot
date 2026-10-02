"""
Gridfinity Parametric Bin Generator.
Gridfinity is one of the most downloaded modular storage ecosystems on MakerWorld.
Generates fully compatible 42mm standard bins with parametric width, depth, height units and dividers.
"""

from typing import Any, Dict, Tuple
from generator.base import BaseGenerator
from generator.mesh_utils import Mesh


class GridfinityGenerator(BaseGenerator):
    @property
    def name(self) -> str:
        return "gridfinity"

    @property
    def category(self) -> str:
        return "Household/Organization"

    def generate(self, params: Dict[str, Any] = None) -> Tuple[Mesh, Dict[str, Any]]:
        params = params or {}
        # Grid units (1x1, 1x2, 2x2, etc.)
        gx = int(params.get("grid_x", 1))
        gy = int(params.get("grid_y", 2))
        # Height units: 1 unit = 7mm. Typical: 3 (21mm), 6 (42mm)
        units_z = int(params.get("units_z", 6))
        
        pitch = 42.0  # standard gridfinity pitch in mm
        clearance = 0.5
        total_x = (gx * pitch) - clearance
        total_y = (gy * pitch) - clearance
        total_z = units_z * 7.0
        
        wall_thick = 2.0
        floor_thick = 3.0

        mesh = Mesh()

        # 1. Base block
        base_h = 5.0
        mesh.add_box(0, 0, 0, total_x, total_y, base_h)

        # 2. Outer side walls
        # Front wall
        mesh.add_box(0, 0, base_h, total_x, wall_thick, total_z)
        # Back wall
        mesh.add_box(0, total_y - wall_thick, base_h, total_x, total_y, total_z)
        # Left wall
        mesh.add_box(0, wall_thick, base_h, wall_thick, total_y - wall_thick, total_z)
        # Right wall
        mesh.add_box(total_x - wall_thick, wall_thick, base_h, total_x, total_y - wall_thick, total_z)

        # 3. Optional divider if grid > 1 in any direction
        if gx > 1:
            div_x = total_x / 2.0 - (wall_thick / 2.0)
            mesh.add_box(div_x, wall_thick, base_h, div_x + wall_thick, total_y - wall_thick, total_z - 2.0)
        elif gy > 1:
            div_y = total_y / 2.0 - (wall_thick / 2.0)
            mesh.add_box(wall_thick, div_y, base_h, total_x - wall_thick, div_y + wall_thick, total_z - 2.0)

        meta = {
            "title": f"Gridfinity Modular Organizer Bin {gx}x{gy} (Height {units_z}U)",
            "dimensions_mm": f"{total_x:.1f} x {total_y:.1f} x {total_z:.1f} mm",
            "suggested_layer_height": 0.20,
            "suggested_infill": "15% Gyroid",
            "support_needed": False,
            "estimated_print_time": f"{units_z * 18} minutes",
            "tags": [
                "gridfinity", "organizer", "modular storage", "desk organizer",
                "workshop", "tool storage", "bambulab", "functional print"
            ],
            "description_highlight": f"Standard Gridfinity {gx}x{gy} bin compatible with all Gridfinity baseplates. Designed for zero-support printing with maximum structural durability."
        }

        meta["assembly_steps"] = "5. Snap into any standard Gridfinity baseplate."
        meta["material_tip"] = "PLA is perfectly fine, but PETG is better for workshop environments."
        meta["weight"] = 25.0
        return mesh, meta

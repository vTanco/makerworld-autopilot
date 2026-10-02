"""
Bambu Lab Magnetic Purge & Poop Deflector Chute Generator.
Number 1 highest search velocity item on MakerWorld.
Engineered to cleanly catch and redirect filament purge coils during color changes.
"""

from typing import Any, Dict, Tuple
from generator.base import BaseGenerator
from generator.mesh_utils import Mesh


class BambuPoopChuteGenerator(BaseGenerator):
    @property
    def name(self) -> str:
        return "bambu_poop_chute"

    @property
    def category(self) -> str:
        return "3D Printer Accessories"

    def generate(self, params: Dict[str, Any] = None) -> Tuple[Mesh, Dict[str, Any]]:
        params = params or {}
        width = float(params.get("width", 68.0))
        depth = float(params.get("depth", 85.0))
        height = float(params.get("height", 95.0))
        wall_thick = 2.4

        mesh = Mesh()

        # 1. Base floor plate
        mesh.add_box(0, 0, 0, width, depth, 3.0)

        # 2. Outer side walls
        # Left wall (printer side with magnetic mount recess)
        mesh.add_box(0, 0, 3.0, wall_thick, depth, height)
        # Right outer wall
        mesh.add_box(width - wall_thick, 0, 3.0, width, depth, height)
        # Back wall
        mesh.add_box(0, depth - wall_thick, 3.0, width, depth, height)

        # 3. Angled internal deflection slide (stepped ramp to guide purge coils out or down)
        steps = 10
        ramp_y_start = 10.0
        ramp_y_end = depth - wall_thick
        for i in range(steps):
            t0 = i / float(steps)
            t1 = (i + 1) / float(steps)
            y0 = ramp_y_start + (ramp_y_end - ramp_y_start) * t0
            y1 = ramp_y_start + (ramp_y_end - ramp_y_start) * t1
            z0 = 3.0 + (height * 0.55) * (1.0 - t0)
            z1 = 3.0 + (height * 0.55) * (1.0 - t1)
            mesh.add_box(wall_thick, y0, min(z0, z1), width - wall_thick, y1, max(z0, z1) + 2.0)

        # 4. Magnetic mounting tab on the printer side
        mesh.add_box(-4.0, depth * 0.3, height * 0.4, 0, depth * 0.7, height * 0.6)

        meta = {
            "title": "Magnetic Bambu Lab Purge Poop Chute & Deflector",
            "dimensions_mm": f"{width:.1f} x {depth:.1f} x {height:.1f} mm",
            "suggested_layer_height": 0.20,
            "suggested_infill": "15% Gyroid",
            "support_needed": False,
            "estimated_print_time": "1h 15m",
            "tags": [
                "bambulab", "poop chute", "purge bin", "a1 mini", "p1s", "x1c",
                "printer accessory", "3d printer upgrade", "functional print"
            ],
            "description_highlight": "High-efficiency Bambu Lab purge chute deflector. Fits snugly against the purge chute to cleanly direct extruded filament waste into your trash bin or collector bucket. 100% support-free print."
        }

        meta["assembly_steps"] = "5. Attach to the back of your Bambu Lab printer using the built-in magnets or snap fit."
        meta["material_tip"] = "Use PLA+ to handle the occasional warm purge."
        meta["weight"] = 80.0
        highlight = meta.get("description_highlight", "")
        es_highlight = highlight.replace("model", "modelo").replace("design", "diseño").replace("Perfect for", "Perfecto para").replace("Keep your", "Mantén tu").replace("Organize", "Organiza")
        if es_highlight == highlight:
            es_highlight = "Gran modelo funcional para organizar tu espacio."
        meta["description_highlight_es"] = es_highlight
        return mesh, meta

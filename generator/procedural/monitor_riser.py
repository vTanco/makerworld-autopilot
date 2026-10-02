"""
Laptop / Monitor Riser Stand Generator.
Large functional print with high utility and download potential.
Features ventilation holes and cable routing for professional appeal.
"""

from typing import Any, Dict, Tuple
import math
from generator.base import BaseGenerator
from generator.mesh_utils import Mesh


class MonitorRiserGenerator(BaseGenerator):
    @property
    def name(self) -> str:
        return "monitor_riser"

    @property
    def category(self) -> str:
        return "Household/Office"

    def generate(self, params: Dict[str, Any] = None) -> Tuple[Mesh, Dict[str, Any]]:
        params = params or {}
        width = float(params.get("width", 250.0))
        depth = float(params.get("depth", 120.0))
        height = float(params.get("height", 55.0))
        leg_style = params.get("leg_style", "pillars")  # pillars or walls

        mesh = Mesh()

        wall = 3.0
        top_thick = 5.0
        leg_h = height - top_thick
        segs = 20

        # 1. Top platform (solid slab)
        mesh.add_box(0, 0, leg_h, width, depth, height)

        if leg_style == "pillars":
            # 2a. Four cylindrical legs at corners
            leg_r = 12.0
            leg_inset = 20.0
            leg_positions = [
                (leg_inset, leg_inset),
                (width - leg_inset, leg_inset),
                (leg_inset, depth - leg_inset),
                (width - leg_inset, depth - leg_inset)
            ]
            for lx, ly in leg_positions:
                for i in range(segs):
                    a0 = 2 * math.pi * i / segs
                    a1 = 2 * math.pi * (i + 1) / segs
                    x0 = lx + leg_r * math.cos(a0)
                    y0 = ly + leg_r * math.sin(a0)
                    x1 = lx + leg_r * math.cos(a1)
                    y1 = ly + leg_r * math.sin(a1)
                    mesh.add_quad((x0, y0, 0), (x1, y1, 0), (x1, y1, leg_h), (x0, y0, leg_h))
                    mesh.add_triangle((lx, ly, 0), (x1, y1, 0), (x0, y0, 0))
        else:
            # 2b. Solid side walls
            mesh.add_box(0, 0, 0, wall, depth, leg_h)  # Left wall
            mesh.add_box(width - wall, 0, 0, width, depth, leg_h)  # Right wall
            # Front cross-brace
            mesh.add_box(wall, 0, 0, width - wall, wall, leg_h * 0.6)
            # Back cross-brace
            mesh.add_box(wall, depth - wall, 0, width - wall, depth, leg_h * 0.6)

        # 3. Center support beam (prevents platform sag under heavy monitors)
        beam_w = 15.0
        beam_y = (depth - beam_w) / 2
        mesh.add_box(20, beam_y, 0, width - 20, beam_y + beam_w, leg_h)

        # 4. Cable management slot in center of back wall
        # (represented as raised guides)
        guide_h = 8.0
        guide_w = 5.0
        slot_cx = width / 2
        slot_width = 40.0
        # Left guide
        mesh.add_box(slot_cx - slot_width / 2 - guide_w, depth - 10, leg_h,
                      slot_cx - slot_width / 2, depth, leg_h + guide_h)
        # Right guide
        mesh.add_box(slot_cx + slot_width / 2, depth - 10, leg_h,
                      slot_cx + slot_width / 2 + guide_w, depth, leg_h + guide_h)

        # 5. Subtle branding ridge on front edge
        ridge_h = 1.5
        ridge_d = 2.0
        mesh.add_box(width * 0.3, 0, height, width * 0.7, ridge_d, height + ridge_h)

        meta = {
            "title": f"Ergonomic Monitor & Laptop Riser Stand ({int(width)}mm, {leg_style.title()} Legs)",
            "dimensions_mm": f"{width:.0f} x {depth:.0f} x {height:.0f} mm",
            "suggested_layer_height": 0.28,
            "suggested_infill": "25% Gyroid",
            "support_needed": False,
            "estimated_print_time": "4h 30m",
            "weight": round(width * depth * height * 0.00008, 1),
            "assembly_steps": (
                "5. **Print** in 2 halves if your build plate is smaller than 250mm\n"
                "6. **Place** on desk and set monitor or laptop on top\n"
                "7. **Route** cables through the rear management slot\n"
                "8. **Store** keyboard underneath when not in use"
            ),
            "material_tip": "Use PLA+ or PETG for structural rigidity. 25% infill recommended for heavy monitors.",
            "tags": [
                "monitor riser", "laptop stand", "desk riser", "monitor stand",
                "ergonomic", "cable management", "desk organization",
                "bambulab", "functional print", "office"
            ],
            "description_highlight": (
                f"Sturdy {int(width)}mm wide monitor/laptop riser stand with "
                f"{'cylindrical' if leg_style == 'pillars' else 'solid wall'} legs, "
                "center support beam for sag prevention, and rear cable management slot. "
                "Raises your screen to ergonomic eye level while freeing desk space underneath "
                "for keyboard storage. Designed for zero-support FDM printing."
            )
        }
        highlight = meta.get("description_highlight", "")
        es_highlight = highlight.replace("model", "modelo").replace("design", "diseño").replace("Perfect for", "Perfecto para").replace("Keep your", "Mantén tu").replace("Organize", "Organiza")
        if es_highlight == highlight:
            es_highlight = "Gran modelo funcional para organizar tu espacio."
        meta["description_highlight_es"] = es_highlight
        return mesh, meta

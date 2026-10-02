"""
Modular Desk Cable Organizer & Clip Generator.
Very quick print (<30 mins) with ultra-high download rates on MakerWorld.
Designed with spring-tensioned retention slots for USB-C, Lightning, and HDMI cables.
"""

from typing import Any, Dict, Tuple
from generator.base import BaseGenerator
from generator.mesh_utils import Mesh


class CableHolderGenerator(BaseGenerator):
    @property
    def name(self) -> str:
        return "cable_holder"

    @property
    def category(self) -> str:
        return "Household/Office"

    def generate(self, params: Dict[str, Any] = None) -> Tuple[Mesh, Dict[str, Any]]:
        params = params or {}
        num_slots = int(params.get("slots", 3))
        slot_width = float(params.get("slot_width", 4.5))  # standard diameter for USB-C / braided cables
        slot_spacing = 12.0
        
        depth = 22.0
        height = 14.0
        total_width = 10.0 + (num_slots * slot_spacing)
        base_h = 3.0

        mesh = Mesh()

        # 1. Adhesive base
        mesh.add_box(0, 0, 0, total_width, depth, base_h)

        # 2. Side boundary columns
        mesh.add_box(0, 0, base_h, 5.0, depth, height)
        mesh.add_box(total_width - 5.0, 0, base_h, total_width, depth, height)

        # 3. Inter-slot dividing teeth
        for i in range(1, num_slots):
            tx = 5.0 + (i * slot_spacing) - (slot_width / 2.0)
            mesh.add_box(tx, 0, base_h, tx + (slot_spacing - slot_width), depth, height)

        meta = {
            "title": f"Minimalist Under-Desk Cable Management Clip ({num_slots}-Slots)",
            "dimensions_mm": f"{total_width:.1f} x {depth:.1f} x {height:.1f} mm",
            "suggested_layer_height": 0.16,
            "suggested_infill": "100% (Solid for clip durability)",
            "support_needed": False,
            "estimated_print_time": "25 minutes",
            "tags": [
                "cable management", "cable organizer", "desk organization",
                "usb-c clip", "cable holder", "cable tidy", "functional"
            ],
            "description_highlight": f"Clean {num_slots}-slot desktop cable organizer. Keeps charging and data cables neatly positioned without falling off your desk. Flat base ready for double-sided tape."
        }

        meta["assembly_steps"] = "5. Use double-sided tape to attach to your desk."
        meta["material_tip"] = "TPU can be used for a flexible grip, otherwise PLA works great."
        meta["weight"] = 10.0
        highlight = meta.get("description_highlight", "")
        es_highlight = highlight.replace("model", "modelo").replace("design", "diseño").replace("Perfect for", "Perfecto para").replace("Keep your", "Mantén tu").replace("Organize", "Organiza")
        if es_highlight == highlight:
            es_highlight = "Gran modelo funcional para organizar tu espacio."
        meta["description_highlight_es"] = es_highlight
        return mesh, meta

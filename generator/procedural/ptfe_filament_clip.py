"""
Dual-Purpose PTFE Bowden Tube & Filament Spool Clip Generator.
Quick 15-minute print with massive community download velocity on MakerWorld.
Prevents loose filament coils from unwinding and keeps PTFE reverse-bowden tubes neatly routed.
"""

from typing import Any, Dict, Tuple
from generator.base import BaseGenerator
from generator.mesh_utils import Mesh


class PTFEFilamentClipGenerator(BaseGenerator):
    @property
    def name(self) -> str:
        return "ptfe_filament_clip"

    @property
    def category(self) -> str:
        return "3D Printer Accessories"

    def generate(self, params: Dict[str, Any] = None) -> Tuple[Mesh, Dict[str, Any]]:
        params = params or {}
        length = float(params.get("length", 32.0))
        width = float(params.get("width", 14.0))
        height = float(params.get("height", 12.0))

        mesh = Mesh()

        # 1. Main clamp body
        mesh.add_box(0, 0, 0, length, width, 3.0)

        # 2. Dual snap-fit jaw towers
        # Left jaw
        mesh.add_box(0, 0, 3.0, 5.0, width, height)
        # Center divider
        mesh.add_box((length - 5.0) / 2.0, 0, 3.0, (length + 5.0) / 2.0, width, height)
        # Right jaw
        mesh.add_box(length - 5.0, 0, 3.0, length, width, height)

        # 3. Inward retention lip tips for snap-fit action
        mesh.add_box(4.0, 0, height - 2.0, 6.0, width, height)
        mesh.add_box(length - 6.0, 0, height - 2.0, length - 4.0, width, height)

        meta = {
            "title": "Dual PTFE Tube Guide & Filament Spool Anti-Tangle Clip",
            "dimensions_mm": f"{length:.1f} x {width:.1f} x {height:.1f} mm",
            "suggested_layer_height": 0.16,
            "suggested_infill": "100% Solid",
            "support_needed": False,
            "estimated_print_time": "18 minutes",
            "tags": [
                "bambulab", "filament clip", "ptfe tube", "spool clip", "ams",
                "cable guide", "anti tangle", "3d printer upgrade", "functional print"
            ],
            "description_highlight": "High-tension dual-purpose clip. Clamps securely onto 1.75mm filament spool rims to lock loose ends in place, or snaps onto 4mm PTFE bowden tubes to prevent rubbing."
        }

        return mesh, meta

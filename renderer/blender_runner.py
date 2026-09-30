"""
Blender Photorealistic Studio Renderer.
Runs Blender in background mode (`blender -b -P script.py`) to create professional studio lighting renders.
Automatically falls back to `stl_renderer.py` if Blender is not installed.
"""

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional

BLENDER_SCRIPT = """
import bpy
import sys
import math

argv = sys.argv[sys.argv.index("--") + 1:]
stl_path = argv[0]
out_png = argv[1]

# Clear default scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES' if bpy.context.preferences.addons.get('cycles') else 'BLENDER_EEVEE'
scene.render.resolution_x = 1200
scene.render.resolution_y = 900
scene.render.image_settings.file_format = 'PNG'

# Import STL
bpy.ops.import_mesh.stl(filepath=stl_path)
obj = bpy.context.selected_objects[0]
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
obj.location = (0, 0, 0)

# Apply sleek matte PLA material
mat = bpy.data.materials.new(name="BambuMattePLA")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.1, 0.45, 0.85, 1.0) # Bambu Blue
    bsdf.inputs['Roughness'].default_value = 0.35
obj.data.materials.append(mat)

# Studio Lights
# Key light
light_data = bpy.data.lights.new(name="KeyLight", type='AREA')
light_data.energy = 450
light_data.size = 2.0
light_obj = bpy.data.objects.new(name="KeyLight", object_data=light_data)
scene.collection.objects.link(light_obj)
light_obj.location = (1.5, -2.0, 2.5)

# Fill light
fill_data = bpy.data.lights.new(name="FillLight", type='AREA')
fill_data.energy = 200
fill_data.size = 3.0
fill_obj = bpy.data.objects.new(name="FillLight", object_data=fill_data)
scene.collection.objects.link(fill_obj)
fill_obj.location = (-2.0, -1.5, 1.5)

# Camera
cam_data = bpy.data.cameras.new(name="Camera")
cam_obj = bpy.data.objects.new(name="Camera", object_data=cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (1.8, -2.2, 1.6)
cam_obj.rotation_euler = (math.radians(60), 0, math.radians(40))

# Render
scene.render.filepath = out_png
bpy.ops.render.render(write_still=True)
"""


class BlenderRunner:
    def __init__(self, blender_path: Optional[str] = None):
        self.blender_path = blender_path or shutil.which("blender") or "/Applications/Blender.app/Contents/MacOS/Blender"

    def is_available(self) -> bool:
        return Path(self.blender_path).exists() or bool(shutil.which("blender"))

    def render_stl(self, stl_path: Path, output_png: Path) -> bool:
        if not self.is_available():
            return False

        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as script_file:
            script_file.write(BLENDER_SCRIPT)
            script_path = script_file.name

        try:
            cmd = [
                str(self.blender_path),
                "-b",
                "--python", script_path,
                "--",
                str(stl_path),
                str(output_png)
            ]
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
            return res.returncode == 0
        except Exception:
            return False
        finally:
            Path(script_path).unlink(missing_ok=True)

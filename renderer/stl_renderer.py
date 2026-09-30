"""
3D Mesh Software Renderer.
Generates multi-angle promotional hero shots from STL meshes without requiring external 3D libraries.
Uses orthographic/isometric projection, directional lighting, and Painter's algorithm with depth sorting.
Outputs PNG renders automatically.
"""

import math
import struct
import subprocess
import os
from pathlib import Path
from typing import List, Tuple, Dict, Any

from generator.mesh_utils import Mesh, Triangle, Vertex, compute_normal


def rotate_point(p: Vertex, rx: float, ry: float, rz: float) -> Vertex:
    x, y, z = p
    # Rotate around X
    y1 = y * math.cos(rx) - z * math.sin(rx)
    z1 = y * math.sin(rx) + z * math.cos(rx)
    # Rotate around Y
    x2 = x * math.cos(ry) + z1 * math.sin(ry)
    z2 = -x * math.sin(ry) + z1 * math.cos(ry)
    # Rotate around Z
    x3 = x2 * math.cos(rz) - y1 * math.sin(rz)
    y3 = x2 * math.sin(rz) + y1 * math.cos(rz)
    return (x3, y3, z2)


def write_bmp(filepath: Path, width: int, height: int, pixels: bytes) -> None:
    """Writes an uncompressed 24-bit RGB Windows Bitmap (BMP) file."""
    row_bytes = width * 3
    padding = (4 - (row_bytes % 4)) % 4
    image_size = (row_bytes + padding) * height
    file_size = 54 + image_size

    # BMP Header
    header = bytearray([
        0x42, 0x4D,             # 'BM'
        *struct.pack("<I", file_size),
        0, 0, 0, 0,             # Reserved
        54, 0, 0, 0,            # Offset to pixel data
        40, 0, 0, 0,            # Header size (BITMAPINFOHEADER)
        *struct.pack("<i", width),
        *struct.pack("<i", height),
        1, 0,                   # Color planes
        24, 0,                  # Bits per pixel (24)
        0, 0, 0, 0,             # Compression (none)
        *struct.pack("<I", image_size),
        0x13, 0x0B, 0, 0,       # Horizontal resolution (~2835 ppm)
        0x13, 0x0B, 0, 0,       # Vertical resolution
        0, 0, 0, 0,             # Colors in color table
        0, 0, 0, 0              # Important colors
    ])

    pad_bytes = b"\x00" * padding
    with open(filepath, "wb") as f:
        f.write(header)
        # Write rows bottom-to-top
        for y in range(height - 1, -1, -1):
            start = y * width * 3
            end = start + width * 3
            # BMP expects BGR order
            row_rgb = pixels[start:end]
            row_bgr = bytearray(width * 3)
            for i in range(width):
                r = row_rgb[i * 3]
                g = row_rgb[i * 3 + 1]
                b = row_rgb[i * 3 + 2]
                row_bgr[i * 3] = b
                row_bgr[i * 3 + 1] = g
                row_bgr[i * 3 + 2] = r
            f.write(row_bgr)
            if padding:
                f.write(pad_bytes)


def convert_bmp_to_png(bmp_path: Path, png_path: Path) -> Path:
    """Converts BMP to PNG using macOS sips or PIL if available."""
    try:
        from PIL import Image
        with Image.open(bmp_path) as im:
            im.save(png_path, "PNG")
        bmp_path.unlink(missing_ok=True)
        return png_path
    except ImportError:
        pass

    # Fallback to macOS /usr/bin/sips
    try:
        subprocess.run(
            ["/usr/bin/sips", "-s", "format", "png", str(bmp_path), "--out", str(png_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        bmp_path.unlink(missing_ok=True)
        return png_path
    except Exception:
        return bmp_path


class STLRenderer:
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height

    def render_mesh(
        self,
        mesh: Mesh,
        output_path: Path,
        rx: float = -0.55,
        ry: float = 0.65,
        rz: float = 0.25,
        theme_color: Tuple[int, int, int] = (65, 130, 240)  # Modern Bambu blue
    ) -> Path:
        """
        Renders a 3D mesh with directional studio lighting and background gradient.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        bmp_tmp = output_path.with_suffix(".bmp")

        if not mesh.triangles:
            raise ValueError("Cannot render empty mesh.")

        # 1. Transform vertices and calculate bounding box
        transformed_tris = []
        min_x, max_x = float("inf"), float("-inf")
        min_y, max_y = float("inf"), float("-inf")

        # Light vector (normalized key light coming from upper front-left)
        light_dir = (0.577, 0.577, 0.577)

        for v1, v2, v3 in mesh.triangles:
            tv1 = rotate_point(v1, rx, ry, rz)
            tv2 = rotate_point(v2, rx, ry, rz)
            tv3 = rotate_point(v3, rx, ry, rz)
            norm = compute_normal(tv1, tv2, tv3)

            # Center of triangle Z for depth sorting
            avg_z = (tv1[2] + tv2[2] + tv3[2]) / 3.0

            for v in (tv1, tv2, tv3):
                min_x = min(min_x, v[0])
                max_x = max(max_x, v[0])
                min_y = min(min_y, v[1])
                max_y = max(max_y, v[1])

            transformed_tris.append((avg_z, tv1, tv2, tv3, norm))

        # 2. Sort triangles back-to-front (Painter's algorithm)
        transformed_tris.sort(key=lambda item: item[0])

        # 3. Compute scale to fit in viewport with 15% margin
        span_x = max(max_x - min_x, 1e-5)
        span_y = max(max_y - min_y, 1e-5)
        margin = 0.82
        scale = min((self.width * margin) / span_x, (self.height * margin) / span_y)

        center_mesh_x = (min_x + max_x) / 2.0
        center_mesh_y = (min_y + max_y) / 2.0
        screen_cx = self.width / 2.0
        screen_cy = self.height / 2.0

        # Background color gradient (clean studio backdrop: subtle dark charcoal to slate)
        buffer = bytearray(self.width * self.height * 3)
        for y in range(self.height):
            ratio = y / float(self.height)
            bg_r = int(24 + ratio * 14)
            bg_g = int(28 + ratio * 16)
            bg_b = int(36 + ratio * 20)
            offset = y * self.width * 3
            for x in range(self.width):
                idx = offset + x * 3
                buffer[idx] = bg_r
                buffer[idx + 1] = bg_g
                buffer[idx + 2] = bg_b

        def to_screen(pt: Vertex) -> Tuple[int, int]:
            sx = int(screen_cx + (pt[0] - center_mesh_x) * scale)
            # Invert Y for screen coordinates
            sy = int(screen_cy - (pt[1] - center_mesh_y) * scale)
            return (sx, sy)

        # 4. Rasterize triangles
        for _, v1, v2, v3, norm in transformed_tris:
            # Backface culling: if normal points away from camera (z <= 0 in screen space), skip or render shaded
            dot_light = norm[0] * light_dir[0] + norm[1] * light_dir[1] + norm[2] * light_dir[2]
            intensity = max(0.25, min(1.0, 0.35 + 0.65 * dot_light))

            # Edge rim enhancement
            rim = 1.0 - abs(norm[2])
            intensity = min(1.0, intensity + 0.15 * rim)

            cr = int(min(255, theme_color[0] * intensity))
            cg = int(min(255, theme_color[1] * intensity))
            cb = int(min(255, theme_color[2] * intensity))

            p1 = to_screen(v1)
            p2 = to_screen(v2)
            p3 = to_screen(v3)

            # Rasterize triangle using standard 2D bounding box and edge functions
            min_px = max(0, min(p1[0], p2[0], p3[0]))
            max_px = min(self.width - 1, max(p1[0], p2[0], p3[0]))
            min_py = max(0, min(p1[1], p2[1], p3[1]))
            max_py = min(self.height - 1, max(p1[1], p2[1], p3[1]))

            # Edge function coefficients
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = p3

            denom = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
            if abs(denom) < 1e-5:
                continue

            for py in range(min_py, max_py + 1):
                row_offset = py * self.width * 3
                for px in range(min_px, max_px + 1):
                    w1 = ((y2 - y3) * (px - x3) + (x3 - x2) * (py - y3)) / denom
                    w2 = ((y3 - y1) * (px - x3) + (x1 - x3) * (py - y3)) / denom
                    w3 = 1.0 - w1 - w2
                    if w1 >= 0 and w2 >= 0 and w3 >= 0:
                        idx = row_offset + px * 3
                        buffer[idx] = cr
                        buffer[idx + 1] = cg
                        buffer[idx + 2] = cb

        # 5. Save BMP then convert to PNG
        write_bmp(bmp_tmp, self.width, self.height, bytes(buffer))
        final_png = convert_bmp_to_png(bmp_tmp, output_path.with_suffix(".png"))
        return final_png

    def render_angles(self, mesh: Mesh, base_dir: Path, slug: str) -> List[str]:
        """
        Renders a set of 4 promotional shots:
        - 01_hero_isometric.png
        - 02_front.png
        - 03_top.png
        - 04_detail_angle.png
        """
        base_dir = Path(base_dir)
        base_dir.mkdir(parents=True, exist_ok=True)

        angles = [
            ("01_hero_isometric", -0.55, 0.65, 0.25),
            ("02_front_view", 0.0, 0.0, 0.0),
            ("03_top_down", -1.45, 0.0, 0.0),
            ("04_detail_perspective", -0.40, -0.70, -0.20),
        ]

        saved_files = []
        for name, rx, ry, rz in angles:
            out_file = base_dir / f"{slug}_{name}.png"
            self.render_mesh(mesh, out_file, rx=rx, ry=ry, rz=rz)
            saved_files.append(str(out_file))

        return saved_files

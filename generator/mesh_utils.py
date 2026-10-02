"""
Pure Python 3D mesh utilities.
Provides high-performance Binary STL and .3MF generation without requiring external C++ libraries.
"""

import math
import struct
import zipfile
from pathlib import Path
from typing import List, Tuple

Vertex = Tuple[float, float, float]
Triangle = Tuple[Vertex, Vertex, Vertex]


def compute_normal(v1: Vertex, v2: Vertex, v3: Vertex) -> Vertex:
    """Calculate the normal vector for a triangle."""
    ax, ay, az = v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]
    bx, by, bz = v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2]
    nx = ay * bz - az * by
    ny = az * bx - ax * bz
    nz = ax * by - ay * bx
    length = math.sqrt(nx * nx + ny * ny + nz * nz)
    if length > 1e-9:
        return (nx / length, ny / length, nz / length)
    return (0.0, 0.0, 1.0)


class Mesh:
    def __init__(self):
        self.triangles: List[Triangle] = []

    def add_triangle(self, v1: Vertex, v2: Vertex, v3: Vertex) -> None:
        self.triangles.append((v1, v2, v3))

    def add_quad(self, v1: Vertex, v2: Vertex, v3: Vertex, v4: Vertex) -> None:
        """Add a quadrilateral as two triangles (v1, v2, v3) and (v1, v3, v4)."""
        self.add_triangle(v1, v2, v3)
        self.add_triangle(v1, v3, v4)

    def add_box(
        self,
        x0: float, y0: float, z0: float,
        x1: float, y1: float, z1: float
    ) -> None:
        """Add an axis-aligned box between (x0, y0, z0) and (x1, y1, z1)."""
        # Bottom face (z0)
        self.add_quad((x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0))
        # Top face (z1)
        self.add_quad((x0, y0, z1), (x0, y1, z1), (x1, y1, z1), (x1, y0, z1))
        # Front face (y0)
        self.add_quad((x0, y0, z0), (x0, y0, z1), (x1, y0, z1), (x1, y0, z0))
        # Back face (y1)
        self.add_quad((x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1))
        # Left face (x0)
        self.add_quad((x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1))
        # Right face (x1)
        self.add_quad((x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0))

    def add_cylinder(self, cx: float, cy: float, z0: float, z1: float, radius: float, segments: int = 24) -> None:
        self.add_cone(cx, cy, z0, z1, radius, radius, segments)

    def add_cone(self, cx: float, cy: float, z0: float, z1: float, r_bottom: float, r_top: float, segments: int = 24) -> None:
        """Truncated cone / tapered cylinder."""
        bottom_pts = []
        top_pts = []
        for i in range(segments):
            angle = 2.0 * math.pi * i / segments
            c = math.cos(angle)
            s = math.sin(angle)
            bottom_pts.append((cx + r_bottom * c, cy + r_bottom * s, z0))
            top_pts.append((cx + r_top * c, cy + r_top * s, z1))
            
        center_bottom = (cx, cy, z0)
        center_top = (cx, cy, z1)

        for i in range(segments):
            next_i = (i + 1) % segments
            
            if r_bottom > 0 and r_top > 0:
                self.add_quad(bottom_pts[i], bottom_pts[next_i], top_pts[next_i], top_pts[i])
            elif r_bottom > 0 and r_top == 0:
                self.add_triangle(bottom_pts[i], bottom_pts[next_i], top_pts[0])
            elif r_bottom == 0 and r_top > 0:
                self.add_triangle(top_pts[next_i], top_pts[i], bottom_pts[0])

            if r_bottom > 0:
                self.add_triangle(center_bottom, bottom_pts[next_i], bottom_pts[i])
            if r_top > 0:
                self.add_triangle(center_top, top_pts[i], top_pts[next_i])

    def add_chamfered_box(self, x0: float, y0: float, z0: float, x1: float, y1: float, z1: float, chamfer: float = 1.0, segments: int = 4) -> None:
        """Box with chamfered (beveled) top edges."""
        cx0, cy0 = x0 + chamfer, y0 + chamfer
        cx1, cy1 = x1 - chamfer, y1 - chamfer
        cz = z1 - chamfer
        
        self.add_quad((x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0))
        
        self.add_quad((x0, y0, z0), (x0, y0, cz), (x1, y0, cz), (x1, y0, z0))
        self.add_quad((x1, y0, z0), (x1, y0, cz), (x1, y1, cz), (x1, y1, z0))
        self.add_quad((x1, y1, z0), (x1, y1, cz), (x0, y1, cz), (x0, y1, z0))
        self.add_quad((x0, y1, z0), (x0, y1, cz), (x0, y0, cz), (x0, y0, z0))
        
        p_cz_00, p_cz_10, p_cz_11, p_cz_01 = (x0, y0, cz), (x1, y0, cz), (x1, y1, cz), (x0, y1, cz)
        p_z1_00, p_z1_10, p_z1_11, p_z1_01 = (cx0, cy0, z1), (cx1, cy0, z1), (cx1, cy1, z1), (cx0, cy1, z1)
        
        self.add_quad(p_cz_00, p_z1_00, p_z1_10, p_cz_10)
        self.add_quad(p_cz_10, p_z1_10, p_z1_11, p_cz_11)
        self.add_quad(p_cz_11, p_z1_11, p_z1_01, p_cz_01)
        self.add_quad(p_cz_01, p_z1_01, p_z1_00, p_cz_00)
        
        self.add_quad(p_z1_00, p_z1_01, p_z1_11, p_z1_10)

    def add_hollow_cylinder(self, cx: float, cy: float, z0: float, z1: float, r_outer: float, r_inner: float, segments: int = 24) -> None:
        """Tube/pipe."""
        outer_bottom, outer_top, inner_bottom, inner_top = [], [], [], []
        for i in range(segments):
            angle = 2.0 * math.pi * i / segments
            c, s = math.cos(angle), math.sin(angle)
            outer_bottom.append((cx + r_outer * c, cy + r_outer * s, z0))
            outer_top.append((cx + r_outer * c, cy + r_outer * s, z1))
            inner_bottom.append((cx + r_inner * c, cy + r_inner * s, z0))
            inner_top.append((cx + r_inner * c, cy + r_inner * s, z1))
            
        for i in range(segments):
            next_i = (i + 1) % segments
            self.add_quad(outer_bottom[i], outer_bottom[next_i], outer_top[next_i], outer_top[i])
            self.add_quad(inner_bottom[next_i], inner_bottom[i], inner_top[i], inner_top[next_i])
            self.add_quad(inner_bottom[i], inner_bottom[next_i], outer_bottom[next_i], outer_bottom[i])
            self.add_quad(outer_top[i], outer_top[next_i], inner_top[next_i], inner_top[i])

    def add_rounded_box(self, x0: float, y0: float, z0: float, x1: float, y1: float, z1: float, radius: float = 2.0, segments: int = 8) -> None:
        """Box with rounded vertical edges."""
        cx0, cy0 = x0 + radius, y0 + radius
        cx1, cy1 = x1 - radius, y1 - radius
        
        corners = [
            (cx1, cy1, 0),
            (cx0, cy1, math.pi / 2),
            (cx0, cy0, math.pi),
            (cx1, cy0, 3 * math.pi / 2)
        ]
        
        points_bottom, points_top = [], []
        for cx, cy, start_angle in corners:
            for i in range(segments + 1):
                angle = start_angle + (math.pi / 2) * i / segments
                px = cx + radius * math.cos(angle)
                py = cy + radius * math.sin(angle)
                points_bottom.append((px, py, z0))
                points_top.append((px, py, z1))
                
        num_points = len(points_bottom)
        for i in range(num_points):
            next_i = (i + 1) % num_points
            self.add_quad(points_bottom[i], points_bottom[next_i], points_top[next_i], points_top[i])
            
        cx_mid, cy_mid = (x0 + x1) / 2, (y0 + y1) / 2
        center_bottom = (cx_mid, cy_mid, z0)
        center_top = (cx_mid, cy_mid, z1)
        
        for i in range(num_points):
            next_i = (i + 1) % num_points
            self.add_triangle(center_bottom, points_bottom[next_i], points_bottom[i])
            self.add_triangle(center_top, points_top[i], points_top[next_i])

    def add_sphere(self, cx: float, cy: float, cz: float, radius: float, u_segments: int = 16, v_segments: int = 12) -> None:
        """UV sphere."""
        for i in range(v_segments):
            v_angle1 = math.pi * i / v_segments
            v_angle2 = math.pi * (i + 1) / v_segments
            z1 = cz + radius * math.cos(v_angle1)
            z2 = cz + radius * math.cos(v_angle2)
            r1 = radius * math.sin(v_angle1)
            r2 = radius * math.sin(v_angle2)
            
            for j in range(u_segments):
                u_angle1 = 2 * math.pi * j / u_segments
                u_angle2 = 2 * math.pi * (j + 1) / u_segments
                
                p1 = (cx + r1 * math.cos(u_angle1), cy + r1 * math.sin(u_angle1), z1)
                p2 = (cx + r1 * math.cos(u_angle2), cy + r1 * math.sin(u_angle2), z1)
                p3 = (cx + r2 * math.cos(u_angle2), cy + r2 * math.sin(u_angle2), z2)
                p4 = (cx + r2 * math.cos(u_angle1), cy + r2 * math.sin(u_angle1), z2)
                
                if i == 0:
                    self.add_triangle(p1, p4, p3)
                elif i == v_segments - 1:
                    self.add_triangle(p1, p2, p4)
                else:
                    self.add_quad(p1, p4, p3, p2)

    def add_torus(self, cx: float, cy: float, cz: float, major_r: float, minor_r: float, major_seg: int = 24, minor_seg: int = 12) -> None:
        """Torus/ring shape."""
        for i in range(major_seg):
            u1 = 2 * math.pi * i / major_seg
            u2 = 2 * math.pi * (i + 1) / major_seg
            cos_u1, sin_u1 = math.cos(u1), math.sin(u1)
            cos_u2, sin_u2 = math.cos(u2), math.sin(u2)
            
            for j in range(minor_seg):
                v1 = 2 * math.pi * j / minor_seg
                v2 = 2 * math.pi * (j + 1) / minor_seg
                cos_v1, sin_v1 = math.cos(v1), math.sin(v1)
                cos_v2, sin_v2 = math.cos(v2), math.sin(v2)
                
                r1 = major_r + minor_r * cos_v1
                z1 = cz + minor_r * sin_v1
                r2 = major_r + minor_r * cos_v2
                z2 = cz + minor_r * sin_v2
                
                p1 = (cx + r1 * cos_u1, cy + r1 * sin_u1, z1)
                p2 = (cx + r1 * cos_u2, cy + r1 * sin_u2, z1)
                p3 = (cx + r2 * cos_u2, cy + r2 * sin_u2, z2)
                p4 = (cx + r2 * cos_u1, cy + r2 * sin_u1, z2)
                
                self.add_quad(p1, p2, p3, p4)

    def export_stl_binary(self, filepath: Path) -> Path:
        """Export the mesh as a standard binary STL file."""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        num_triangles = len(self.triangles)
        header = b"MakerWorld Autopilot Mesh Exporter - BambuLab Compatible"
        header = header.ljust(80, b"\0")

        with open(filepath, "wb") as f:
            f.write(header)
            f.write(struct.pack("<I", num_triangles))
            for v1, v2, v3 in self.triangles:
                norm = compute_normal(v1, v2, v3)
                # Normal (3f), V1 (3f), V2 (3f), V3 (3f), attribute byte count (H)
                f.write(struct.pack(
                    "<12fH",
                    norm[0], norm[1], norm[2],
                    v1[0], v1[1], v1[2],
                    v2[0], v2[1], v2[2],
                    v3[0], v3[1], v3[2],
                    0
                ))
        return filepath

    def export_3mf(self, filepath: Path, model_title: str = "AutopilotModel") -> Path:
        """Export the mesh as a valid Bambu-compatible 3MF package."""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Index vertices for 3MF model format
        vertex_map = {}
        unique_vertices = []
        indexed_triangles = []

        for tri in self.triangles:
            tri_indices = []
            for v in tri:
                # Round to 4 decimal places for deduplication
                key = (round(v[0], 4), round(v[1], 4), round(v[2], 4))
                if key not in vertex_map:
                    vertex_map[key] = len(unique_vertices)
                    unique_vertices.append(key)
                tri_indices.append(vertex_map[key])
            indexed_triangles.append(tri_indices)

        # Build 3D/3dmodel.model XML
        vertices_xml = "\n".join([f'      <vertex x="{x}" y="{y}" z="{z}" />' for x, y, z in unique_vertices])
        triangles_xml = "\n".join([f'      <triangle v1="{v1}" v2="{v2}" v3="{v3}" />' for v1, v2, v3 in indexed_triangles])

        model_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">
  <metadata name="Title">{model_title}</metadata>
  <metadata name="Designer">MakerWorld Autopilot</metadata>
  <metadata name="Description">Optimized 3D print profile for Bambu Lab printers</metadata>
  <resources>
    <object id="1" type="model">
      <mesh>
        <vertices>
{vertices_xml}
        </vertices>
        <triangles>
{triangles_xml}
        </triangles>
      </mesh>
    </object>
  </resources>
  <build>
    <item objectid="1" />
  </build>
</model>"""

        content_types_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
</Types>"""

        rels_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>"""

        with zipfile.ZipFile(filepath, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr("[Content_Types].xml", content_types_xml)
            zipf.writestr("_rels/.rels", rels_xml)
            zipf.writestr("3D/3dmodel.model", model_xml)

        return filepath

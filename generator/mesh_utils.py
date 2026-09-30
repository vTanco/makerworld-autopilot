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

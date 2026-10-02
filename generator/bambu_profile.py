import os
import tempfile
import zipfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Any

class BambuProfileInjector:
    def __init__(self):
        self.default_settings = {
            "layer_height": "0.20",
            "first_layer_height": "0.20",
            "wall_loops": "3",
            "top_shell_layers": "5",
            "bottom_shell_layers": "4",
            "sparse_infill_density": "15%",
            "sparse_infill_pattern": "gyroid",
            "support_type": "none",
            "filament_type": "PLA",
            "nozzle_diameter": "0.4",
            "print_speed": "250",
            "bed_temperature": "60",
            "nozzle_temperature": "220",
            "plate_type": "textured_pei",
            "printer_model": "Bambu Lab P1S 0.4 nozzle"
        }

    def _get_plate_config(self, settings: Dict[str, Any]) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<config>
  <plate>
    <metadata key="plater_id" value="1"/>
    <metadata key="plater_name" value=""/>
    <metadata key="locked" value="false"/>
    <metadata key="thumbnail_file" value="Metadata/plate_1.png"/>
    <metadata key="top_file" value="Metadata/plate_1_top.png"/>
    <metadata key="pick_file" value="Metadata/plate_1_pick.png"/>
    <metadata key="pattern_bbox_file" value="Metadata/plate_1_pattern_bbox.png"/>
  </plate>
  <object id="1">
    <metadata key="name" value="Model"/>
  </object>
</config>"""

    def _get_model_settings_config(self, settings: Dict[str, Any]) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<config>
  <object id="1">
    <setting key="layer_height" value="{settings.get('layer_height')}"/>
    <setting key="first_layer_height" value="{settings.get('first_layer_height')}"/>
    <setting key="wall_loops" value="{settings.get('wall_loops')}"/>
    <setting key="top_shell_layers" value="{settings.get('top_shell_layers')}"/>
    <setting key="bottom_shell_layers" value="{settings.get('bottom_shell_layers')}"/>
    <setting key="sparse_infill_density" value="{settings.get('sparse_infill_density')}"/>
    <setting key="sparse_infill_pattern" value="{settings.get('sparse_infill_pattern')}"/>
    <setting key="support_type" value="{settings.get('support_type')}"/>
  </object>
</config>"""

    def _get_project_settings_config(self, settings: Dict[str, Any]) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<config>
  <setting key="printer_model_id" value="{settings.get('printer_model')}"/>
  <setting key="filament_type" value="{settings.get('filament_type')}"/>
  <setting key="nozzle_diameter" value="{settings.get('nozzle_diameter')}"/>
  <setting key="print_speed" value="{settings.get('print_speed')}"/>
  <setting key="bed_temperature" value="{settings.get('bed_temperature')}"/>
  <setting key="nozzle_temperature" value="{settings.get('nozzle_temperature')}"/>
  <setting key="plate_type" value="{settings.get('plate_type')}"/>
</config>"""

    def _get_slice_info_config(self, settings: Dict[str, Any]) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<config>
  <plate id="1">
    <metadata key="estimated_time" value="3600"/>
    <metadata key="filament_weight" value="10"/>
  </plate>
</config>"""

    def _get_content_types_xml(self) -> str:
        return """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
  <Default Extension="config" ContentType="application/vnd.bambulab.bambustudio.config+xml"/>
</Types>"""

    def _get_rels_xml(self) -> str:
        return """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
  <Relationship Target="/Metadata/plate_1.config" Id="rel1" Type="http://schemas.bambulab.com/3dmanufacturing/2021/11/bambustudiometadata"/>
  <Relationship Target="/Metadata/model_settings.config" Id="rel2" Type="http://schemas.bambulab.com/3dmanufacturing/2021/11/bambustudiometadata"/>
  <Relationship Target="/Metadata/project_settings.config" Id="rel3" Type="http://schemas.bambulab.com/3dmanufacturing/2021/11/bambustudiometadata"/>
  <Relationship Target="/Metadata/slice_info.config" Id="rel4" Type="http://schemas.bambulab.com/3dmanufacturing/2021/11/bambustudiometadata"/>
</Relationships>"""

    def inject_profile(self, input_3mf_path: str, output_3mf_path: str, settings: Optional[Dict[str, Any]] = None):
        if settings is None:
            settings = self.default_settings.copy()
        else:
            merged = self.default_settings.copy()
            merged.update(settings)
            settings = merged

        temp_dir = tempfile.mkdtemp()
        try:
            with zipfile.ZipFile(input_3mf_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            metadata_dir = Path(temp_dir) / "Metadata"
            metadata_dir.mkdir(exist_ok=True)

            with open(metadata_dir / "plate_1.config", "w") as f:
                f.write(self._get_plate_config(settings))
            
            with open(metadata_dir / "model_settings.config", "w") as f:
                f.write(self._get_model_settings_config(settings))
                
            with open(metadata_dir / "project_settings.config", "w") as f:
                f.write(self._get_project_settings_config(settings))
                
            with open(metadata_dir / "slice_info.config", "w") as f:
                f.write(self._get_slice_info_config(settings))
                
            with open(Path(temp_dir) / "[Content_Types].xml", "w") as f:
                f.write(self._get_content_types_xml())
                
            rels_dir = Path(temp_dir) / "_rels"
            rels_dir.mkdir(exist_ok=True)
            with open(rels_dir / ".rels", "w") as f:
                f.write(self._get_rels_xml())

            with zipfile.ZipFile(output_3mf_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        # Replace backslashes with forward slashes for zip archive paths
                        arcname = arcname.replace('\\', '/')
                        zipf.write(file_path, arcname)
                        
        finally:
            shutil.rmtree(temp_dir)

    def create_bambu_3mf(self, mesh, output_path: str, model_title: str, settings: Optional[Dict[str, Any]] = None):
        temp_3mf = tempfile.mktemp(suffix=".3mf")
        try:
            mesh.export_3mf(temp_3mf, model_title=model_title)
            self.inject_profile(temp_3mf, output_path, settings)
        finally:
            if os.path.exists(temp_3mf):
                os.unlink(temp_3mf)

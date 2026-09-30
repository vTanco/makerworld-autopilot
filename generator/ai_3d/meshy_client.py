"""
Client for Meshy AI Text-to-3D and Image-to-3D APIs.
Allows autonomous generation of complex artistic models (figurines, decorative items) via AI.
"""

import os
import time
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Dict, Optional


class MeshyClient:
    BASE_URL = "https://api.meshy.ai/v2"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("MESHY_API_KEY", "")

    def is_configured(self) -> bool:
        return bool(self.api_key.strip())

    def create_text_to_3d_task(self, prompt: str, art_style: str = "realistic") -> Dict[str, Any]:
        """Submit a text-to-3D generation task."""
        if not self.is_configured():
            raise ValueError("MESHY_API_KEY is not configured.")

        url = f"{self.BASE_URL}/text-to-3d"
        payload = json.dumps({
            "mode": "preview",
            "prompt": prompt,
            "art_style": art_style,
            "negative_prompt": "low quality, low resolution, broken geometry, non-manifold"
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def poll_task(self, task_id: str, timeout_seconds: int = 300) -> Dict[str, Any]:
        """Poll task until completion."""
        url = f"{self.BASE_URL}/text-to-3d/{task_id}"
        start_time = time.time()

        while time.time() - start_time < timeout_seconds:
            req = urllib.request.Request(
                url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                method="GET"
            )
            with urllib.request.urlopen(req) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                status = res.get("status")
                if status == "SUCCEEDED":
                    return res
                elif status in ["FAILED", "EXPIRED"]:
                    raise RuntimeError(f"Meshy generation failed: {res.get('task_error', 'Unknown error')}")
            time.sleep(5)
        raise TimeoutError("Meshy generation timed out.")

    def download_model(self, download_url: str, output_path: Path) -> Path:
        """Download resulting 3D model file (GLB or STL)."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(download_url, str(output_path))
        return output_path

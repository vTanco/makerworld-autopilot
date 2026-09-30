"""
Base Generator class for MakerWorld 3D models.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Tuple
from generator.mesh_utils import Mesh


class BaseGenerator(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def category(self) -> str:
        pass

    @abstractmethod
    def generate(self, params: Dict[str, Any] = None) -> Tuple[Mesh, Dict[str, Any]]:
        """
        Generates the 3D mesh and metadata.
        Returns: (Mesh, metadata_dict)
        """
        pass

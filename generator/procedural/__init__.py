"""
Procedural generator registry.
"""

from typing import Dict, Type
from generator.base import BaseGenerator
from generator.procedural.gridfinity import GridfinityGenerator
from generator.procedural.phone_stand import PhoneStandGenerator
from generator.procedural.cable_holder import CableHolderGenerator
from generator.procedural.modular_bracket import ModularBracketGenerator

PROCEDURAL_REGISTRY: Dict[str, Type[BaseGenerator]] = {
    "gridfinity": GridfinityGenerator,
    "phone_stand": PhoneStandGenerator,
    "cable_holder": CableHolderGenerator,
    "modular_bracket": ModularBracketGenerator,
}


def get_generator(name: str) -> BaseGenerator:
    cls = PROCEDURAL_REGISTRY.get(name.lower())
    if not cls:
        raise ValueError(f"Unknown generator '{name}'. Available: {list(PROCEDURAL_REGISTRY.keys())}")
    return cls()

"""
Procedural generator registry.
"""

from typing import Dict, Type
from generator.base import BaseGenerator
from generator.procedural.gridfinity import GridfinityGenerator
from generator.procedural.phone_stand import PhoneStandGenerator
from generator.procedural.cable_holder import CableHolderGenerator
from generator.procedural.modular_bracket import ModularBracketGenerator
from generator.procedural.bambu_poop_chute import BambuPoopChuteGenerator
from generator.procedural.sd_usb_caddy import SDUsbCaddyGenerator
from generator.procedural.headphone_hanger import HeadphoneHangerGenerator
from generator.procedural.hex_wrench_caddy import HexWrenchCaddyGenerator
from generator.procedural.ptfe_filament_clip import PTFEFilamentClipGenerator

PROCEDURAL_REGISTRY: Dict[str, Type[BaseGenerator]] = {
    "gridfinity": GridfinityGenerator,
    "phone_stand": PhoneStandGenerator,
    "cable_holder": CableHolderGenerator,
    "modular_bracket": ModularBracketGenerator,
    "bambu_poop_chute": BambuPoopChuteGenerator,
    "sd_usb_caddy": SDUsbCaddyGenerator,
    "headphone_hanger": HeadphoneHangerGenerator,
    "hex_wrench_caddy": HexWrenchCaddyGenerator,
    "ptfe_filament_clip": PTFEFilamentClipGenerator,
}


def get_generator(name: str) -> BaseGenerator:
    cls = PROCEDURAL_REGISTRY.get(name.lower())
    if not cls:
        raise ValueError(f"Unknown generator '{name}'. Available: {list(PROCEDURAL_REGISTRY.keys())}")
    return cls()

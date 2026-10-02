"""
Viral Product Photography Prompt Generator.
Creates highly engaging, click-worthy AI image prompts for MakerWorld listings.
Designed to maximize thumbnail appeal and drive downloads.
"""

from typing import Dict, Any, List


# Photography styles that drive the most engagement on 3D printing marketplaces
PHOTO_STYLES = {
    "hero_lifestyle": {
        "style": "Professional product photography, warm natural lighting, shallow depth of field, bokeh background",
        "context": "clean modern desk setup with plants and warm ambient lighting",
        "mood": "aspirational, premium, inviting"
    },
    "pei_fresh": {
        "style": "Close-up macro product photo, sharp focus, studio lighting",
        "context": "sitting on gold textured PEI build plate inside Bambu Lab 3D printer, fresh off the print bed with slight sheen",
        "mood": "satisfying, fresh, technical"
    },
    "handheld_scale": {
        "style": "Casual authentic photo, natural indoor lighting, iPhone camera aesthetic, slight motion blur",
        "context": "held in a person's hand to show scale, workshop or home office background",
        "mood": "authentic, relatable, real"
    },
    "in_use": {
        "style": "Action lifestyle shot, dynamic composition, natural lighting with warm tones",
        "context": "product being actively used in its intended environment",
        "mood": "functional, practical, inspiring"
    },
    "collection": {
        "style": "Flat lay product arrangement, top-down view, clean white background, soft even lighting",
        "context": "multiple color variants arranged aesthetically with complementary accessories",
        "mood": "variety, choice, professional"
    }
}

# Template-specific scene descriptions for maximum visual impact
TEMPLATE_SCENES: Dict[str, Dict[str, str]] = {
    "gridfinity": {
        "product": "a 3D printed modular storage bin organizer in matte white PLA with dividers, filled with small electronic components, screws, and resistors",
        "in_use": "on a maker's workbench next to a soldering iron and multimeter, with neatly sorted components visible inside the compartments",
        "color_variants": "in matte white, matte black, and sky blue, arranged side by side"
    },
    "phone_stand": {
        "product": "a sleek 3D printed phone stand in matte black PLA holding an iPhone showing a video call, with clean desk setup",
        "in_use": "on a minimalist desk with a MacBook and coffee cup, phone propped at perfect viewing angle for a FaceTime call",
        "color_variants": "in white, charcoal gray, and sage green"
    },
    "cable_holder": {
        "product": "a compact 3D printed cable management clip in white PLA, holding organized USB-C and HDMI cables on a desk edge",
        "in_use": "attached to the back edge of a walnut desk, neatly routing multiple charging cables that would otherwise dangle",
        "color_variants": "in matte white and matte black, mounted on light and dark desk edges"
    },
    "modular_bracket": {
        "product": "a heavy-duty 3D printed structural bracket in gray PETG with visible reinforcement gusset, industrial appearance",
        "in_use": "mounted on a DIY wooden shelf project, supporting a heavy load with visible structural integrity",
        "color_variants": "in gray, black, and white PETG"
    },
    "bambu_poop_chute": {
        "product": "a 3D printed Bambu Lab purge chute deflector in matte black PLA, precision-fit accessory",
        "in_use": "mounted on a Bambu Lab P1S printer, directing purge filament into a small trash bin below, clean printing workspace",
        "color_variants": "in matte black matching the printer aesthetic"
    },
    "sd_usb_caddy": {
        "product": "a compact 3D printed memory card organizer holding SD cards and USB drives, in white PLA on a photographer's desk",
        "in_use": "next to a camera, laptop, and drone controller with SD cards neatly organized and easily accessible",
        "color_variants": "in white and matte black, showing different slot configurations"
    },
    "headphone_hanger": {
        "product": "a minimalist 3D printed under-desk headphone hook in matte black PLA, holding premium over-ear headphones",
        "in_use": "mounted under a gaming desk, supporting a pair of Sony WH-1000XM5 headphones, RGB keyboard visible in background",
        "color_variants": "in matte black, white, and navy blue"
    },
    "hex_wrench_caddy": {
        "product": "a 3D printed hex key organizer caddy in gray PLA, holding a complete set of metric Allen wrenches sorted by size",
        "in_use": "on a 3D printer workstation next to a Bambu Lab printer, with hex keys, nozzles, and a maintenance scraper neatly organized",
        "color_variants": "in Bambu Lab gray and matte black"
    },
    "ptfe_filament_clip": {
        "product": "a small 3D printed filament clip in orange PLA clamped onto a spool of filament, keeping the end secured",
        "in_use": "attached to an AMS filament spool preventing tangles, with multiple clips visible on adjacent spools in different colors",
        "color_variants": "in orange, red, blue, and green — one for each AMS slot"
    },
    "watch_dock": {
        "product": "an elegant 3D printed smartwatch charging dock in white PLA with circular base and tapered pillar, Apple Watch sitting on cradle",
        "in_use": "on a nightstand next to a lamp and book, Apple Watch glowing softly on the dock charging overnight",
        "color_variants": "in matte white, matte black, and walnut-colored PLA"
    },
    "controller_stand": {
        "product": "a 3D printed game controller display stand in matte black PLA holding a PS5 DualSense controller upright",
        "in_use": "on a gaming desk setup next to a monitor, with controller displayed prominently, RGB ambient lighting in background",
        "color_variants": "in matte black, white, and PlayStation blue"
    },
    "pen_holder": {
        "product": "a cylindrical 3D printed dual pen holder in silk copper PLA, holding pens, markers, and an Apple Pencil",
        "in_use": "on a creative professional's desk next to an iPad and sketchbook, markers and styluses easily accessible",
        "color_variants": "in silk copper, silk gold, matte black, and matte white"
    },
    "monitor_riser": {
        "product": "a wide 3D printed monitor riser stand in white PLA with cylindrical legs, laptop sitting on top",
        "in_use": "on a clean desk with keyboard stored underneath, monitor at perfect ergonomic eye level, plants and peripherals arranged around it",
        "color_variants": "in white and matte black, showing both pillar and wall leg styles"
    },
    "tool_mount": {
        "product": "a wall-mounted 3D printed tool organizer in gray PETG with screwdrivers and pliers inserted in cylindrical slots",
        "in_use": "mounted on a workshop pegboard wall, tools neatly organized and easily grabable, workbench visible below",
        "color_variants": "in gray and black PETG"
    }
}

# Default scene for any template not explicitly defined
DEFAULT_SCENE = {
    "product": "a functional 3D printed accessory in matte white PLA with visible layer lines, professional product photo",
    "in_use": "being used in a modern home office or workshop setting, demonstrating practical functionality",
    "color_variants": "in matte white, black, and gray"
}


def get_photo_prompts(template_name: str, title: str = "") -> List[Dict[str, str]]:
    """
    Generates a list of optimized AI image generation prompts for a given template.
    Returns list of dicts with 'name', 'prompt', and 'aspect_ratio' keys.
    """
    scene = TEMPLATE_SCENES.get(template_name, DEFAULT_SCENE)
    
    prompts = [
        {
            "name": "01_hero_desk",
            "prompt": (
                f"Professional product photography of {scene['product']}. "
                f"{PHOTO_STYLES['hero_lifestyle']['style']}. "
                f"Set on a {PHOTO_STYLES['hero_lifestyle']['context']}. "
                "Shot with iPhone 15 Pro, 24mm lens, f/1.78. "
                "Photorealistic, editorial quality, trending on Behance. "
                "The object has visible FDM 3D print layer lines showing it's genuinely printed."
            ),
            "aspect_ratio": "3:2"
        },
        {
            "name": "02_pei_bed",
            "prompt": (
                f"Close-up product photo of {scene['product']} "
                f"sitting directly on a gold textured PEI spring steel build plate "
                f"inside a Bambu Lab 3D printer print chamber. "
                "The object has just finished printing with slight warm sheen. "
                "LED chamber lights illuminating the print. "
                "Bambu Lab logo visible on printer. Authentic maker photography."
            ),
            "aspect_ratio": "3:2"
        },
        {
            "name": "03_handheld",
            "prompt": (
                f"Casual authentic photo of {scene['product']} "
                f"being held up by a person's hand to show scale. "
                f"Background shows a home office or workshop, slightly out of focus. "
                "Natural indoor lighting, genuine amateur photography aesthetic. "
                "The 3D print has visible layer texture confirming real FDM printing. "
                "Shot on iPhone, candid and relatable."
            ),
            "aspect_ratio": "3:2"
        },
        {
            "name": "04_in_use",
            "prompt": (
                f"Lifestyle action photo showing {scene['in_use']}. "
                f"{PHOTO_STYLES['in_use']['style']}. "
                "The 3D printed item is the focal point, clearly visible and in active use. "
                "Professional but approachable photography style. "
                "Warm color palette, high engagement composition."
            ),
            "aspect_ratio": "3:2"
        }
    ]
    
    return prompts


def get_thumbnail_prompt(template_name: str, title: str = "") -> Dict[str, str]:
    """
    Generates a single high-impact thumbnail prompt optimized for 4:3 cover images.
    This is the most important image — it's what appears in search results.
    """
    scene = TEMPLATE_SCENES.get(template_name, DEFAULT_SCENE)
    
    return {
        "name": "00_thumbnail",
        "prompt": (
            f"Eye-catching product hero shot of {scene['product']}. "
            "Clean gradient background transitioning from dark charcoal to slate gray. "
            "Dramatic studio lighting with key light from upper-left creating defined shadows. "
            "Product centered and prominent, filling 70% of frame. "
            "Ultra-sharp focus, professional e-commerce product photography. "
            "Visible 3D print layer lines for authenticity. "
            "4:3 aspect ratio, no text overlays, no watermarks."
        ),
        "aspect_ratio": "4:3"
    }

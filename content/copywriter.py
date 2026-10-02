"""
Autonomous SEO & Copywriting Engine.
Generates search-optimized listing content, descriptions, and promotional social posts.
"""

import os
import json
import urllib.request
from typing import Dict, Any, List
from content.templates import MAKERWORLD_DESCRIPTION_TEMPLATE, REDDIT_POST_TEMPLATE, PINTEREST_PIN_TEMPLATE


class Copywriter:
    def __init__(self, provider: str = "builtin"):
        self.provider = provider

    def generate_listing(self, meta: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates full listing package: title, description, tags, social copy.
        """
        title = meta.get("title", "Functional 3D Print Model")
        dimensions = meta.get("dimensions_mm", "50x50x50")
        layer_height = meta.get("suggested_layer_height", 0.20)
        infill = meta.get("suggested_infill", "15% Gyroid")
        highlight = meta.get("description_highlight", "High quality functional 3D printable model.")
        print_time = meta.get("estimated_print_time", "45 minutes")
        tags = meta.get("tags", ["3dprinting", "bambulab", "functional"])
        
        # Calculate weight if not provided
        weight = meta.get("weight")
        if weight is None:
            try:
                dims = [float(d.strip()) for d in dimensions.split('x')]
                if len(dims) == 3:
                    volume_cm3 = (dims[0] * dims[1] * dims[2]) / 1000
                    weight = round(volume_cm3 * 1.24, 1)
                else:
                    weight = 15.0
            except:
                weight = 15.0

        assembly_steps = meta.get("assembly_steps", "5. Enjoy your new print!")
        material_tip = meta.get("material_tip", "Dry your filament for best results.")

        # High-quality Spanish description highlights per template
        _ES_HIGHLIGHTS = {
            "gridfinity": "Bandeja modular de almacenamiento compatible con el sistema Gridfinity. Perfecta para organizar tornillos, componentes electrónicos y herramientas pequeñas. Imprime sin soportes en menos de 1 hora.",
            "phone_stand": "Soporte ergonómico para móvil con ángulo de visualización optimizado para videollamadas, FaceTime y notificaciones. Diseño minimalista que combina con cualquier escritorio.",
            "cable_holder": "Clip organizador de cables para escritorio. Mantén tus cables USB-C, HDMI y de carga siempre ordenados y accesibles. Se adhiere al borde del escritorio sin herramientas.",
            "modular_bracket": "Escuadra de refuerzo estructural de alta resistencia con nervadura triangular central. Ideal para proyectos de bricolaje, estanterías y talleres.",
            "bambu_poop_chute": "Deflector de purga para impresoras Bambu Lab. Redirige los residuos de filamento directamente a la papelera. Compatible con A1, A1 mini, P1S y X1C.",
            "sd_usb_caddy": "Organizador compacto de escritorio para tarjetas SD, MicroSD y memorias USB. Mantén tu equipo de fotografía y accesorios de impresión 3D siempre ordenados.",
            "headphone_hanger": "Gancho minimalista para auriculares bajo escritorio. Cuna de 38mm que protege la diadema. Mantén tu setup gaming limpio y organizado.",
            "hex_wrench_caddy": "Organizador de llaves Allen y herramientas de mantenimiento para Bambu Lab. Llaves hex de 1.5mm a 4.0mm, boquillas de repuesto y espátula siempre a mano.",
            "ptfe_filament_clip": "Clip de filamento PTFE de doble propósito. Sujeta el extremo del filamento en el carrete y guía los tubos Bowden. Impresión rápida en menos de 20 minutos.",
            "watch_dock": "Base de carga elegante para Apple Watch y smartwatches compatibles. Base circular con peso para estabilidad, pilar cónico y canal trasero para el cable.",
            "controller_stand": "Soporte universal para mandos de videojuegos. Compatible con PS5 DualSense, Xbox Series, Nintendo Switch Pro y Joy-Con. Incluye paso de cable de carga.",
            "pen_holder": "Porta bolígrafos y estiletes cilíndrico de diseño. Perfecto para Apple Pencil, rotuladores y bolígrafos de escritorio. Acabado profesional en PLA mate.",
            "monitor_riser": "Elevador ergonómico para monitor y portátil. Eleva la pantalla al nivel de los ojos y libera espacio debajo para guardar el teclado. Incluye gestión de cables.",
            "tool_mount": "Organizador de herramientas de pared con ranuras cilíndricas para destornilladores, alicates y marcadores. Incluye agujeros de montaje y tira para etiquetas.",
        }
        template_name = meta.get("template_used", "")
        highlight_es = meta.get("description_highlight_es")
        if not highlight_es or highlight_es == "Gran modelo funcional para organizar tu espacio.":
            highlight_es = _ES_HIGHLIGHTS.get(template_name, 
                f"Modelo funcional impreso en 3D de alta calidad. Diseñado para imprimir sin soportes en impresoras Bambu Lab. Descarga el archivo .3mf con perfil de impresión preconfigurado."
            )

        # Try AI enrichment if configured
        if self.provider == "gemini" and os.getenv("GEMINI_API_KEY"):
            try:
                ai_result = self._generate_with_gemini(meta)
                if ai_result:
                    return ai_result
            except Exception as e:
                print(f"[Copywriter] Gemini API call failed, falling back to builtin templates: {e}")

        # Builtin High-Converting Markdown
        description = MAKERWORLD_DESCRIPTION_TEMPLATE.format(
            title=title,
            description_highlight=highlight,
            description_highlight_es=highlight_es,
            dimensions=dimensions,
            weight=weight,
            layer_height=layer_height,
            infill=infill,
            print_time=print_time,
            assembly_steps=assembly_steps,
            material_tip=material_tip
        )

        reddit_body = REDDIT_POST_TEMPLATE.format(
            title=title,
            print_time=print_time,
            makerworld_url="{makerworld_url}"
        )

        return {
            "title": title,
            "description": description,
            "tags": tags,
            "reddit_post": reddit_body,
            "pinterest_pin": PINTEREST_PIN_TEMPLATE.format(
                title=title,
                makerworld_url="{makerworld_url}"
            )
        }

    def _generate_with_gemini(self, meta: Dict[str, Any]) -> Dict[str, Any]:
        api_key = os.getenv("GEMINI_API_KEY")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        prompt = f"""You are a top 3D printing creator on MakerWorld. Write a high-converting listing for:
Title: {meta.get('title')}
Dimensions: {meta.get('dimensions_mm')}
Highlight: {meta.get('description_highlight')}

Return ONLY JSON with these exact keys:
{{
  "title": "catchy SEO title under 70 chars",
  "description": "rich markdown description with features, print settings table, and boost call-to-action",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8"]
}}"""

        req_body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"response_mime_type": "application/json"}
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(req_body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(text)
            parsed["reddit_post"] = REDDIT_POST_TEMPLATE.format(
                title=parsed["title"],
                print_time=meta.get("estimated_print_time", "45 minutes"),
                makerworld_url="{makerworld_url}"
            )
            parsed["pinterest_pin"] = PINTEREST_PIN_TEMPLATE.format(
                title=parsed["title"],
                makerworld_url="{makerworld_url}"
            )
            return parsed

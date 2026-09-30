"""
Webhook Notification Client (Discord, Telegram & WhatsApp).
Sends rich embedded alerts when models are generated, uploaded, or points are earned.
"""

import json
import urllib.request
import urllib.parse
import urllib.error
import ssl
from typing import Dict, Any, Optional


class WebhookNotifier:
    def __init__(
        self,
        discord_url: Optional[str] = None,
        telegram_token: Optional[str] = None,
        telegram_chat_id: Optional[str] = None,
        whatsapp_phone: Optional[str] = None,
        whatsapp_apikey: Optional[str] = None,
    ):
        self.discord_url = discord_url or ""
        self.telegram_token = telegram_token or ""
        self.telegram_chat_id = telegram_chat_id or ""
        self.whatsapp_phone = whatsapp_phone or ""
        self.whatsapp_apikey = whatsapp_apikey or ""

    def send_discord_alert(self, title: str, description: str, fields: list = None, color: int = 0x2E86AB) -> bool:
        if not self.discord_url:
            return False

        payload = {
            "username": "MakerWorld Autopilot",
            "avatar_url": "https://makerworld.bblmw.com/static/image/logo.png",
            "embeds": [{
                "title": title,
                "description": description,
                "color": color,
                "fields": fields or [],
                "footer": {"text": "MakerWorld Autonomous Engine • 100% Autopilot"}
            }]
        }

        try:
            req = urllib.request.Request(
                self.discord_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "User-Agent": "MakerWorldAutopilot/1.0"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=8):
                return True
        except Exception as e:
            print(f"[Webhook] Discord notification error: {e}")
            return False

    def send_telegram_alert(self, message: str) -> bool:
        if not self.telegram_token or not self.telegram_chat_id:
            return False

        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        try:
            ssl_ctx = ssl._create_unverified_context()
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, context=ssl_ctx, timeout=10):
                return True
        except Exception as e:
            print(f"[Webhook] Telegram notification error: {e}")
            return False

    def send_whatsapp_alert(self, message: str) -> bool:
        """Sends WhatsApp notification using the CallMeBot free API."""
        if not self.whatsapp_phone or not self.whatsapp_apikey:
            return False

        clean_phone = self.whatsapp_phone.replace("+", "").replace(" ", "").replace("-", "")
        encoded_msg = urllib.parse.quote(message)
        url = f"https://api.callmebot.com/whatsapp.php?phone={clean_phone}&text={encoded_msg}&apikey={self.whatsapp_apikey}"

        try:
            ssl_ctx = ssl._create_unverified_context()
            req = urllib.request.Request(url, headers={"User-Agent": "MakerWorldAutopilot/1.0"})
            with urllib.request.urlopen(req, context=ssl_ctx, timeout=10) as resp:
                return resp.status == 200
        except Exception as e:
            print(f"[Webhook] WhatsApp notification error: {e}")
            return False

    def notify_model_ready(self, model_data: Dict[str, Any]) -> None:
        title = f"🚀 New 3D Model Prepared: {model_data.get('title')}"
        url_link = model_data.get("makerworld_url") or "https://makerworld.com/en/my/models"
        desc = f"**Status:** {model_data.get('status')}\n**Category:** {model_data.get('category')}\n**URL:** {url_link}"
        fields = [
            {"name": "Dimensions", "value": model_data.get("dimensions_mm", "N/A"), "inline": True},
            {"name": "Print Profile", "value": "Bambu 3MF Generated", "inline": True},
        ]
        
        # 1. Discord
        self.send_discord_alert(title, desc, fields, color=0x2ECC71)
        
        # 2. Telegram
        mw_status = "Publicado en vivo 🎉" if model_data.get('status') == 'published' else "Guardado en MakerWorld 📝"
        tg_text = (
            f"🚀 <b>¡Nuevo Modelo en MakerWorld!</b>\n\n"
            f"📦 <b>Título:</b> {model_data.get('title')}\n"
            f"🏷️ <b>Categoría:</b> {model_data.get('category')}\n"
            f"📊 <b>Estado:</b> <code>{mw_status}</code>\n"
            f"📐 <b>Dimensiones:</b> <code>{model_data.get('dimensions_mm', 'Optimizado')}</code>\n\n"
            f"🔗 <b>Enlace:</b> <a href=\"{url_link}\">{url_link}</a>\n\n"
            f"🤖 <i>Generado y publicado por MakerWorld Autopilot</i>"
        )
        self.send_telegram_alert(tg_text)
        
        # 3. WhatsApp
        wa_msg = f"🚀 *MakerWorld Autopilot*\nNuevo modelo procesado:\n*{model_data.get('title')}*\nEstado: {model_data.get('status')}\n🔗 {url_link}"
        self.send_whatsapp_alert(wa_msg)

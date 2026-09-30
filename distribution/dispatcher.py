"""
Social Distribution Dispatcher.
Coordinates multi-platform syndication across Reddit, Pinterest, Discord, and Telegram.
"""

from typing import Dict, Any, List
from distribution.webhook_notifier import WebhookNotifier
from distribution.reddit_client import RedditPoster
from core.database import Database


class DistributionDispatcher:
    def __init__(self, config: Dict[str, Any] = None, db: Database = None):
        config = config or {}
        self.db = db
        webhooks = config.get("webhooks", {})
        self.notifier = WebhookNotifier(
            discord_url=webhooks.get("discord_webhook_url"),
            telegram_token=webhooks.get("telegram_bot_token"),
            telegram_chat_id=webhooks.get("telegram_chat_id"),
            whatsapp_phone=webhooks.get("whatsapp_phone"),
            whatsapp_apikey=webhooks.get("whatsapp_apikey"),
        )
        self.reddit = RedditPoster(config.get("reddit", {}))

    def dispatch(self, model_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Distribute the model across all configured channels."""
        results = []

        # 1. Webhook alert
        self.notifier.notify_model_ready(model_data)

        # 2. Reddit Syndication
        reddit_res = self.reddit.post_model(model_data)
        results.append(reddit_res)
        if self.db:
            self.db.record_distribution(
                model_id=model_data["id"],
                platform="reddit",
                post_url=reddit_res.get("post_url"),
                status=reddit_res.get("status"),
                error_message=reddit_res.get("error")
            )

        return results

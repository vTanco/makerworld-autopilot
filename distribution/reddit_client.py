"""
Reddit Promotional Poster for 3D Printing communities.
Generates shareable copy and posts to configured subreddits when API credentials are provided.
"""

import os
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional


class RedditPoster:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.enabled = self.config.get("enabled", False)
        self.client_id = self.config.get("client_id", "")
        self.client_secret = self.config.get("client_secret", "")
        self.username = self.config.get("username", "")
        self.password = self.config.get("password", "")
        self.subreddits = self.config.get("subreddits", ["3Dprinting"])

    def is_configured(self) -> bool:
        return bool(self.enabled and self.client_id and self.client_secret and self.username and self.password)

    def post_model(self, model_data: Dict[str, Any]) -> Dict[str, Any]:
        """Posts to configured subreddits or stages post for manual copy-paste."""
        title = f"[Free 3MF] {model_data.get('title')}"
        url = model_data.get("makerworld_url") or "https://makerworld.com"
        reddit_text = (model_data.get("reddit_post") or "").replace("{makerworld_url}", str(url))

        if not self.is_configured():
            return {
                "status": "staged_for_manual_share",
                "platform": "reddit",
                "ready_title": title,
                "ready_body": reddit_text,
                "note": "Reddit credentials not set in config.yaml. Text is pre-formatted and ready to paste."
            }

        # Authentic Reddit API posting logic (OAuth2 password flow)
        try:
            auth = f"{self.client_id}:{self.client_secret}"
            import base64
            auth_encoded = base64.b64encode(auth.encode()).decode()

            token_data = urllib.parse.urlencode({
                "grant_type": "password",
                "username": self.username,
                "password": self.password
            }).encode()

            token_req = urllib.request.Request(
                "https://www.reddit.com/api/v1/access_token",
                data=token_data,
                headers={
                    "Authorization": f"Basic {auth_encoded}",
                    "User-Agent": "MakerWorldAutopilot/1.0"
                },
                method="POST"
            )
            with urllib.request.urlopen(token_req) as resp:
                token = json.loads(resp.read().decode())["access_token"]

            # Submit link/text post
            sub = self.subreddits[0]
            post_data = urllib.parse.urlencode({
                "sr": sub,
                "kind": "self",
                "title": title,
                "text": reddit_text
            }).encode()

            submit_req = urllib.request.Request(
                "https://oauth.reddit.com/api/submit",
                data=post_data,
                headers={
                    "Authorization": f"Bearer {token}",
                    "User-Agent": "MakerWorldAutopilot/1.0"
                },
                method="POST"
            )
            with urllib.request.urlopen(submit_req) as resp:
                result = json.loads(resp.read().decode())
                post_url = result.get("json", {}).get("data", {}).get("url")
                return {
                    "status": "published",
                    "platform": "reddit",
                    "subreddit": sub,
                    "post_url": post_url
                }
        except Exception as e:
            return {
                "status": "error",
                "platform": "reddit",
                "error": str(e)
            }

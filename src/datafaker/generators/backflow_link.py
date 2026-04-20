from __future__ import annotations

from datafaker.generators.base import BaseGenerator
from datafaker.utils.random_data import random_choice, random_slug


class BackflowLinkGenerator(BaseGenerator):
    def build_payload(self, index: int) -> dict:
        code = random_slug("lk")
        return {
            "link_id": f"BLK-{index:08d}",
            "source": random_choice(["sms", "email", "wechat", "app_push"]),
            "short_code": code,
            "short_url": f"https://go.example.com/{code}",
            "target_url": f"https://example.com/returning/{index}",
            "expired": False,
        }

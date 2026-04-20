from __future__ import annotations

from datafaker.generators.base import BaseGenerator
from datafaker.utils.random_data import random_choice, random_slug, random_title


class BackflowLandingPageGenerator(BaseGenerator):
    def build_payload(self, index: int) -> dict:
        page_slug = random_slug("backflow-lp")
        return {
            "page_id": f"BLP-{index:08d}",
            "title": random_title("backflow-page"),
            "campaign_id": f"CMP-{index:06d}",
            "url": f"https://example.com/b/{page_slug}",
            "channel": random_choice(["sms", "email", "push", "ads"]),
            "status": random_choice(["draft", "published"]),
        }

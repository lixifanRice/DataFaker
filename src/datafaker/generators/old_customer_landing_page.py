from __future__ import annotations

from datafaker.generators.base import BaseGenerator
from datafaker.utils.random_data import random_choice, random_slug, random_title


class OldCustomerLandingPageGenerator(BaseGenerator):
    def build_payload(self, index: int) -> dict:
        slug = random_slug("old-customer-lp")
        return {
            "page_id": f"OLP-{index:08d}",
            "title": random_title("old-customer"),
            "url": f"https://example.com/old/{slug}",
            "segment": random_choice(["high_value", "silent_30d", "silent_90d"]),
            "benefit_tag": random_choice(["coupon", "gift", "bundle", "free_shipping"]),
            "status": random_choice(["draft", "published"]),
        }

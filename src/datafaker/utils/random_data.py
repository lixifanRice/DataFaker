from __future__ import annotations

import random
import string


def random_slug(prefix: str) -> str:
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}-{suffix}"


def random_title(prefix: str) -> str:
    words = [
        "alpha",
        "beta",
        "premium",
        "plus",
        "growth",
        "pro",
        "edge",
        "smart",
        "ultra",
    ]
    return f"{prefix}-{random.choice(words)}-{random.randint(100, 999)}"


def random_choice(options: list[str]) -> str:
    return random.choice(options)

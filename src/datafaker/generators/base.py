from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from uuid import uuid4


class BaseGenerator(ABC):
    include_meta = False

    @abstractmethod
    def build_payload(self, index: int) -> dict:
        """Build business payload for one record."""

    def generate(self, index: int) -> dict:
        payload = self.build_payload(index)
        if self.include_meta:
            payload.setdefault("trace_id", uuid4().hex)
            payload.setdefault("generated_at", datetime.now(timezone.utc).isoformat())
        return payload

from __future__ import annotations

import logging
import time

import requests
from requests.adapters import HTTPAdapter

from datafaker.models import SubmitResult


class APIClient:
    def __init__(
        self,
        base_url: str,
        token: str = "",
        default_headers: dict[str, str] | None = None,
        timeout_seconds: float = 10.0,
        max_retries: int = 3,
        retry_backoff_seconds: float = 0.5,
        connection_pool_size: int = 100,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.default_headers = dict(default_headers or {})
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.retry_backoff_seconds = retry_backoff_seconds
        self.connection_pool_size = connection_pool_size
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = requests.Session()
        adapter = HTTPAdapter(
            pool_connections=self.connection_pool_size,
            pool_maxsize=self.connection_pool_size,
            max_retries=0,
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def close(self) -> None:
        self.session.close()

    def create(self, endpoint: str, payload: dict) -> SubmitResult:
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            url = endpoint
        else:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {"Content-Type": "application/json", **self.default_headers}
        has_authorization = any(key.lower() == "authorization" for key in headers)
        if self.token and not has_authorization:
            headers["Authorization"] = f"Bearer {self.token}"

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=self.timeout_seconds,
                )
                if 200 <= response.status_code < 300:
                    return SubmitResult(success=True, status_code=response.status_code)

                text = (response.text or "").strip().replace("\n", " ")
                message = f"HTTP {response.status_code}: {text[:200]}"
                if response.status_code >= 500 and attempt < self.max_retries:
                    time.sleep(self.retry_backoff_seconds * attempt)
                    continue
                return SubmitResult(
                    success=False,
                    status_code=response.status_code,
                    message=message,
                )
            except requests.RequestException as exc:
                if attempt >= self.max_retries:
                    return SubmitResult(success=False, message=str(exc))
                time.sleep(self.retry_backoff_seconds * attempt)

        return SubmitResult(success=False, message="Unknown request failure")

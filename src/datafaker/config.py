from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


DEFAULT_ENDPOINTS = {
    "product": "https://console-api-test.deepclick.com/api/console/ad/app/create",
    "backflow_landing_page": "/api/v1/backflow/landing-pages",
    "backflow_link": "/api/v1/backflow/links",
    "old_customer_landing_page": "/api/v1/old-customer/landing-pages",
}

DEFAULT_ENDPOINT_LABELS = {
    "product": "新建APK产品接口",
    "backflow_landing_page": "回流落地页接口",
    "backflow_link": "回流链接接口",
    "old_customer_landing_page": "老客落地页接口",
}


@dataclass
class AppConfig:
    base_url: str = "http://localhost:8080"
    token: str = ""
    timeout_seconds: float = 10.0
    max_retries: int = 3
    retry_backoff_seconds: float = 0.5
    connection_pool_size: int = 100
    headers: dict[str, str] = field(default_factory=dict)
    default_workers: int = 10
    max_workers: int = 100
    endpoints: dict[str, str] = field(default_factory=lambda: dict(DEFAULT_ENDPOINTS))
    endpoint_labels: dict[str, str] = field(default_factory=lambda: dict(DEFAULT_ENDPOINT_LABELS))

    @classmethod
    def load(cls, config_path: str | Path | None = None) -> "AppConfig":
        config = cls()
        if config_path:
            config.apply_yaml(config_path)
        config.apply_env()
        return config

    def apply_yaml(self, config_path: str | Path) -> None:
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with path.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}

        self._apply_mapping(raw)

    def apply_env(self) -> None:
        self.base_url = os.getenv("DATAFAKER_BASE_URL", self.base_url)
        self.token = os.getenv("DATAFAKER_TOKEN", self.token)
        self.timeout_seconds = float(os.getenv("DATAFAKER_TIMEOUT_SECONDS", self.timeout_seconds))
        self.max_retries = int(os.getenv("DATAFAKER_MAX_RETRIES", self.max_retries))
        self.retry_backoff_seconds = float(
            os.getenv("DATAFAKER_RETRY_BACKOFF_SECONDS", self.retry_backoff_seconds)
        )
        self.connection_pool_size = int(
            os.getenv("DATAFAKER_CONNECTION_POOL_SIZE", self.connection_pool_size)
        )
        self.default_workers = int(os.getenv("DATAFAKER_DEFAULT_WORKERS", self.default_workers))
        self.max_workers = int(os.getenv("DATAFAKER_MAX_WORKERS", self.max_workers))

    def apply_overrides(self, base_url: str | None = None, token: str | None = None) -> None:
        if base_url:
            self.base_url = base_url
        if token is not None:
            self.token = token

    def endpoint_for(self, key: str) -> str:
        endpoint = self.endpoints.get(key)
        if not endpoint:
            raise KeyError(f"No endpoint configured for data_type={key}")
        return endpoint

    def endpoint_label_for(self, key: str) -> str:
        return self.endpoint_labels.get(key, key)

    def _apply_mapping(self, raw: dict[str, Any]) -> None:
        api = raw.get("api", {})
        threading = raw.get("threading", {})

        self.base_url = api.get("base_url", self.base_url)
        self.token = api.get("token", self.token)
        self.timeout_seconds = float(api.get("timeout_seconds", self.timeout_seconds))
        self.max_retries = int(api.get("max_retries", self.max_retries))
        self.retry_backoff_seconds = float(
            api.get("retry_backoff_seconds", self.retry_backoff_seconds)
        )
        self.connection_pool_size = int(
            api.get("connection_pool_size", self.connection_pool_size)
        )
        headers = api.get("headers", {})
        if headers:
            self.headers = {str(k): str(v) for k, v in headers.items()}

        self.default_workers = int(threading.get("default_workers", self.default_workers))
        self.max_workers = int(threading.get("max_workers", self.max_workers))

        endpoints = raw.get("endpoints", {})
        if endpoints:
            merged = dict(self.endpoints)
            merged.update({str(k): str(v) for k, v in endpoints.items()})
            self.endpoints = merged

        endpoint_labels = raw.get("endpoint_labels", {})
        if endpoint_labels:
            merged_labels = dict(self.endpoint_labels)
            merged_labels.update({str(k): str(v) for k, v in endpoint_labels.items()})
            self.endpoint_labels = merged_labels

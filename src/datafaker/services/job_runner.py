from __future__ import annotations

from datafaker.api.client import APIClient
from datafaker.config import AppConfig
from datafaker.generators.registry import GeneratorRegistry, build_default_registry
from datafaker.models import BatchResult, GenerationTask, TaskResult
from datafaker.services.worker_pool import WorkerPool


class JobRunner:
    def __init__(self, config: AppConfig, registry: GeneratorRegistry | None = None) -> None:
        self.config = config
        self.registry = registry or build_default_registry()
        self.client = APIClient(
            base_url=config.base_url,
            token=config.token,
            default_headers=config.headers,
            timeout_seconds=config.timeout_seconds,
            max_retries=config.max_retries,
            retry_backoff_seconds=config.retry_backoff_seconds,
            connection_pool_size=config.connection_pool_size,
        )
        self.worker_pool = WorkerPool(
            default_workers=config.default_workers,
            max_workers=config.max_workers,
        )

    def close(self) -> None:
        self.client.close()

    def run_task(self, task: GenerationTask) -> TaskResult:
        generator = self.registry.create(task.data_type)
        endpoint = self.config.endpoint_for(task.data_type.value)
        return self.worker_pool.run(
            task=task,
            generator=generator,
            submitter=lambda payload: self.client.create(endpoint=endpoint, payload=payload),
        )

    def run_batch(self, tasks: list[GenerationTask]) -> BatchResult:
        results: list[TaskResult] = []
        for task in tasks:
            results.append(self.run_task(task))
        return BatchResult(results=results)

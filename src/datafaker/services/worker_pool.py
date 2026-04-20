from __future__ import annotations

import time
from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor, as_completed

from datafaker.generators.base import BaseGenerator
from datafaker.models import GenerationTask, SubmitResult, TaskResult


class WorkerPool:
    def __init__(self, default_workers: int, max_workers: int) -> None:
        self.default_workers = default_workers
        self.max_workers = max_workers

    def run(
        self,
        task: GenerationTask,
        generator: BaseGenerator,
        submitter: Callable[[dict], SubmitResult],
    ) -> TaskResult:
        worker_count = min(task.workers or self.default_workers, self.max_workers)
        start = time.perf_counter()

        attempted = task.count
        succeeded = 0
        failed = 0
        errors: list[str] = []

        def one(index: int) -> SubmitResult:
            payload = generator.generate(index)
            return submitter(payload)

        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            futures: dict[Future[SubmitResult], int] = {}
            begin = task.start_index
            end = begin + task.count
            for index in range(begin, end):
                futures[executor.submit(one, index)] = index

            for future in as_completed(futures):
                index = futures[future]
                try:
                    result = future.result()
                except Exception as exc:  # noqa: BLE001
                    failed += 1
                    if len(errors) < 20:
                        errors.append(f"index={index} exception={exc}")
                    continue

                if result.success:
                    succeeded += 1
                else:
                    failed += 1
                    if len(errors) < 20:
                        details = result.message or "unknown failure"
                        errors.append(f"index={index} status={result.status_code} message={details}")

        duration_seconds = time.perf_counter() - start
        return TaskResult(
            task=task,
            attempted=attempted,
            succeeded=succeeded,
            failed=failed,
            duration_seconds=duration_seconds,
            errors=errors,
        )

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DataType(str, Enum):
    PRODUCT = "product"
    BACKFLOW_LANDING_PAGE = "backflow_landing_page"
    BACKFLOW_LINK = "backflow_link"
    OLD_CUSTOMER_LANDING_PAGE = "old_customer_landing_page"


@dataclass
class GenerationTask:
    data_type: DataType
    count: int
    workers: int | None = None
    start_index: int = 1

    def __post_init__(self) -> None:
        if self.count <= 0:
            raise ValueError("count must be greater than 0")
        if self.workers is not None and self.workers <= 0:
            raise ValueError("workers must be greater than 0")
        if self.start_index <= 0:
            raise ValueError("start_index must be greater than 0")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GenerationTask":
        raw_type = data.get("data_type")
        if not raw_type:
            raise ValueError("task.data_type is required")

        return cls(
            data_type=DataType(raw_type),
            count=int(data.get("count", 0)),
            workers=int(data["workers"]) if data.get("workers") is not None else None,
            start_index=int(data.get("start_index", 1)),
        )


@dataclass
class SubmitResult:
    success: bool
    status_code: int | None = None
    message: str | None = None


@dataclass
class TaskResult:
    task: GenerationTask
    attempted: int
    succeeded: int
    failed: int
    duration_seconds: float
    errors: list[str] = field(default_factory=list)


@dataclass
class BatchResult:
    results: list[TaskResult]

    @property
    def attempted(self) -> int:
        return sum(result.attempted for result in self.results)

    @property
    def succeeded(self) -> int:
        return sum(result.succeeded for result in self.results)

    @property
    def failed(self) -> int:
        return sum(result.failed for result in self.results)

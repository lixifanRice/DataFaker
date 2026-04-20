from datafaker.generators.product import ProductGenerator
from datafaker.models import DataType, GenerationTask, SubmitResult
from datafaker.services.worker_pool import WorkerPool


def test_worker_pool_run_success() -> None:
    pool = WorkerPool(default_workers=4, max_workers=8)
    task = GenerationTask(data_type=DataType.PRODUCT, count=10, workers=3)

    def submitter(_payload: dict) -> SubmitResult:
        return SubmitResult(success=True, status_code=201)

    result = pool.run(task=task, generator=ProductGenerator(), submitter=submitter)
    assert result.attempted == 10
    assert result.succeeded == 10
    assert result.failed == 0

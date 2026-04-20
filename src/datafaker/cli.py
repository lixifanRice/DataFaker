from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from datafaker.config import AppConfig
from datafaker.models import BatchResult, DataType, GenerationTask, TaskResult
from datafaker.services.job_runner import JobRunner
from datafaker.utils.logging import setup_logging


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="DataFaker: API-based multi-threaded data generator")
    add_common_options(parser)

    subparsers = parser.add_subparsers(dest="command", required=True)

    single = subparsers.add_parser("single", help="Run one generation task")
    add_common_options(single)
    single.add_argument("--data-type", required=True, choices=[d.value for d in DataType])
    single.add_argument("--count", required=True, type=int)
    single.add_argument("--workers", type=int)
    single.add_argument("--start-index", type=int, default=1)

    batch = subparsers.add_parser("batch", help="Run task list from YAML")
    add_common_options(batch)
    batch.add_argument("--task-file", required=True, help="Task yaml path")

    return parser


def add_common_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", default="config/default.yaml", help="Path to YAML config")
    parser.add_argument("--base-url", help="Override API base url")
    parser.add_argument("--token", help="Override API token")
    parser.add_argument("--log-level", default="INFO", help="Logging level")


def load_batch_tasks(path: str | Path) -> list[GenerationTask]:
    with Path(path).open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    raw_tasks = data.get("tasks", [])
    if not isinstance(raw_tasks, list):
        raise ValueError("tasks must be a list")

    return [GenerationTask.from_dict(item) for item in raw_tasks]


def print_task_result(result: TaskResult, endpoint: str, interface_label: str) -> None:
    ok = result.failed == 0
    conclusion = (
        f"{interface_label} 执行成功"
        if ok
        else f"{interface_label} 执行失败，成功 {result.succeeded} / 失败 {result.failed}"
    )
    output = {
        "interface_label": interface_label,
        "endpoint": endpoint,
        "data_type": result.task.data_type.value,
        "count": result.task.count,
        "attempted": result.attempted,
        "succeeded": result.succeeded,
        "failed": result.failed,
        "duration_seconds": round(result.duration_seconds, 3),
        "sample_errors": result.errors,
        "conclusion": conclusion,
    }
    print(json.dumps(output, ensure_ascii=True, indent=2))


def print_batch_result(result: BatchResult, config: AppConfig) -> None:
    batch_ok = result.failed == 0
    summary_conclusion = (
        "批量任务全部执行成功"
        if batch_ok
        else f"批量任务执行完成，成功 {result.succeeded} / 失败 {result.failed}"
    )
    output = {
        "summary": {
            "attempted": result.attempted,
            "succeeded": result.succeeded,
            "failed": result.failed,
            "conclusion": summary_conclusion,
        },
        "tasks": [
            {
                "interface_label": config.endpoint_label_for(item.task.data_type.value),
                "endpoint": config.endpoint_for(item.task.data_type.value),
                "data_type": item.task.data_type.value,
                "count": item.task.count,
                "attempted": item.attempted,
                "succeeded": item.succeeded,
                "failed": item.failed,
                "duration_seconds": round(item.duration_seconds, 3),
                "sample_errors": item.errors,
                "conclusion": (
                    f"{config.endpoint_label_for(item.task.data_type.value)} 执行成功"
                    if item.failed == 0
                    else (
                        f"{config.endpoint_label_for(item.task.data_type.value)} 执行失败，"
                        f"成功 {item.succeeded} / 失败 {item.failed}"
                    )
                ),
            }
            for item in result.results
        ],
    }
    print(json.dumps(output, ensure_ascii=True, indent=2))


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    setup_logging(args.log_level)

    config = AppConfig.load(args.config)
    config.apply_overrides(base_url=args.base_url, token=args.token)

    runner = JobRunner(config)
    try:
        if args.command == "single":
            task = GenerationTask(
                data_type=DataType(args.data_type),
                count=args.count,
                workers=args.workers,
                start_index=args.start_index,
            )
            result = runner.run_task(task)
            endpoint = config.endpoint_for(task.data_type.value)
            interface_label = config.endpoint_label_for(task.data_type.value)
            print_task_result(result, endpoint=endpoint, interface_label=interface_label)
            return 0 if result.failed == 0 else 2

        if args.command == "batch":
            tasks = load_batch_tasks(args.task_file)
            result = runner.run_batch(tasks)
            print_batch_result(result, config=config)
            return 0 if result.failed == 0 else 2

        parser.error(f"Unknown command: {args.command}")
        return 1
    finally:
        runner.close()

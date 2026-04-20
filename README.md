# DataFaker

A multi-threaded data generation framework that calls API endpoints to create test/mock data.

## Supported Data Types

- `product`
- `backflow_landing_page`
- `backflow_link`
- `old_customer_landing_page`

## Project Structure

```text
DataFaker/
├── config/
│   ├── default.yaml
│   └── tasks.example.yaml
├── src/datafaker/
│   ├── api/
│   │   └── client.py
│   ├── generators/
│   │   ├── base.py
│   │   ├── product.py
│   │   ├── backflow_landing_page.py
│   │   ├── backflow_link.py
│   │   ├── old_customer_landing_page.py
│   │   └── registry.py
│   ├── services/
│   │   ├── worker_pool.py
│   │   └── job_runner.py
│   ├── utils/
│   │   ├── logging.py
│   │   └── random_data.py
│   ├── cli.py
│   ├── config.py
│   └── models.py
└── pyproject.toml
```

## Quick Start

1. Install dependencies:

```bash
pip install -e .
```

2. Edit `config/default.yaml` for your API host and endpoints.

3. Run a single task:

```bash
datafaker single \
  --data-type product \
  --count 1000 \
  --workers 20 \
  --config config/default.yaml
```

4. Run batch tasks from file:

```bash
datafaker batch --task-file config/tasks.example.yaml --config config/default.yaml
```

## Env Overrides

You can override config via environment variables:

- `DATAFAKER_BASE_URL`
- `DATAFAKER_TOKEN`
- `DATAFAKER_TIMEOUT_SECONDS`
- `DATAFAKER_MAX_RETRIES`
- `DATAFAKER_RETRY_BACKOFF_SECONDS`
- `DATAFAKER_CONNECTION_POOL_SIZE`
- `DATAFAKER_DEFAULT_WORKERS`
- `DATAFAKER_MAX_WORKERS`

## Notes

- This repository is a framework scaffold, not a complete business implementation.
- Replace payload fields in each generator based on your real API contract.

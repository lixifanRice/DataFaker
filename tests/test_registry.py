from datafaker.generators.registry import build_default_registry
from datafaker.models import DataType


def test_default_registry_can_create_all_generators() -> None:
    registry = build_default_registry()
    for data_type in DataType:
        generator = registry.create(data_type)
        payload = generator.generate(1)
        assert isinstance(payload, dict)
        assert payload

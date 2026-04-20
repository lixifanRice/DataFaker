from __future__ import annotations

from collections.abc import Callable

from datafaker.generators.backflow_landing_page import BackflowLandingPageGenerator
from datafaker.generators.backflow_link import BackflowLinkGenerator
from datafaker.generators.base import BaseGenerator
from datafaker.generators.old_customer_landing_page import OldCustomerLandingPageGenerator
from datafaker.generators.product import ProductGenerator
from datafaker.models import DataType


class GeneratorRegistry:
    def __init__(self) -> None:
        self._factories: dict[DataType, Callable[[], BaseGenerator]] = {}

    def register(self, data_type: DataType, factory: Callable[[], BaseGenerator]) -> None:
        self._factories[data_type] = factory

    def create(self, data_type: DataType) -> BaseGenerator:
        factory = self._factories.get(data_type)
        if not factory:
            raise KeyError(f"No generator registered for data_type={data_type.value}")
        return factory()


def build_default_registry() -> GeneratorRegistry:
    registry = GeneratorRegistry()
    registry.register(DataType.PRODUCT, ProductGenerator)
    registry.register(DataType.BACKFLOW_LANDING_PAGE, BackflowLandingPageGenerator)
    registry.register(DataType.BACKFLOW_LINK, BackflowLinkGenerator)
    registry.register(DataType.OLD_CUSTOMER_LANDING_PAGE, OldCustomerLandingPageGenerator)
    return registry

from typing import Any

from .backwards_compatibility import warn_deprecation_pending


class Component(object):
    """Defines a Component in the PreHEAT sense"""

    def __init__(self, component_data: dict[str, Any]):
        # Identifier of the component
        self.cid = component_data.pop("cid", None)
        self.id = component_data.pop("id", None)

        # Name of the component
        self.name = component_data.pop("name", str(self.id))

        # Tag (e.g. BACNET/source name)
        self.tag = component_data.pop("tag", None)

        # Data for the component (PreHEAT_API.Data)
        self.data = None

        # Factor to divide by to obtain a 'standard' unit
        self.std_unit_divisor = component_data.pop("stdUnitDivisor", 1)

        # Standard unit for this type of component
        self.std_unit = component_data.pop("stdUnit", "")

    @property
    def std_unit_devisor(self):
        """DEPRECATED: use std_unit_divisor instead"""
        warn_deprecation_pending("Deprecated: use std_unit_divisor instead")
        return self.std_unit_divisor

    def __repr__(self) -> str:
        """String representation"""
        return f"{type(self).__name__}({self.name}, {self.tag})"

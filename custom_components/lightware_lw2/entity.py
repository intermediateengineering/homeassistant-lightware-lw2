"""Base class for Lightware entities."""

from dataclasses import dataclass
from typing import TypeVar

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import LightwareUpdateCoordinator

T = TypeVar("T", bound=EntityDescription)


@dataclass
class LightwareEntity[T](CoordinatorEntity[LightwareUpdateCoordinator]):
    """Common elements for all entities."""

    _attr_has_entity_name = True
    entity_description: T

    def __init__(
        self, coordinator: LightwareUpdateCoordinator, entity_description: T
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._lw2 = coordinator.lw2
        self._attr_unique_id = f"{self._lw2.serial}_{entity_description.key}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._lw2.serial)},
            manufacturer="Lightware",
            model=self._lw2.product_type,
            suggested_area="Serverroom",
            sw_version=self._lw2.server_version,
            serial_number=self._lw2.serial,
            hw_version=self._lw2.firmware,
        )

    @property
    def available(self) -> bool:
        """Returns whether entity is available."""
        return self.coordinator.available

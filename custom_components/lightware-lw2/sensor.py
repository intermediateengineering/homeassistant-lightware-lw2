"""Video Matrix Mapping Sensor"""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import LightwareConfigEntry
from .const import DOMAIN
from .coordinator import LightwareUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: LightwareConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    coordinator = entry.runtime_data.coordinator
    sensors = [
        MappingSensor(coordinator, entry.entry_id, output)
        for output in coordinator.lw2.outputs
    ]

    async_add_entities(sensors, update_before_add=True)


class MappingSensor(CoordinatorEntity[LightwareUpdateCoordinator], SensorEntity):
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_icon = "mdi:connection"
    _attr_state_class = None

    def __init__(self, coordinator, entry_id, output):
        super().__init__(coordinator)
        self._entry_id = entry_id
        self.output = output
        self._attr_options = [input.idx for input in coordinator.lw2.inputs]
        self._attr_unique_id = (
            f"lightware_mapping{output.idx:02}_{coordinator.lw2.serial}"
        )
        self._attr_name = f"Mapping Output {output.idx:02}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name="Lightware Video Matrix",
            manufacturer="Lightware",
            model=coordinator.lw2.product_type,
            sw_version=coordinator.lw2.firmware,
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        input = self.coordinator.lw2.mapping[self.output]
        self._attr_native_value = getattr(input, "idx", None)
        self.input = input
        self.async_write_ha_state()

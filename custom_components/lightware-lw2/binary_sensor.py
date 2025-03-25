"""Video Matrix Port Sensor"""

import logging
from datetime import timedelta

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import (
    AddEntitiesCallback,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from lw2.lightware import Port, Type

from . import LightwareConfigEntry
from .const import DOMAIN
from .coordinator import LightwareUpdateCoordinator

# the interval in which the update function will be called
SCAN_INTERVAL = timedelta(seconds=10)


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: LightwareConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the port binary sensor entity from a config entry."""

    coordinator = entry.runtime_data.coordinator
    inputs = [
        PortStatusSensor(i, coordinator, entry.entry_id) for i in coordinator.lw2.inputs
    ]
    outputs = [
        PortStatusSensor(o, coordinator, entry.entry_id)
        for o in coordinator.lw2.outputs
    ]
    async_add_entities(inputs + outputs, update_before_add=True)


class PortStatusSensor(
    CoordinatorEntity[LightwareUpdateCoordinator], BinarySensorEntity
):
    """The port status of the video matrix if a cable is connected"""

    _attr_icon = "mdi:hdmi-port"
    _attr_is_on = False

    def __init__(
        self,
        port: Port,
        coordinator: LightwareUpdateCoordinator,
        entry_id: str,
    ):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._attr_unique_id = (
            f"lightware_{port.type.name}{port.idx:02}_{coordinator.lw2.serial}"
        )
        self._attr_extra_state_attributes = {"type": port.type, "index": port.idx}

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name="Lightware Video Matrix",
            manufacturer="Lightware",
            model=coordinator.lw2.product_type,
            sw_version=coordinator.lw2.firmware,
        )

        _LOGGER.info("Added %s", self._attr_unique_id)

        self._attr_name = f"{port.type.name} {port.idx:02}"
        self.port = port

    @callback
    def _handle_coordinator_update(self) -> None:
        """Fetch new data for the sensor from the update coordinator."""
        match self.port.type:
            case Type.INPUT:
                port: Port = next(
                    input
                    for input in self.coordinator.data.inputs
                    if input.idx == self.port.idx
                )
            case Type.OUTPUT:
                port: Port = next(
                    output
                    for output in self.coordinator.data.outputs
                    if output.idx == self.port.idx
                )
        self.port = port
        self._attr_is_on = port.connected
        super()._handle_coordinator_update()

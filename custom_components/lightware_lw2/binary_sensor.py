"""Video Matrix Port Sensor"""

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from lw2.lightware import Port, Type

from .coordinator import LightwareConfigEntry
from .entity import LightwareEntity

# Coordinator is used to centralize the data updates
PARALLEL_UPDATES = 0


@dataclass(kw_only=True, frozen=True)
class PortSensorEntityDescription(BinarySensorEntityDescription):
    """Description for Lightware Mapping sensor entities."""

    port: Port


async def async_setup_entry(
    hass: HomeAssistant,
    entry: LightwareConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the port binary sensor entity from a config entry."""

    coordinator = entry.runtime_data
    entity_descriptions = [
        PortSensorEntityDescription(
            key=f"{port.type.name}_{port.idx:02}",
            name=f"{port.type.name.capitalize()} {port.idx:02}",
            port=port,
            icon="mdi:hdmi-port",
        )
        for port in coordinator.lw2.inputs + coordinator.lw2.outputs
    ]

    sensors = [
        PortStatusSensor(coordinator, entity_description)
        for entity_description in entity_descriptions
    ]
    async_add_entities(sensors, update_before_add=True)


class PortStatusSensor(
    LightwareEntity[PortSensorEntityDescription], BinarySensorEntity
):
    """The port status of the video matrix if a cable is connected"""

    @callback
    def _handle_coordinator_update(self) -> None:
        """Fetch new data for the sensor from the update coordinator."""
        match self.entity_description.port.type:
            case Type.INPUT:
                port: Port = next(
                    input
                    for input in self.coordinator.lw2.inputs
                    if input.idx == self.entity_description.port.idx
                )
            case Type.OUTPUT:
                port: Port = next(
                    output
                    for output in self.coordinator.lw2.outputs
                    if output.idx == self.entity_description.port.idx
                )
        self._attr_is_on = port.connected
        super()._handle_coordinator_update()

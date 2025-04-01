"""Video Matrix Mapping Sensor"""

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from lw2.lightware import Output

from .coordinator import LightwareConfigEntry
from .entity import LightwareEntity

# Coordinator is used to centralize the data updates
PARALLEL_UPDATES = 0


@dataclass(kw_only=True, frozen=True)
class MappingSensorEntityDescription(SensorEntityDescription):
    """Description for Lightware Mapping sensor entities."""

    output: Output


async def async_setup_entry(
    hass: HomeAssistant,
    entry: LightwareConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    coordinator = entry.runtime_data
    options = [str(input.idx) for input in coordinator.lw2.inputs]

    entity_descriptions = [
        MappingSensorEntityDescription(
            key=f"mapping_{output.idx:02}",
            name=f"Connection Output {output.idx:02}",
            device_class=SensorDeviceClass.ENUM,
            options=options,
            output=output,
            icon="mdi:connection",
            state_class=None,
        )
        for output in coordinator.lw2.outputs
    ]

    sensors = [
        MappingSensor(coordinator, entity_description)
        for entity_description in entity_descriptions
    ]

    async_add_entities(sensors, update_before_add=True)


class MappingSensor(LightwareEntity[MappingSensorEntityDescription], SensorEntity):
    """The mapping of the input port index to the corresponding output port index"""

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        input = self.coordinator.lw2.mapping[self.entity_description.output]
        self._attr_native_value = str(getattr(input, "idx", None))
        self.async_write_ha_state()
        super()._handle_coordinator_update()

"""My Sensor."""

from datetime import timedelta
import logging

import voluptuous as vol

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant, ServiceCall, callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import (
    AddEntitiesCallback,
    async_get_current_platform,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MySensorUpdateCoordinator

# the interval in which the update function will be called
SCAN_INTERVAL = timedelta(seconds=10)

SERVICE_OFFSET_TEMP_SCHEMA = {
    vol.Required("by"): vol.Coerce(float),
}

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the light sensor entity from a config entry."""

    platform = async_get_current_platform()
    platform.async_register_entity_service(
        name="offset_temperature",  # key in the services.yaml file
        func=async_handle_offset_temp,
        schema=cv.make_entity_service_schema(SERVICE_OFFSET_TEMP_SCHEMA),
    )

    coordinator = entry.runtime_data
    # Create and add our single sensor entity
    sensor = MySensor(coordinator, entry.entry_id)
    async_add_entities([sensor], update_before_add=True)


class MySensor(CoordinatorEntity[MySensorUpdateCoordinator], SensorEntity):
    """Representation of a Temperature Sensor."""

    _attr_name = "My Sensor"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:thermometer"
    _attr_available = True
    _attr_native_value = None

    def __init__(
        self,
        coordinator: MySensorUpdateCoordinator,
        entry_id: str,
    ):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._offset: float = 0
        self._attr_unique_id = f"my_sensor_{coordinator.ip}_{coordinator.port}"
        self._attr_extra_state_attributes = {
            "ip": coordinator.ip,
            "port": coordinator.port,
        }

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name="Dummy Temperature Sensor",
            manufacturer="Dummy Inc.",
            model="Test001",
        )

        self._attr_native_value = coordinator.data.temp
        self._attr_available = coordinator.data.temp is not None

    def offset(self, offset=0):
        """Offset the temperature readings."""
        self._offset = offset

    # Device Info
    # Information about the devices that is partially visible in the UI.
    # The most critical thing here is to give this entity a name so it is displayed
    # as a "device" in the HA UI. This name is used on the Devices overview table,
    # and the initial screen when the device is added (rather than the entity name
    # property below). You can then associate other Entities (eg: a battery
    # sensor) with this device, so it shows more like a unified element in the UI.
    # For example, an associated battery sensor will be displayed in the right most
    # column in the Configuration > Devices view for a device.
    # To associate an entity with this device, the device_info must also return an
    # identical "identifiers" attribute, but not return a name attribute.
    # See the sensors.py file for the corresponding example setup.
    # Additional meta data can also be returned here, including sw_version (displayed
    # as Firmware), model and manufacturer (displayed as <model> by <manufacturer>)
    # shown on the device info screen. The Manufacturer and model also have their
    # respective columns on the Devices overview table. Note: Many of these must be
    # set when the device is first added, and they are not always automatically
    # refreshed by HA from it's internal cache.
    # For more information see:
    # https://developers.home-assistant.io/docs/device_registry_index/#device-properties
    # This property is important to let HA know if this entity is online or not.
    # If an entity is offline (return False), the UI will refelect this.

    @callback
    def _handle_coordinator_update(self) -> None:
        """Fetch new data for the sensor from the update coordinator."""
        temp = self.coordinator.data.temp
        self._attr_native_value = temp + self._offset
        super()._handle_coordinator_update()


async def async_handle_offset_temp(entity: MySensor, call: ServiceCall) -> None:
    """Service Call handler to offset the temperature to the given value."""

    by = call.data.get("by", 0)
    _LOGGER.info("Offset Temperature by %s for %s", by, entity.unique_id)
    # Update the sensor's state attribute.
    entity.offset(by)
    # Notify Home Assistant that the entity's state has changed.
    entity.async_write_ha_state()

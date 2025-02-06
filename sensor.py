"""My Sensor."""

from datetime import timedelta
from decimal import Decimal
from random import randint

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

# the interval in which the update function will be called
SCAN_INTERVAL = timedelta(minutes=1)


async def async_setup_entry(
    _hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the light sensor entity from a config entry."""
    ip_address = entry.data["ip_address"]
    port = entry.data["port"]

    # Create and add our single sensor entity
    async_add_entities(
        [MySensor(entry.entry_id, ip_address, port)], update_before_add=True
    )


class MySensor(SensorEntity):
    """Representation of a Temperature Sensor."""

    _attr_name = "My Sensor"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:thermometer"
    _attr_available = True

    def __init__(self, entry_id: str, ip_address: str, port: int):
        """Initialize the sensor with an IP and port."""
        self._entry_id = entry_id
        self._ip = ip_address
        self._port = port
        self._attr_unique_id = f"my_sensor_{self._ip}_{self._port}"
        self._state: int | None = None
        self._attr_extra_state_attributes = {"ip": self._ip, "port": self._port}

    @property
    def native_value(self):
        """Native value."""
        return self._state

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
    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name="Dummy Temperature Sensor",
            manufacturer="Dummy Inc.",
            model="Test001",
        )

    # This property is important to let HA know if this entity is online or not.
    # If an entity is offline (return False), the UI will refelect this.
    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return self.state is not None

    async def async_update(self):
        """Fetch new data for the sensor (dummy data here)."""
        # In a real implementation, you would communicate with your device at
        # the configured IP address and port to get the light level.
        # For now, let's just simulate a random value.
        self._state = randint(-10, 40)

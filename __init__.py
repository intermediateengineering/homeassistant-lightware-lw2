"""My Sensor."""

import logging

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, PLATFORMS
from .coordinator import MySensorUpdateCoordinator

# This will be called when we write something like this in `configuration.yaml`
#
# my_sensor:
#   - ip_address: localhost
#     port: 123
#   - ip_address: localhost
#     port: 456

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the integration from YAML if configured."""
    if DOMAIN in config:
        # Initiate the config flow to import the YAML config
        for device_config in config[DOMAIN]:
            hass.async_create_task(
                hass.config_entries.flow.async_init(
                    DOMAIN,
                    context={"source": SOURCE_IMPORT},
                    data=device_config,
                )
            )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration from a config entry."""

    # Do global setup
    ip = entry.data["ip_address"]
    port = entry.data["port"]
    coordinator = MySensorUpdateCoordinator(hass, ip, port)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    entry.runtime_data = coordinator
    # Forward the setup to your platform(s)
    # In this case it will forward it to sensor.py:async_setup_entry because PLATFORMS == ["sensor"]
    # See https://developers.home-assistant.io/docs/core/entity for available entities
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the sensor config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

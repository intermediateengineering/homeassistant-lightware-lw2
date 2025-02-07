"""My Sensor."""

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, PLATFORMS

# This will be called when we write something like this in `configuration.yaml`
#
# my_sensor:
#   - ip_address: localhost
#     port: 123
#   - ip_address: localhost
#     port: 456


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
    #
    # Forward the setup to your platform(s)
    # In this case it will forward it to sensor.py:async_setup_entry because PLATFORMS == ["sensor"]
    # See https://developers.home-assistant.io/docs/core/entity for available entities
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

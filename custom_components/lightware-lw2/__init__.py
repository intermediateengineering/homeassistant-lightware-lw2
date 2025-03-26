"""My Sensor."""

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .coordinator import LightwareUpdateCoordinator

type LightwareConfigEntry = ConfigEntry[LightwareData]


@dataclass
class LightwareData:
    coordinator: LightwareUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration from a config entry."""

    # Do global setup
    ip = entry.data["ip_address"]
    port = entry.data["port"]
    coordinator = LightwareUpdateCoordinator(hass, ip, port)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    entry.runtime_data = LightwareData(coordinator)
    # Forward the setup to your platform(s)
    # In this case it will forward it to sensor.py:async_setup_entry because PLATFORMS == ["sensor"]
    # See https://developers.home-assistant.io/docs/core/entity for available entities
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the sensor config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

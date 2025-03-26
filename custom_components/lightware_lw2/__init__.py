"""Lightware LW2"""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from homeassistant.const import CONF_HOST, CONF_PORT

from .services import setup_services
from .const import PLATFORMS
from .coordinator import LightwareUpdateCoordinator


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Lightware."""

    setup_services(hass)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration from a config entry."""

    # Do global setup
    ip = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    coordinator = LightwareUpdateCoordinator(hass, ip, port)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    # Forward the setup to your platform(s)
    # In this case it will forward it to sensor.py:async_setup_entry because PLATFORMS == ["sensor"]
    # See https://developers.home-assistant.io/docs/core/entity for available entities
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the sensor config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

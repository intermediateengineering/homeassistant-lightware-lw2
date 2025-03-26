from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from lw2.lightware import LightwareLW2

_LOGGER = logging.getLogger(__name__)

type LightwareConfigEntry = ConfigEntry[LightwareUpdateCoordinator]


class LightwareUpdateCoordinator(DataUpdateCoordinator[None]):
    """Coordinator to fetch all relevant data from my sensor."""

    def __init__(self, hass: HomeAssistant, ip: str, port: int):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=self.__class__.__name__,
            update_interval=timedelta(seconds=10),  # Adjust as needed
        )
        self._lw2 = LightwareLW2(ip, port)

    @property
    def lw2(self) -> LightwareLW2:
        return self._lw2

    async def _async_update_data(self) -> None:
        """Fetch the latest values status from the video matrix."""

        try:
            await self.lw2.update()
        except Exception as e:
            _LOGGER.error(e)

        return

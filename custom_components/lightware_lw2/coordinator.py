from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from lw2.commands import QueryConnections, QueryInputPortStatus, QueryOutputPortStatus
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

    @property
    def available(self) -> bool:
        return self._lw2.device_data_available and self.last_update_success

    async def _async_setup(self):
        """Set up the coordinator

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        try:
            await self._lw2.update()
        except Exception:
            raise UpdateFailed(
                f"Error getting device data of Lightware device {self.lw2.host}:{self.lw2.port}"
            )

    async def _async_update_data(self) -> None:
        """Fetch the latest values status from the video matrix."""

        try:
            await self.lw2.send_batch_commands(
                [QueryConnections(), QueryInputPortStatus(), QueryOutputPortStatus()]
            )
        except Exception:
            raise UpdateFailed(
                f"Error updating Lightware device {self.lw2.host}:{self.lw2.port}"
            )

        return

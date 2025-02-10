from dataclasses import dataclass
from datetime import timedelta
import logging
import random

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass
class MySensorData:
    temp: float


class MySensorUpdateCoordinator(DataUpdateCoordinator[MySensorData]):
    """Coordinator to fetch all relevant data from my sensor."""

    def __init__(self, hass: HomeAssistant, ip: str, port: int):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=self.__class__.__name__,
            update_interval=timedelta(seconds=10),  # Adjust as needed
        )
        self.ip = ip
        self.port = port

    async def _async_update_data(self):
        """Fetch the latest values status from the sensor."""

        temp = random.choice([12.3, 23.4, 34.5])
        return MySensorData(temp=temp)

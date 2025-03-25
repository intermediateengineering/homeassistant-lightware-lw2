import logging
from dataclasses import dataclass
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from lw2.lightware import LightwareLW2, Input, Output
from typing import Dict, Optional

_LOGGER = logging.getLogger(__name__)


@dataclass
class LightwareData:
    inputs: list[Input]
    outputs: list[Output]
    mapping: Dict[Output, Optional[Input]]


class LightwareUpdateCoordinator(DataUpdateCoordinator[LightwareData]):
    """Coordinator to fetch all relevant data from my sensor."""

    def __init__(self, hass: HomeAssistant, ip: str, port: int):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=self.__class__.__name__,
            update_interval=timedelta(seconds=10),  # Adjust as needed
        )
        self.lw2 = LightwareLW2(ip, port)

    async def _async_update_data(self):
        """Fetch the latest values status from the video matrix."""

        await self.lw2.update()
        return LightwareData(
            inputs=self.lw2.inputs, outputs=self.lw2.outputs, mapping=self.lw2.mapping
        )

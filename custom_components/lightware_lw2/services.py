from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant.const import CONF_DEVICE_ID
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import device_registry as dr
from lw2.commands import InputToOutput

from .const import CONF_INPUT_IDX, CONF_OUTPUT_IDX, DOMAIN, SERVICE_SET_ROUTING
from .coordinator import LightwareConfigEntry

SET_ROUTING_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_INPUT_IDX): cv.positive_int,
        vol.Required(CONF_OUTPUT_IDX): cv.positive_int,
        vol.Required(CONF_DEVICE_ID): vol.All(cv.ensure_list, [cv.string]),
    }
)

_LOGGER = logging.getLogger(__name__)


def setup_services(hass: HomeAssistant) -> None:
    async def async_handle_set_routing(call: ServiceCall) -> None:
        # Grab the input/output fields
        input_idx = call.data[CONF_INPUT_IDX]
        output_idx = call.data[CONF_OUTPUT_IDX]
        device_ids = call.data[CONF_DEVICE_ID]

        for device_id in device_ids:
            device_registry = dr.async_get(call.hass)
            device = device_registry.async_get(device_id)

            if not device or not device.config_entries:
                raise ValueError(f"Device {device_id} not found in device registry.")

            entry_id = next(iter(device.config_entries))

            config_entry: LightwareConfigEntry | None
            if not (config_entry := call.hass.config_entries.async_get_entry(entry_id)):
                raise ValueError(
                    f"Config entry for id {entry_id} not found in config entries."
                )

            coordinator = config_entry.runtime_data
            await coordinator.lw2.send_command(InputToOutput(input_idx, output_idx))
            await coordinator.async_request_refresh()

    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_ROUTING,
        async_handle_set_routing,
        schema=SET_ROUTING_SCHEMA,
    )

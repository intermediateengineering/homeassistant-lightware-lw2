"""Config Flow."""

import voluptuous as vol

from typing import Any
from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN

SCHEMA = vol.Schema(
    {
        vol.Required("ip_address"): cv.string,
        vol.Required("port", default=80): cv.port,
    }
)


class LightwareConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My Sensor in the UI."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        # If user has submitted the form
        if user_input is not None:
            # Create the config entry
            return self.async_create_entry(title="Lightware LW2", data=user_input)

        return self.async_show_form(step_id="user", data_schema=SCHEMA, errors=errors)

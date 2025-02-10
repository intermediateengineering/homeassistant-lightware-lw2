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


class MySensorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
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
            return self.async_create_entry(title="My Sensor", data=user_input)

        return self.async_show_form(step_id="user", data_schema=SCHEMA, errors=errors)

    async def async_step_import(self, import_data) -> ConfigFlowResult:
        """Handle configuration via YAML import."""
        for entry in self._async_current_entries():
            ip_match = entry.data.get("ip_address") == import_data.get("ip_address")
            port_match = entry.data.get("port") == import_data.get("port")

            if ip_match and port_match:
                return self.async_abort(reason="already_configured")

        return await self.async_step_user(user_input=import_data)

"""Constants."""

import voluptuous as vol

from homeassistant.const import Platform
import homeassistant.helpers.config_validation as cv

DOMAIN = "lightware-lw2"  # has to be the same as parent directory name and match the name in manifest.json
PLATFORMS = [Platform.BINARY_SENSOR]  # delegates to each <PLATFORM>.py


# schema for yaml configuration
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            cv.ensure_list,
            [
                vol.Schema(
                    {
                        vol.Required("ip_address"): cv.string,
                        vol.Required("port"): cv.port,
                    }
                )
            ],
        )
    },
    extra=vol.ALLOW_EXTRA,
)

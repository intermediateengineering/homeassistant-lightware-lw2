"""Constants."""

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import Platform

DOMAIN = "lightware_lw2"  # has to be the same as parent directory name and match the name in manifest.json
PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]  # delegates to each <PLATFORM>.py

CONF_INPUT_IDX = "input_idx"
CONF_OUTPUT_IDX = "output_idx"

SERVICE_SET_ROUTING = "set_routing"

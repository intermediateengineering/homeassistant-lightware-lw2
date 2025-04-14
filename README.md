# Home Assistant Lightware LW2 integration

A [Home Assistant](https://www.home-assistant.io/) integration for the Lightware video switches with the LW2 API

## Features

- Fetches device data
    - Version Numbers
    - Serial
    - Network info
- Shows port status (disconnected/connected)
- Shows routing
- Control Routing

## Installation

### Installation via HACS

1. Add this repository as a custom repository to HACS:

[![Add Repository](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=intermediateengineering&repository=homeassistant-lightware-lw2&category=Integration)

2. Use HACS to install the integration.
3. Restart Home Assistant.
4. Set up the integration using the UI:

[![Add Integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=lightware_lw2)


### Manual Installation

1. Download the integration files from the GitHub repository.
2. Place the integration folder in the custom_components directory of Home Assistant.
3. Restart Home Assistant.
4. Set up the integration using the UI:

[![Add Integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=lightware_lw2)

## Debugging

It is possible to show the info and debug logs for the Pi-hole V6 integration, to do this you need to enable logging in the configuration.yaml, example below:

```
logger:
  default: warning
  logs:
    # Log for Pi-hole V6 integation
    custom_components.lightware_lw2: debug
```

Logs do not remove sensitive information so careful what you share, check what you are about to share and blank identifying information.

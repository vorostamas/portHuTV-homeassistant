"""Constants for porthutv."""
# Base component constants
NAME = "PortHuTv"
DOMAIN = "porthutv"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"

ISSUE_URL = "https://github.com/vorostamas/portHuTV-homeassistant/issues"

# Icons
ICON = "mdi:television-guide"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_TV_CHANNEL = "channel"
CONF_PASSWORD = "password"

# Defaults
DEFAULT_NAME = DOMAIN

# Other
CHANNEL_MAPPING_FILE_PATH = "custom_components/porthutv/channel_mapping.json"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

"""Constants for porthutv."""
# Base component constants
NAME = "PortHuTv"
DOMAIN = "porthutv"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "1.0.6"

ISSUE_URL = "https://github.com/vorostamas/portHuTV-homeassistant/issues"

# Icons
ICON = "mdi:television-guide"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_TV_CHANNEL_ID = "channel_id"
CONF_TV_CHANNEL_NAME = "channel_name"
CONF_TIME_ZONE = "Europe/Budapest"

# Defaults
DEFAULT_NAME = DOMAIN

# Other
CHANNEL_MAPPING_FILE_PATH = "custom_components/porthutv/channel_mapping.json"
BASE_URL = "http://port.hu"
CHANNEL_DATA_URL = (
    "https://port.hu/tvapi?channel_id={}&i_datetime_from={}&i_datetime_to={}"
)


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

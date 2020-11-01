import json

from custom_components.porthutv.const import CHANNEL_MAPPING_FILE_PATH


def validate_channel_id(channel_id):
    """
    Validate the channel ID.
    """
    try:
        with open(CHANNEL_MAPPING_FILE_PATH) as channel_mapping_file:
            channels = json.load(channel_mapping_file)
        if channel_id in channels:
            return True
    except Exception:  # pylint: disable=broad-except
        pass
    return False
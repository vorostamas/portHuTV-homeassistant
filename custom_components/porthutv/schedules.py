from datetime import date
import requests

CHANNEL_DATA_URL = (
    "https://port.hu/tvapi?channel_id={}&i_datetime_from={}&i_datetime_to={}"
)


def get_today_date():
    """
    Get the the for the actual day in YYYY-MM-DD format.
    """
    return date.today().strftime("%Y-%m-%d")


def get_channel_data(channel_id):
    """
    Get the channel information and schedule of a channel for today.
    """
    today = get_today_date()
    url = CHANNEL_DATA_URL.format(channel_id, today, today)
    return requests.get(url).json()


def get_key(channel_data):
    """
    Determine the first key in the datastructure, which is a timestamp.
    """
    return list(channel_data.keys())[0]


def get_channel_name(channel_id):
    """
    Exctract the name of the channel from the channel ID.
    """
    channel_data = get_channel_data(channel_id)  # TODO: fallback to channel id
    key = get_key(channel_data)
    return channel_data[key]["channels"][0]["name"]
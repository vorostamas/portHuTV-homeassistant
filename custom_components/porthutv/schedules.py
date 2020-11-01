from datetime import date
import requests

from custom_components.porthutv.const import BASE_URL, CHANNEL_DATA_URL


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


def exctract_schedule_details(channel_information):
    """
    Extract the details of a channel's schedule.
    """
    key = get_key(channel_information)
    schedule = channel_information[key]["channels"][0]["programs"]

    channel_schedule = []
    for program in schedule:
        title = program["title"]
        start_time = program["start_time"]
        end_time = program["end_time"]
        # start_datetime = parse(program["start_datetime"])
        # end_datetime = parse(program["end_datetime"])
        episode_title = program["episode_title"] or ""
        short_description = program["short_description"]
        film_url = BASE_URL + program["film_url"] if program["film_url"] else ""

        # Create result
        channel_program = {}
        channel_program["title"] = title
        channel_program["start_time"] = start_time
        channel_program["end_time"] = end_time
        channel_program["episode_title"] = episode_title
        channel_program["short_description"] = short_description
        channel_program["film_url"] = film_url

        channel_schedule.append(channel_program)

    return channel_schedule


def get_schedules(channel_id):
    """
    List the programs for the given channel.
    """
    channel_data = get_channel_data(channel_id)
    schedule = exctract_schedule_details(channel_data)

    return schedule
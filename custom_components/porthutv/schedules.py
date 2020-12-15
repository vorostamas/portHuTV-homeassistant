"""Schedule data manipulation functions for porthutv."""
from datetime import datetime
from dateutil.parser import parse
import pytz
import requests

from custom_components.porthutv.const import BASE_URL, CHANNEL_DATA_URL, CONF_TIME_ZONE


def get_today_date():
    """
    Get the the for the actual day in YYYY-MM-DD format.
    """
    today = datetime.now(pytz.timezone(CONF_TIME_ZONE)).strftime("%Y-%m-%d")
    return today


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
    return exctract_schedule_details(channel_data)


def parse_time(time):
    """
    Parse and localize time with timezone.
    """
    return pytz.timezone(CONF_TIME_ZONE).localize(parse(time))


def in_between(now, start, end):
    """
    Determine if now is between an interval considering day overlap.
    """
    if start <= end:
        return start <= now < end
    # over midnight e.g., 23:30-00:15
    return start <= now or now < end


def get_actual_show_index(schedule):
    """
    Get the index of the actual show.
    """
    now = datetime.now(pytz.timezone(CONF_TIME_ZONE))
    for i in range(len(schedule)):
        start = parse_time(schedule[i]["start_time"])
        end = parse_time(schedule[i]["end_time"])
        if in_between(now, start, end):
            return i
    return -1


def get_attributes(channel_id):
    """
    Get the ongoing TV show, the previous and next show, plus all schedule for the day.
    """
    schedule = get_schedules(channel_id)

    actual_show = {}
    previous_show = {}
    next_show = {}
    index = get_actual_show_index(schedule)
    if index >= 0:
        actual_show = schedule[index]
        # check lower bound
        if index - 1 >= 0:
            previous_show = schedule[index - 1]
        # check upper bound
        if index + 1 <= len(schedule):
            next_show = schedule[index + 1]
    return actual_show, previous_show, next_show, schedule

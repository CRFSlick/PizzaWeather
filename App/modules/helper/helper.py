from datetime import datetime
import requests
import base64


def unix_to_12_hr_time(unix_timestamp, offset):
    """
    Converts unix timestamp to 12 hour time

    Args:
        unix_timestamp (int)
        offset (int)
    """
    return datetime.utcfromtimestamp(unix_timestamp + offset).strftime('%I:%M %p').lstrip("0").replace(" 0", " ")


def unix_to_date(unix_timestamp, offset):
    """
    Converts unix timestamp to date

    Args:
        unix_timestamp (int)
        offset (int)
    """
    return datetime.utcfromtimestamp(unix_timestamp + offset).strftime('%m/%d/%Y')


def get_local_time(offset):
    """
    Gets local time given an offset from UTC time

    Args:
        offset (int)
    """
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return datetime.utcfromtimestamp(timestamp + offset).strftime('%I:%M %p').lstrip("0").replace(" 0", " ")


def get_local_date(offset):
    """
    Gets local date given an offset from UTC time

    Args:
        offset (int)
    """
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return datetime.utcfromtimestamp(timestamp + offset).strftime('%m/%d/%Y')


def image_to_base64(image_url):
    """
    Converts radar image URL to base64

    Args:
        image_url (str)
    """
    r = requests.get(image_url)
    if r.status_code == 200:
        image_data = base64.b64encode(r.content).decode('UTF-8')
        return image_data

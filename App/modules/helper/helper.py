from datetime import datetime


def unix_to_12_hr_time(unix_timestamp, offset):
    return datetime.utcfromtimestamp(unix_timestamp + offset).strftime('%I:%M %p').lstrip("0").replace(" 0", " ")


def unix_to_date(unix_timestamp, offset):
    return datetime.utcfromtimestamp(unix_timestamp + offset).strftime('%m/%d/%Y')


def get_local_time(offset):
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return datetime.utcfromtimestamp(timestamp + offset).strftime('%I:%M %p').lstrip("0").replace(" 0", " ")


def get_local_date(offset):
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return datetime.utcfromtimestamp(timestamp + offset).strftime('%m/%d/%Y')
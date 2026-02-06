from decimal import Decimal
from datetime import datetime


def timestamp_to_second(timestamp):
    time_obj = datetime.strptime(timestamp, "%H:%M:%S.%f")
    time_in_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second + time_obj.microsecond / 1e6
    return round(Decimal(time_in_seconds), 4)


def second_to_timestamp(time_in_seconds):
    minutes, seconds = divmod(int(time_in_seconds), 60)
    hours, minutes = divmod(minutes, 60)
    milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)
    timestamp = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    return timestamp

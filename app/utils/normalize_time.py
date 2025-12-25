from datetime import datetime, timedelta


def normalize_time(user_input: str) -> str:
    """
    Normalize a user-provided time string (HH:MM:SS) to the nearest hour.
    Special case: if hour == 23 and minutes >= 30, round down to 23:00:00.

    Args:
        user_input (str): Time string in format "HH:MM:SS"

    Returns:
        str: Normalized time string in format "HH:00:00"
    """
    # Parse string into datetime object
    user_time = datetime.strptime(user_input, "%H:%M:%S")

    hour = user_time.hour
    minutes = user_time.minute
    seconds = user_time.second

    # Edge case: 23:30:00 or later → snap down to 23:00:00
    if hour == 23 and minutes >= 30:
        rounded_time = user_time.replace(hour=23, minute=0, second=0)

    # General case: round up if minutes >= 30 (or exactly 30 with seconds > 0)
    elif minutes > 30 or (minutes == 30 and seconds > 0):
        rounded_time = user_time.replace(
            minute=0, second=0) + timedelta(hours=1)

    # Otherwise round down
    else:
        rounded_time = user_time.replace(minute=0, second=0)

    return rounded_time.strftime("%H:%M:%S")

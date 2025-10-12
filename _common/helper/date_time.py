from datetime import datetime, timedelta

DT_FORMAT_YMDHMS = "%Y-%m-%d %H:%M:%S"


def dt_local_to_utc(dt):
    """Convert local datetime to UTC."""
    return datetime.utcfromtimestamp(datetime.timestamp(dt))


def lookup_range_str_to_timestamp(start_time=None, end_time=None, lookup_hours=1, local_to_utc=False):
    """
    start_time and end_time format "%Y-%m-%d %H:%M:%S" (e.g. 2020-04-01 04:00:00)

    If end_time is None, current date/time will be used.
    If start_time is None, start_time will be set to (end_time - lookup_hours)
    """
    end_dt = datetime.now() if end_time is None else datetime.strptime(end_time, DT_FORMAT_YMDHMS)
    if start_time is None:
        start_dt = end_dt - timedelta(hours=lookup_hours)
    else:
        start_dt = datetime.strptime(start_time, DT_FORMAT_YMDHMS)

    if start_dt > end_dt:
        raise Exception(f"start_dt {start_dt} > end_dt {end_dt}")

    if local_to_utc:
        end_dt = dt_local_to_utc(end_dt)
        start_dt = dt_local_to_utc(start_dt)

    return start_dt, end_dt


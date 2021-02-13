from datetime import datetime

import pytest
from helper.datetime import lookup_range_str_to_timestamp


def test_lookup_range_str_to_timestamp_passed():
    start_time = "2021-02-12 08:00:00"
    end_time = "2021-02-13 08:00:00"
    start_dt, end_dt = lookup_range_str_to_timestamp(start_time, end_time)
    assert start_dt == datetime(2021, 2, 12, 8, 0)
    assert end_dt == datetime(2021, 2, 13, 8, 0)

    start_time = None
    end_time = "2021-02-13 08:00:00"
    start_dt, end_dt = lookup_range_str_to_timestamp(start_time, end_time)
    assert start_dt == datetime(2021, 2, 13, 7, 0)
    assert end_dt == datetime(2021, 2, 13, 8, 0)


def test_lookup_range_str_to_timestamp_failed_greater_start_time():
    start_time = "2021-02-13 08:00:00"
    end_time = "2021-02-12 08:00:00"
    with pytest.raises(Exception) as e_info:
        lookup_range_str_to_timestamp(start_time, end_time)


def test_lookup_range_str_to_timestamp_failed_invalid_format():
    start_time = "2021-02-13 08:00"
    end_time = None
    with pytest.raises(Exception) as e_info:
        lookup_range_str_to_timestamp(start_time, end_time)

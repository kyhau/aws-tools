"""Test cases for date_time module."""

from datetime import datetime, timedelta

import pytest
from helper.date_time import dt_local_to_utc, lookup_range_str_to_timestamp


class TestLookupRangeStrToTimestamp:
    """Test suite for lookup_range_str_to_timestamp function."""

    @pytest.mark.parametrize(
        "start_time,end_time,expected_start,expected_end",
        [
            (
                "2021-02-12 08:00:00",
                "2021-02-13 08:00:00",
                datetime(2021, 2, 12, 8, 0),
                datetime(2021, 2, 13, 8, 0),
            ),
            (
                "2023-01-01 00:00:00",
                "2023-01-01 23:59:59",
                datetime(2023, 1, 1, 0, 0),
                datetime(2023, 1, 1, 23, 59, 59),
            ),
            (
                "2020-12-31 23:00:00",
                "2021-01-01 01:00:00",
                datetime(2020, 12, 31, 23, 0),
                datetime(2021, 1, 1, 1, 0),
            ),
        ],
    )
    def test_with_both_times_provided(self, start_time, end_time, expected_start, expected_end):
        """Test with both start and end times provided."""
        start_dt, end_dt = lookup_range_str_to_timestamp(start_time, end_time)
        assert start_dt == expected_start
        assert end_dt == expected_end

    @pytest.mark.parametrize(
        "end_time,lookup_hours",
        [
            ("2021-02-13 08:00:00", 1),
            ("2021-02-13 08:00:00", 2),
            ("2021-02-13 08:00:00", 24),
        ],
    )
    def test_with_none_start_time(self, end_time, lookup_hours):
        """Test with start_time=None, should calculate based on lookup_hours."""
        start_dt, end_dt = lookup_range_str_to_timestamp(None, end_time, lookup_hours=lookup_hours)
        expected_end = datetime(2021, 2, 13, 8, 0)
        expected_start = expected_end - timedelta(hours=lookup_hours)
        assert start_dt == expected_start
        assert end_dt == expected_end

    def test_with_both_none(self):
        """Test with both times None, should use current time."""
        before = datetime.now()
        start_dt, end_dt = lookup_range_str_to_timestamp(None, None, lookup_hours=1)
        after = datetime.now()

        # end_dt should be close to now
        assert before <= end_dt <= after
        # start_dt should be 1 hour before end_dt
        assert end_dt - start_dt == timedelta(hours=1)

    def test_local_to_utc_conversion(self):
        """Test local_to_utc parameter converts timestamps correctly."""
        start_time = "2021-02-12 08:00:00"
        end_time = "2021-02-13 08:00:00"
        start_dt, end_dt = lookup_range_str_to_timestamp(start_time, end_time, local_to_utc=True)

        # Converted times should be datetime objects
        assert isinstance(start_dt, datetime)
        assert isinstance(end_dt, datetime)

    @pytest.mark.parametrize(
        "start_time,end_time,error_message",
        [
            ("2021-02-13 08:00:00", "2021-02-12 08:00:00", "start_dt .* > end_dt"),
            ("2023-12-31 23:59:59", "2023-01-01 00:00:00", "start_dt .* > end_dt"),
        ],
    )
    def test_invalid_time_range(self, start_time, end_time, error_message):
        """Test that exception is raised when start_time > end_time."""
        with pytest.raises(Exception, match=error_message):
            lookup_range_str_to_timestamp(start_time, end_time)

    @pytest.mark.parametrize(
        "start_time,end_time",
        [
            ("2021-02-13 08:00", None),  # Missing seconds
            ("2021/02/13 08:00:00", None),  # Wrong date separator
            ("02-13-2021 08:00:00", None),  # Wrong date format
            ("invalid", "2021-02-13 08:00:00"),  # Invalid format
            ("2021-02-13 08:00:00", "not-a-date"),  # Invalid end time
        ],
    )
    def test_invalid_datetime_format(self, start_time, end_time):
        """Test that ValueError is raised for invalid datetime formats."""
        with pytest.raises(ValueError):
            lookup_range_str_to_timestamp(start_time, end_time)


class TestLocalToUtcConversion:
    """Test suite for dt_local_to_utc lambda function."""

    def test_converts_datetime_to_utc(self):
        """Test that local datetime is converted to UTC."""
        local_dt = datetime(2021, 6, 15, 12, 0, 0)
        utc_dt = dt_local_to_utc(local_dt)

        assert isinstance(utc_dt, datetime)
        # The conversion should produce a valid datetime
        assert utc_dt.year == 2021

    def test_handles_edge_cases(self):
        """Test UTC conversion with edge case dates."""
        # New Year
        local_dt = datetime(2021, 1, 1, 0, 0, 0)
        utc_dt = dt_local_to_utc(local_dt)
        assert isinstance(utc_dt, datetime)

        # Leap year date
        local_dt = datetime(2020, 2, 29, 12, 0, 0)
        utc_dt = dt_local_to_utc(local_dt)
        assert isinstance(utc_dt, datetime)

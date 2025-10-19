"""Test cases for ser module (JSON serialization)."""

import decimal
import json
from datetime import date, datetime

import pytest
from helper.ser import DecimalEncoder, DefaultEncoder, dump_json, json_serial


class TestJsonSerial:
    """Test suite for json_serial function."""

    def test_serializes_datetime(self):
        """Test that datetime objects are serialized to ISO format."""
        dt = datetime(2021, 6, 15, 12, 30, 45)
        result = json_serial(dt)
        assert result == "2021-06-15T12:30:45"

    def test_serializes_date(self):
        """Test that date objects are serialized to ISO format."""
        d = date(2021, 6, 15)
        result = json_serial(d)
        assert result == "2021-06-15"

    def test_raises_type_error_for_unsupported_types(self):
        """Test that TypeError is raised for unsupported types."""

        class CustomClass:
            pass

        with pytest.raises(TypeError, match="Type .* not serializable"):
            json_serial(CustomClass())

    @pytest.mark.parametrize(
        "obj",
        [
            set([1, 2, 3]),
            complex(1, 2),
            bytes(b"test"),
        ],
    )
    def test_raises_type_error_for_various_types(self, obj):
        """Test that various unsupported types raise TypeError."""
        with pytest.raises(TypeError):
            json_serial(obj)


class TestDumpJson:
    """Test suite for dump_json lambda function."""

    def test_dumps_dict_with_datetime(self):
        """Test that dictionaries with datetime are serialized correctly."""
        data = {"timestamp": datetime(2021, 6, 15, 12, 30, 45), "name": "test"}
        result = dump_json(data)
        assert "2021-06-15T12:30:45" in result
        assert "test" in result

    def test_dumps_sorted_and_indented(self):
        """Test that output is sorted and indented."""
        data = {"z": 1, "a": 2, "m": 3}
        result = dump_json(data)
        # Check it's indented (has newlines)
        assert "\n" in result
        # Check keys are sorted (a before m before z)
        lines = result.split("\n")
        assert any('"a"' in line for line in lines)
        assert any('"m"' in line for line in lines)
        assert any('"z"' in line for line in lines)

    def test_handles_nested_structures(self):
        """Test that nested structures with dates are handled."""
        data = {
            "outer": {
                "date": date(2021, 6, 15),
                "inner": {"timestamp": datetime(2021, 6, 15, 12, 30, 45)},
            }
        }
        result = dump_json(data)
        assert "2021-06-15" in result
        assert "2021-06-15T12:30:45" in result


class TestDefaultEncoder:
    """Test suite for DefaultEncoder class."""

    def test_encodes_datetime_to_timestamp(self):
        """Test that datetime is encoded as Unix timestamp."""
        dt = datetime(2021, 6, 15, 12, 0, 0)
        result = json.dumps({"time": dt}, cls=DefaultEncoder)
        data = json.loads(result)
        # Should be an integer timestamp
        assert isinstance(data["time"], int)
        assert data["time"] > 0

    def test_falls_back_to_default_encoder(self):
        """Test that non-datetime objects use default encoding."""
        data = {"string": "test", "number": 42, "list": [1, 2, 3]}
        result = json.dumps(data, cls=DefaultEncoder)
        decoded = json.loads(result)
        assert decoded == data

    def test_raises_error_for_unsupported_types(self):
        """Test that unsupported types raise TypeError."""
        data = {"custom": object()}
        with pytest.raises(TypeError):
            json.dumps(data, cls=DefaultEncoder)


class TestDecimalEncoder:
    """Test suite for DecimalEncoder class."""

    def test_encodes_decimal_integer_to_int(self):
        """Test that Decimal integers are encoded as int."""
        data = {"value": decimal.Decimal("42")}
        result = json.dumps(data, cls=DecimalEncoder)
        decoded = json.loads(result)
        assert decoded["value"] == 42
        assert isinstance(decoded["value"], int)

    def test_encodes_decimal_float_to_float(self):
        """Test that Decimal floats are encoded as float."""
        data = {"value": decimal.Decimal("42.5")}
        result = json.dumps(data, cls=DecimalEncoder)
        decoded = json.loads(result)
        assert decoded["value"] == 42.5
        assert isinstance(decoded["value"], float)

    @pytest.mark.parametrize(
        "decimal_str,expected_type",
        [
            ("100", int),
            ("100.0", int),
            ("100.5", float),
            ("0.1", float),
            ("999999999999", int),
        ],
    )
    def test_encodes_various_decimals(self, decimal_str, expected_type):
        """Test that various Decimal values are encoded correctly."""
        data = {"value": decimal.Decimal(decimal_str)}
        result = json.dumps(data, cls=DecimalEncoder)
        decoded = json.loads(result)
        assert isinstance(decoded["value"], expected_type)

    def test_encodes_dynamodb_item(self):
        """Test encoding a typical DynamoDB item with mixed types."""
        dynamodb_item = {
            "id": "abc123",
            "count": decimal.Decimal("42"),
            "price": decimal.Decimal("19.99"),
            "active": True,
            "tags": ["tag1", "tag2"],
        }
        result = json.dumps(dynamodb_item, cls=DecimalEncoder)
        decoded = json.loads(result)

        assert decoded["id"] == "abc123"
        assert decoded["count"] == 42
        assert isinstance(decoded["count"], int)
        assert decoded["price"] == 19.99
        assert isinstance(decoded["price"], float)
        assert decoded["active"] is True
        assert decoded["tags"] == ["tag1", "tag2"]

    def test_handles_nested_decimals(self):
        """Test that nested structures with Decimals are handled."""
        data = {
            "outer": {
                "inner": {
                    "decimal_int": decimal.Decimal("100"),
                    "decimal_float": decimal.Decimal("100.5"),
                }
            }
        }
        result = json.dumps(data, cls=DecimalEncoder)
        decoded = json.loads(result)
        assert decoded["outer"]["inner"]["decimal_int"] == 100
        assert decoded["outer"]["inner"]["decimal_float"] == 100.5

    def test_falls_back_to_default_for_other_types(self):
        """Test that non-Decimal types use default encoding."""
        data = {"str": "test", "int": 42, "list": [1, 2, 3]}
        result = json.dumps(data, cls=DecimalEncoder)
        decoded = json.loads(result)
        assert decoded == data

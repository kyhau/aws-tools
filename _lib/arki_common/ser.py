from datetime import date, datetime
import decimal
import json
from time import mktime


def json_serial(obj):
    """
    JSON serializer for objects not serializable by default json code
    Usage example: json.dumps(data, default=json_serial, indent=2, sort_keys=True)
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


dump_json = lambda x: json.dumps(x, default=json_serial, indent=2, sort_keys=True)


class DefaultEncoder(json.JSONEncoder):
    """
    Encode for the json
    Usage example: json.dumps(data, cls=DefaultEncoder, indent=2, sort_keys=True)
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return int(mktime(obj.timetuple()))
        return json.JSONEncoder.default(self, obj)



class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert a DynamoDB item to JSON."""
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

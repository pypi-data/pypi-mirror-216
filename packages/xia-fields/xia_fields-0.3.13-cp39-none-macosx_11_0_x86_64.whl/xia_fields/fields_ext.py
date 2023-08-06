import os
from typing import Any, Union
from datetime import datetime, timezone, date, time
from xia_fields.fields import IntField, GeneralTimeField, StringField


class Int64Field(IntField):
    """Int64 Field
    """
    def __init__(self, **kwargs):
        kwargs["value_min"] = max(kwargs.get("value_min", -2**63), -2**63)
        kwargs["value_max"] = min(kwargs.get("value_max", 2**63-1), 2**63-1)
        super().__init__(**kwargs)


class UInt64Field(IntField):
    """Unsigned Int64 Field
    """
    def __init__(self, **kwargs):
        kwargs["value_min"] = max(kwargs.get("value_min", 0), 0)
        kwargs["value_max"] = min(kwargs.get("value_max", 2**64-1), 2**64-1)
        super().__init__(**kwargs)


class Int32Field(Int64Field):
    """Int32 Field
    """
    def __init__(self, **kwargs):
        kwargs["value_min"] = max(kwargs.get("value_min", -2**31), -2**31)
        kwargs["value_max"] = min(kwargs.get("value_max", 2**31-1), 2**31-1)
        super().__init__(**kwargs)


class UInt32Field(UInt64Field):
    """Unsigned Int32 Field
    """
    def __init__(self, **kwargs):
        kwargs["value_min"] = max(kwargs.get("value_min", 0), 0)
        kwargs["value_max"] = min(kwargs.get("value_max", 2**32-1), 2**32-1)
        super().__init__(**kwargs)


class DateField(GeneralTimeField):
    """Date Field

    Value Forms:
        * Database form: int as epoch time
        * Internal form: python date object
        * Display form: string defined by dt_format (standard python output definition)

    Notes:
        * The standard guess only supports the following standard formats
    """
    BASE = datetime.fromtimestamp(0.0, tz=timezone.utc).date()

    db_form = int
    internal_form = date
    display_form = str

    def __init__(self, dt_format: str = '%Y-%m-%d', tz=None, **kwargs):
        super().__init__(dt_format, tz=timezone.utc, **kwargs)

    def from_db(self, value: Union[date, int], /, decoder: callable = None, engine = None):
        value = value if not decoder else decoder(value)
        return super().from_display(value*86400.0).date()

    def to_db(self, value: Any, runtime_value: Any = None, /,
              catalog: dict = None, encoder: callable = None, ignore_unknown: bool = False, engine=None):
        if isinstance(value, date):
            value = (value - self.BASE).days
        return value if not encoder else encoder(value)

    def from_display(self, value: Any, runtime_display: Any = None, /):
        return super().from_display(value).date() if isinstance(value, (float, str)) else value

    def to_display(self, value: Any, runtime_value: Any = None, /, **kwargs):
        return value.strftime(self.dt_format) if isinstance(value, date) else value


class TimeField(GeneralTimeField):
    """Time Field

    Value Forms:
        * Database form: float (The difference from 00:00:00 UTC)
        * Internal form: python time object
        * Display form: string defined by dt_format (standard python output definition)

    Notes:
        * The standard guess only supports the following standard formats
    """
    db_form = float
    internal_form = time
    display_form = str

    _guess_with_length = {
        4: {'%H%M': []},
        5: {'%H:%M': [":"]},
        6: {'%H%M%S': []},
        8: {'%H:%M:%S': [":"]},
        10: {'%H:%M:%S.%f': [":", "."]},
        11: {'%H:%M:%S.%f': [":", "."]},
        12: {'%H:%M:%S.%f': [":", "."]},
        13: {'%H:%M:%S.%f': [":", "."]},
        14: {'%H:%M:%S.%f': [":", "."]},
        15: {'%H:%M:%S.%f': [":", "."]},
    }

    _guess_with_length_tz = {
        13: {'%H:%M:%S%z': ["-", ":", " "]},
        14: {'%H:%M:%S%z': ["-", ":", " "]},
        16: {'%H:%M:%S.%f%z': [":", "."]},
        17: {'%H:%M:%S.%f%z': [":", "."]},
        18: {'%H:%M:%S.%f%z': [":", "."]},
        19: {'%H:%M:%S.%f%z': [":", "."]},
        20: {'%H:%M:%S.%f%z': [":", "."]},
        21: {'%H:%M:%S.%f%z': [":", "."]},
    }

    def __init__(self, dt_format: str = '%H:%M:%S', tz=None, **kwargs):
        super().__init__(dt_format, tz=tz, **kwargs)

    def from_display(self, value: Any, runtime_display: Any = None, /):
        return super().from_display(value).time()

    def to_db(self, value: Any, runtime_value: Any = None, /,
              catalog: dict = None, encoder: callable = None, ignore_unknown: bool = False, engine=None):
        if isinstance(value, time):
            value = (datetime.combine(date(1970, 1, 1), value, tzinfo=timezone.utc) - self.BASE).total_seconds()
        return value if not encoder else encoder(value)

    def to_display(self, value: Any, runtime_value: Any = None, /, **kwargs):
        return value.strftime(self.dt_format) if isinstance(value, time) else value


class TimestampField(GeneralTimeField):
    """Timestamp Field

    Value Forms:
        * Database form: float as timestamp
        * Internal form: float
        * Display form: string defined by dt_format (standard python output definition)
    """
    db_form = float
    internal_form = float
    display_form = str

    def __init__(self, dt_format: str = '%Y-%m-%d %H:%M:%S.%f', tz=None, **kwargs):
        super().__init__(dt_format, tz, **kwargs)
        self.tz = timezone.utc  # Timestamp field could only show time in UTC

    def from_db(self, value: Any, /, decoder: callable = None, engine = None):
        value = value if not decoder else decoder(value)
        return value

    def from_display(self, value: Any, runtime_display: Any = None, /):
        return self.parse_date(value).timestamp()

    def to_display(self, value: Any, runtime_value: Any = None, /, **kwargs):
        return datetime.fromtimestamp(value, tz=timezone.utc).astimezone(self.tz).strftime(self.dt_format)

    def to_db(self, value: Any, runtime_value: Any = None, /,
              catalog: dict = None, encoder: callable = None, ignore_unknown: bool = False, engine=None):
        value = value - self.BASE.timestamp()
        return value if not encoder else encoder(value)


class DateTimeField(GeneralTimeField):
    """Date Time Field

    Value Forms:
        * Database form: float
        * Internal form: python datetime object
        * Display form: string defined by dt_format (standard python output definition)

    Notes:
        * The standard guess only supports the following standard formats
    """


class OsEnvironField(StringField):
    """Environment Variable Field

    Value Forms:
        * Database form: Environment variable Name
        * Internal form: Bytes (encode) => Variable Value
        * Display form: String (decode) => Variable Value

    Args:
        prefix:
            The variable value start with prefix will be considered as the name of environment variable.
            For the security reason, only the environment variable name start with prefix will be interpreted.
    """
    db_form = str
    internal_form = bytes
    runtime_form = str
    display_form = str
    detail_form = str

    def __init__(self, prefix="XIA_", **kwargs):
        kwargs["runtime"] = True  # CompressedStringField is a runtime field
        self.prefix = prefix  # Need a prefix to get the environment value back
        super().__init__(**kwargs)

    def validate(self, value: Any, runtime_value: Any = None, /):
        if value:
            value = value.decode() if isinstance(value, bytes) else value
            if not value.startswith(self.prefix):
                raise ValueError(f"Environment variable must start with {self.prefix}")

    def get_sample(self):
        return (self.prefix + "NAME").encode(), "Variable Value"

    def guess_value(self, value: str = None):
        if value is None or isinstance(value, self.internal_form):
            # Case 1: We are sure that it is the environment variable name
            return value, None
        elif value.startswith(self.prefix):
            # Case 2: Possible to define the value with a given prefix
            return value.encode(), None
        else:
            # Case 3: Need to Find the environment variable name back
            for env_key, env_value in os.environ.items():
                if env_key.startswith(self.prefix) and env_value == value:
                    return env_key.encode(), env_value
            return None, value  # Can not find the initial value so return None

    def get_value(self, value: Any = None, runtime_value: Any = None, /, **kwargs):
        return value, os.environ.get(value.decode()) if value is not None else None

    def to_db(self, value: Any, runtime_value: Any = None, /,
              catalog: dict = None , encoder: callable = None, ignore_unknown: bool = False, engine=None):
        return value.decode() if not encoder else encoder(value.decode())

    def from_db(self, value: Any, /, decoder: callable = None, engine=None):
        return value.encode() if not decoder else decoder(value.encode())

    def to_display(self, value: Any, runtime_value: Any = None, /, **kwargs):
        if isinstance(value, self.internal_form):
            return value.decode(), runtime_value
        else:
            return value, runtime_value

    def from_display(self, value: Any, runtime_display: Any = None, /):
        if isinstance(value, self.display_form):
            return value.encode(), runtime_display
        else:
            return value, runtime_display

    def from_runtime(self, runtime_value: str, /):
        for env_key, env_value in os.environ.items():
            if env_key.startswith(self.prefix) and env_value == runtime_value:
                return env_key.encode()

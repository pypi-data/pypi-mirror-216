"""Different Field Implementations"""
import base64
import json
import gzip
import re
import locale
import decimal
from typing import Any, Union
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from xia_fields.base import BaseField


class BooleanField(BaseField):
    """Boolean Field

    Warnings:
        * The text will trigger false are "FALSE", "NON", "NEE", "NEIN"
        * None will be loaded as None instead of False
    """
    db_form = bool
    internal_form = bool
    display_form = bool

    def from_display(self, value: Any, runtime_display: Any = None, /):
        if isinstance(value, str) and value.upper() in ["FALSE", "NON", "NEE", "NEIN"]:
            return False
        else:
            return bool(value)


class StringField(BaseField):
    """String Field

    """
    db_form = str
    internal_form = str
    display_form = str

    def __init__(self, regex: str = None, max_length: int = None, min_length: int = None, **kwargs):
        """
        Args:
            regex (str): String pattern
            max_length (int): A max length that will be applied during validation
            min_length (int): A min length that will be applied during validation
            **kwargs: Keyword arguments passed into the parent class
        """
        self.regex = re.compile(regex) if regex else None
        self.max_length = max_length
        self.min_length = min_length
        super().__init__(**kwargs)

    def validate(self, value: Any, runtime_value: Any = None, /):
        super().validate(value)

        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError("String value is too long")

        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError("String value is too short")

        if self.regex is not None and self.regex.match(value) is None:
            raise ValueError("String value did not match validation regex")

    """
    It is a better idea to raise exception or it will be very likely a hidden bug
    def guess_value(self, value: Any = None):
        return None if value is None else str(value)
    """

    def estimate_max_length(self) -> int:
        """Estimate Max length of the string

        Returns:
            Max string length
        """
        if self.max_length is not None:
            return self.max_length
        elif '\n' in self.sample:
            return 2 ** 20
        else:
            return 2 * len(self.sample)


class IntField(BaseField):
    """Int Field

    Note:
        * String to float conversion using python local settings
        * Accepting decimal but the decimal part will be truncated after load
    """
    db_form = int
    internal_form = int
    display_form = (float, int, str)

    def from_display(self, value: Any, runtime_display: Any = None, /):
        if isinstance(value, str):
            return int(locale.atof(value))
        else:
            return int(value)


class FloatField(BaseField):
    """Float Field

    Note:
        * String to float conversion using python local settings
    """
    db_form = float
    internal_form = float
    display_form = float

    def from_display(self, value: Any, runtime_display: Any = None, /):
        if isinstance(value, str):
            return locale.atof(value)
        else:
            return float(value)

    def guess_value(self, value: Any = None):
        return self.from_display(value)


class DecimalField(BaseField):
    """Decimal Field

    """
    db_form = str
    internal_form = decimal.Decimal
    display_form = (str, float)

    def __init__(self, precision: int = None, rounding=decimal.ROUND_HALF_UP, **kwargs):
        """
        Args:
            precision (int): precision of number
            rounding : rounding method (the same as python decimal module)
            **kwargs: Keyword arguments passed into the parent class
        """
        self.precision = precision
        self.rounding = rounding
        super().__init__(**kwargs)

    def to_db(self, value: Any, runtime_value: Any = None, /,
              catalog: dict = None, encoder: callable = None, ignore_unknown: bool = False, engine=None):
        return str(value) if not encoder else encoder(str(value))

    def from_db(self, value: Any, decoder: callable = None, engine = None):
        value = value if not decoder else decoder(value)
        return self.from_display(value)

    def to_display(self, value: Any, runtime_value: Any = None, /, **kwargs):
        return str(value)

    def from_display(self, value: Any, runtime_display: Any = None, /):
        value = 0 if not value else value
        if self.precision:
            quantizer = decimal.Decimal("1E-" + str(self.precision))
            return decimal.Decimal(value).quantize(quantizer, self.rounding)
        else:
            return decimal.Decimal(value)


class GeneralTimeField(BaseField):
    """General Time Field

    Notes:
        * The standard guess only supports the following standard formats
    """
    BASE = datetime.fromtimestamp(0.0, tz=timezone.utc)

    db_form = float
    internal_form = datetime
    display_form = str

    _guess_with_length = {
        6: {'%Y%m': []},
        7: {'%Y-%m': ["-"]},
        8: {'%Y%m%d': []},
        10: {'%Y-%m-%d': ["-"]},
        16: {'%Y-%m-%d %H:%M': ["-", ":", " "], '%Y-%m-%dT%H:%M': ["-", ":", "T"]},
        19: {'%Y-%m-%d %H:%M:%S': ["-", ":", " "], '%Y-%m-%dT%H:%M:%S': ["-", ":", "T"]},
        20: {'%Y-%m-%d %H:%M:%SZ': ["-", ":", " ", "Z"], '%Y-%m-%dT%H:%M:%SZ': ["-", ":", "T", "Z"]},
        23: {'%Y-%m-%d %H:%M:%S.%f': ["-", ":", " ", "."], '%Y-%m-%dT%H:%M:%S.%f': ["-", ":", "T", "."]},
        26: {'%Y-%m-%d %H:%M:%S.%f': ["-", ":", " ", "."], '%Y-%m-%dT%H:%M:%S.%f': ["-", ":", "T", "."]},
    }
    _guess_with_length_tz = {
        24: {'%Y-%m-%d %H:%M:%S%z': ["-", ":", " "], '%Y-%m-%dT%H:%M:%S%z': ["-", ":", "T"]},
        25: {'%Y-%m-%d %H:%M:%S%z': ["-", ":", " "], '%Y-%m-%dT%H:%M:%S%z': ["-", ":", "T"]},
        28: {'%Y-%m-%d %H:%M:%S.%f%z': ["-", ":", " ", "."], '%Y-%m-%dT%H:%M:%S.%f%z': ["-", ":", "T", "."]},
        29: {'%Y-%m-%d %H:%M:%S.%f%z': ["-", ":", " ", "."], '%Y-%m-%dT%H:%M:%S.%f%z': ["-", ":", "T", "."]},
        31: {'%Y-%m-%d %H:%M:%S.%f%z': ["-", ":", " ", "."], '%Y-%m-%dT%H:%M:%S.%f%z': ["-", ":", "T", "."]},
        32: {'%Y-%m-%d %H:%M:%S.%f%z': ["-", ":", " ", "."], '%Y-%m-%dT%H:%M:%S.%f%z': ["-", ":", "T", "."]},
    }

    def __init__(self, dt_format: str = '%Y-%m-%d %H:%M:%S.%f', tz=None, **kwargs):
        """
        Args:
            dt_format (str): Standard datetime format
            tz : Timezone for display
            **kwargs: Keyword arguments passed into the parent class
        """
        self.dt_format = dt_format
        if tz is None:
            self.tz = timezone(timedelta(seconds=round(datetime.now().timestamp() - datetime.utcnow().timestamp())))
        else:
            self.tz = tz
        super().__init__(**kwargs)

    def _get_description(self):
        return f"{self.__class__.__name__} with format {self.dt_format}. Example: {self.get_sample()}"

    def parse_date(self, value: str):
        """Parse date from string

        Args:
            value (str): String to be parsed

        Returns:
            datetime object
        """
        value = value.strip()
        try:
            dt_temp = datetime.strptime(value, self.dt_format)
            return datetime.combine(dt_temp.date(), dt_temp.time(), tzinfo=self.tz)
        except (ValueError, TypeError):
            pass  # Not a big deal, Let's guess the correct date time format
        dt_length = len(value)
        if dt_length in self._guess_with_length:
            for dt_format, key_words in self._guess_with_length[dt_length].items():
                if all([key_word in value for key_word in key_words]):
                    try:
                        dt_temp = datetime.strptime(value, dt_format)
                        return datetime.combine(dt_temp.date(), dt_temp.time(), tzinfo=self.tz)
                    except (ValueError, TypeError):  # pragma: no cover
                        pass  # We still have a last chance
        elif dt_length in self._guess_with_length_tz:
            for dt_format, key_words in self._guess_with_length_tz[dt_length].items():
                if all([key_word in value for key_word in key_words]):
                    try:
                        return datetime.strptime(value, dt_format)
                    except (ValueError, TypeError):  # pragma: no cover
                        pass  # We still have a last chance by using email format parse
        try:  # Last chance
            return parsedate_to_datetime(value)
        except (ValueError, TypeError):  # pragma: no cover
            raise ValueError(f"Unknown datetime value: {value}")  # Raise a final error

    def from_db(self, value: Any, /, decoder: callable = None, engine = None):
        value = value if not decoder else decoder(value)
        return datetime.fromtimestamp(0, tz=timezone.utc) + timedelta(seconds=value)

    def to_db(self, value: Any, runtime_value: Any = None, /,
              catalog: dict = None, encoder: callable = None, ignore_unknown: bool = False, engine=None):
        value = (value - self.BASE).total_seconds()
        return value if not encoder else encoder(value)

    def from_display(self, value: Any, runtime_display: Any = None, /):
        if isinstance(value, (float, int)):
            return datetime.fromtimestamp(0, tz=timezone.utc) + timedelta(seconds=value)
        else:
            return self.parse_date(value)

    def to_display(self, value: Any, runtime_value: Any = None, /, **kwargs):
        return value.astimezone(self.tz).strftime(self.dt_format) if isinstance(value, datetime) else value


class JsonField(BaseField):
    """Json Field, could be list or dict

    Value Forms:
        * Database form: json string
        * Internal form: python object by using loads function of json module
        * Display form: json string
    """

    db_form = str
    internal_form = (list, dict)
    display_form = str

    def get_sample(self):
        return {"key": "value"}

    def to_db(self, value: Any, runtime_value: Any = None, /,
              catalog: dict = None, encoder: callable = None, ignore_unknown: bool = False, engine=None):
        return json.dumps(value, ensure_ascii=False) if not encoder else encoder(json.dumps(value, ensure_ascii=False))

    def from_db(self, value: Union[str, list, dict], /, decoder: callable = None, engine = None):
        value = value if not decoder else decoder(value)
        return self.from_display(value)

    def to_display(self, value: Any, runtime_value: Any = None, /, **kwargs):
        return json.dumps(value, ensure_ascii=False)

    def from_display(self, value: Any, runtime_display: Any = None, /):
        return json.loads(value)


class CompressedStringField(BaseField):
    """Compressed String Field

    Value Forms:
        * Database form: Compressed data (bytes)
        * Internal form: Bytes
        * Display form: String
    """
    db_form = bytes
    internal_form = bytes
    runtime_form = str
    display_form = str
    detail_form = str

    def __init__(self, **kwargs):
        kwargs["runtime"] = True  # CompressedStringField is a runtime field
        super().__init__(**kwargs)

    def get_sample(self):
        return gzip.compress("Hello world".encode(), mtime=0), "Hello world"

    def guess_value(self, value: str = None):
        if value is None or isinstance(value, self.internal_form):
            return value, None
        if value.startswith("H4sI"):  # Very likely a base64 encoded field
            return base64.b64decode(value.encode()), None
        else:
            return gzip.compress(value.encode(), mtime=0), value

    def to_display(self, value: Any, runtime_value: Any = None, /, **kwargs):
        if value is None:
            return None, runtime_value
        elif isinstance(value, str):
            return value, runtime_value
        else:
            return base64.b64encode(value).decode(), runtime_value

    def from_display(self, value: Any, runtime_display: Any = None, /):
        if isinstance(runtime_display, str):
            return gzip.compress(runtime_display.encode(), mtime=0), runtime_display
        else:
            return base64.b64decode(value.encode()), runtime_display

    def from_runtime(self, runtime_value: str, /):
        return gzip.compress(runtime_value.encode(), mtime=0)

    def get_value(self, value: Any = None, runtime_value: Any = None, /, **kwargs):
        return value, gzip.decompress(value).decode() if value is not None else None


class ByteField(BaseField):
    """Byte Field. Will be displayed as base64 string

    Value Forms:
        * Database form: bytes
        * Internal form: bytes
        * Display form: bytes as base64 encoded
    """
    db_form = bytes
    internal_form = bytes
    display_form = str

    def to_display(self, value: Any, runtime_value: Any = None, /, **kwargs):
        return base64.b64encode(value).decode()

    def from_display(self, value: Any, runtime_display: Any = None, /):
        return base64.b64decode(value)


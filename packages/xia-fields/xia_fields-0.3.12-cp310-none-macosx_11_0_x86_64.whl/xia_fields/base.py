"""Abstract Definition of Fields"""
from __future__ import annotations
from typing import Any
from functools import wraps
from decimal import Decimal
from datetime import datetime, date, time, timezone


def wrap_validation(func):
    @wraps(func)
    def passed_func(*args, **kwargs):
        # We pass the internal value if None
        if args[1] is None:
            return args[1]
        return func(*args, **kwargs)
    return passed_func


def wrap_to_db(func):
    @wraps(func)
    def passed_func(*args, **kwargs):
        # We pass if the input is already in db form
        if args[1] is None:
            return args[1]
        elif (args[0].db_form is not None and isinstance(args[1], args[0].db_form)) and not kwargs.get("encoder", None):
            return args[1]
        return func(*args, **kwargs)
    return passed_func


def wrap_from_db(func):
    @wraps(func)
    def passed_func(*args, **kwargs):
        # we pass if the internal value (first output is in internal form)
        if args[1] is None or (args[0].internal_form is not None and isinstance(args[1], args[0].internal_form)):
            return args[1]
        return func(*args, **kwargs)
    return passed_func


def wrap_to_display(func):
    @wraps(func)
    def passed_func(*args, **kwargs):
        args = args if len(args) == 3 else (args + (None, ))
        # we pass if the display form and detail form are both ok
        display_ok = args[1] is None or (args[0].display_form is not None and isinstance(args[1], args[0].display_form))
        detail_ok = args[0].detail_form is None or isinstance(args[2], args[0].detail_form)
        if display_ok and detail_ok:
            return (args[1], args[2]) if args[0].runtime else args[1]
        result = func(*args, **kwargs)
        return result if not args[0].runtime or isinstance(result, tuple) else (result, None)
    return passed_func


def wrap_from_display(func):
    @wraps(func)
    def passed_func(*args, **kwargs):
        args = args if len(args) == 3 else (args + (None,))
        # We pass if the internal value has been set
        int_ok = args[1] is None or (args[0].internal_form is not None and isinstance(args[1], args[0].internal_form))
        runtime_ok = args[2] is None or (args[0].runtime_form is not None and isinstance(args[2], args[0].runtime_form))
        if int_ok and runtime_ok:
            return (args[1], args[2]) if args[0].runtime else args[1]
        result = func(*args, **kwargs)
        return result if not args[0].runtime or isinstance(result, tuple) else (result, None)
    return passed_func


def wrap_get_value(func):
    @wraps(func)
    def passed_func(*args, **kwargs):
        if not args[0].runtime:
            # Return the same value if runtime is inactive
            return args[1]
        args = args if len(args) == 3 else (args + (None,))
        # we pass if the internal form and runtime form are both ok
        inter_ok = args[1] is None or (args[0].internal_form is not None and isinstance(args[1], args[0].internal_form))
        runtime_ok = args[0].runtime_form is None or isinstance(args[2], args[0].runtime_form)
        if inter_ok and runtime_ok:
            return (args[1], args[2]) if args[0].runtime else args[1]
        result = func(*args, **kwargs)
        return result if not args[0].runtime or isinstance(result, tuple) else (result, None)
    return passed_func


class MetaField(type):
    """Define Meta operation for all simple fields

    """
    pass_dict = {
        "validate": wrap_validation,
        "to_db": wrap_to_db,
        "from_db": wrap_from_db,
        "to_display": wrap_to_display,
        "from_display": wrap_from_display,
        "get_value": wrap_get_value,
    }

    def __new__(mcs, *args, **kwargs):
        if args[0] == "ComplexStringField":
            pass
        for func_name, pass_decorator in mcs.pass_dict.items():
            if func_name in args[2]:
                args[2][func_name] = pass_decorator(args[2][func_name])
        return type.__new__(mcs, *args, **kwargs)


class MetaComplexField(MetaField):
    """Define Meta operation for all complex fields

    """
    def __new__(mcs, *args, **kwargs):
        return type.__new__(mcs, *args, **kwargs)


class BaseField(metaclass=MetaField):
    """Parent of all Field types who have database forms

    Value Forms:
        * Database form: The value store in the engine
        * Internal form: The value presented as python object
        * Runtime form: The value calculated at runtime
        * Display form: The display value map to internal form
        * detail form: The display value map to runtime form
    """

    # Value Forms:
    db_form = None
    internal_form = None
    runtime_form = None
    display_form = None
    detail_form = None

    # Sample dictionary:
    SAMPLE_DICT = {
        int: 0,
        float: 0.0,
        str: "String Value",
        bytes: b"Bytes Value",
        bool: True,
        Decimal: Decimal('0.0'),
        datetime: datetime.now(tz=timezone.utc),
        date: datetime.now(tz=timezone.utc).date(),
        time: datetime.now(tz=timezone.utc).time()
    }

    def __init__(self,
                 required: bool = False,
                 default: Any = None,
                 validation: callable = None,
                 value_min: Any = None,
                 value_max: Any = None,
                 choices: list = None,
                 description: str = None,
                 runtime: bool = False,
                 stateful: bool = True,
                 hidden: bool = False,
                 sample: Any = None,
                 display: dict = None,
                 **kwargs):
        """

        Args:
            required (bool): The field is required
            default (Any): Default value of the field
            validation (callable): A custom validation function
            value_min (Any): Minimum accepted value
            value_max (Any): Maximum accepted value
            choices (list): List of accepted value
            description (str): Description of the field
            runtime (bool): value has runtime form
            stateful (bool): value should be store in the database
            hidden (bool): value shouldn't be shown to the display
            sample (Any): example value of this field (in internal / runtime form)
            display (dict): Define some display related settings (display format, readonly etc...)
        """
        self.runtime = runtime
        self.required = required
        self.default = default
        if validation is not None and not callable(validation):
            raise TypeError("validation must be a validation function")
        self.validation = validation
        self.value_min = self.guess_value(value_min)[0] if runtime else self.guess_value(value_min)
        self.value_max = self.guess_value(value_max)[0] if runtime else self.guess_value(value_max)
        self.choices = [self.guess_value(choice)[0] if runtime else self.guess_value(choice)
                        for choice in choices] if choices else []
        self.stateful = stateful
        self.sample = self.get_sample() if sample is None else sample
        self.hidden = hidden
        self.display = display
        for k, v in kwargs.items():
            if not k.startswith("_"):
                setattr(self, k, v)
        self.description = self._get_description() if description is None else description

    def __getattr__(self, item):
        return None

    def _get_description(self):
        return f"{self.__class__.__name__}"

    def get_sample(self):
        """Get a sample value of a field

        Returns:
            object: sample value
        """
        if self.default is not None:
            return self.default
        if self.choices:
            return self.choices[0]
        return self.SAMPLE_DICT.get(self.internal_form, None)

    def guess_value(self, value: Any = None):
        """Guess field value

        Guess field value is normally called when parsing front. The general rules are:
            * If the fields is type runtime
                * Check if the input is type of runtime or detail form
                * When true, the output guess will be a tuple contain internal form, runtime form
            * Or the check will continue to see if it is display form or db_form
                * When found, it will return internal form
                * When field is runtime type, will return internal from, None (lazy load mode)

        Args:
            value: value to be guessed

        Notes:
            The default priority
        """
        if value is None or isinstance(value, self.internal_form):
            return (value, None) if self.runtime else value
        elif self.runtime and self.runtime_form and isinstance(value, self.runtime_form):
            internal_value = self.from_runtime(value)
            return internal_value, value
        elif self.runtime and self.detail_form and isinstance(value, self.detail_form):
            # if the detail_form and display_form is the same, we could pass the value of both for better guess
            return self.from_display(value, value)
        elif self.display_form and isinstance(value, self.display_form):
            return self.from_display(value) if self.runtime else self.from_display(value)
        elif self.db_form and isinstance(value, self.db_form):
            return (self.from_db(value), None) if self.runtime else self.from_db(value)
        raise TypeError(f"Value {str(value)} couldn't be guessed by using {self.__class__.__name__}'s type list")

    def get_value(self, value: Any = None, runtime_value: Any = None, /, **kwargs):
        """Get runtime value when it is necessary

        Args:
            value (any): value on internal form. could be None for no-stateful fields
            runtime_value (any): value of runtime value. could be None when the data is not loaded
        """
        return value, value

    def validate(self, value: Any, runtime_value: Any = None, /):
        """Validate data

        Args:
            value (any): internal value to be validated
            runtime_value (any): runtime data to be validated

        Notes:
            * No exception raised = validation passed
        """
        if self.validation:
            self.validation(value, runtime_value)
        if self.internal_form is not None and not isinstance(value, self.internal_form) \
                and (self.runtime_form is None or not isinstance(value, self.runtime_form)):
            # Extra check: If the runtime value is ok, we could pass
            raise TypeError(f"{self.__class__.__name__} only accepts {str(self.internal_form)} Type")
        if self.value_min and value < self.value_min:
            raise ValueError(f"Value {value} is less than the minimum value {self.value_min}")
        if self.value_max and value > self.value_max:
            raise ValueError(f"Value {value} is more than the maximum value {self.value_max}")
        if self.choices and value not in self.choices:
            raise ValueError(f"Value {value} is not in the authorized value list")

    def to_db(self, value: Any, runtime_value: Any = None, /,
              catalog: dict = None, encoder: callable = None, ignore_unknown: bool = False, engine=None):
        """Value transformation to database form

        Args:
            encoder (callable): Encode the value
            runtime_value (any): runtime value to be transformed
            value (any): value to be transformed from internal form to database form
            catalog (dict): Data catalog to decide if the field will be shown or not
            ignore_unknown (bool): If the unknown field should be ignored
            engine (BaseEngine): Engine to be passed
        """
        return value if not encoder else encoder(value)

    def from_db(self, value: Any, /, decoder: callable = None, engine=None):
        """Value transformation from database form

        Args:
            decoder (callable): Encode the value
            value (any): value to be transformed from database form to internal form
            engine (BaseEngine): Engine to be passed

        Returns:
            internal value and runtime value tuple
        """
        return value if not decoder else decoder(value)

    def to_display(self, value: Any, runtime_value: Any = None, /, **kwargs):
        """Value transformation to display form

        Args:
            value (any): value to be transformed from internal form to database form
            runtime_value (any): value of runtime value. could be None when the data is not loaded
        """
        return value

    def from_display(self, value: Any, runtime_display: Any = None, /):
        """Value transformation from display form to internal form

        Args:
            value (any): display value to be transformed
            runtime_display (any): display runtime value to be transformed
        """
        return value

    def from_runtime(self, runtime_value: Any, /):
        """Value transformation from runtime value to internal form

        Args:
            runtime_value: runtime value
        """
        return runtime_value


class ComplexField(BaseField, metaclass=MetaComplexField):
    """Complex Field Definition
    """

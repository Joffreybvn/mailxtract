import functools
from dataclasses import dataclass
from typing import Optional, Union, Callable, Any


@dataclass
class FieldContext:
    name: str


def field(
        missing_func: Optional[str] = None,
        args: Optional[dict] = None
):
    """
    Convenient decorator to lazily extract a field once he is requested by the
    user. This decorator is intended to be used with any HTMLExtractor class.

    :param missing_func: The function to execute if the field is missing. This
        function has to return the value of the field, or a dictionary
        containing all the fields to be added.
    :param args: The arguments to pass when missing_func is called.
    """

    # Assign empty dict as default options for the missing_func
    options = args
    if options is None:
        options: dict = {}

    def inner(func):
        @functools.wraps(func)
        def wrapper(self: Union['HTMLExtractor'], *args, **kwargs):

            # Create a field context to be passed to the decorated function.
            # Get the field name from the function name
            field_context = FieldContext(
                name=func.__name__
            )

            # If the data is missing, set it to None by default
            if field_context.name not in self._data:
                field_value = None

                # Run the custom function to retrieve data
                if missing_func:
                    missing_function: Callable = self.__getattribute__(missing_func)
                    field_value: Any = missing_function(**options)

                # Fill the missing field
                if isinstance(field_value, dict):
                    self._data |= field_value
                else:
                    self._data[field_context.name] = field_value

            # Run the decorated function and return the field
            func(self, field_context, *args, **kwargs)
            return self._data[field_context.name]

        return wrapper
    return inner

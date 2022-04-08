import inspect
from functools import wraps
from dataclasses import dataclass
from typing import Optional, Union, Callable, Any


@dataclass
class FieldContext:
    name: str


class _Field(object):
    """
    Field decorator. Lazily extract a field once he is requested by the user.
    This decorator is intended to be used with any HTMLExtractor class.
    """

    def __init__(
            self,
            function: Callable,
            parent: Union['HTMLExtractor'],
            missing_function_name: Optional[str] = None,
            options: Optional[dict] = None
    ):
        """
        :param function: The decorated function.
        :param missing_function_name: The function to execute if the field is missing.
            This function has to return the value of the field, or a dictionary
            containing all the fields to be added.
        :param options: The arguments to pass when missing_func is called.
        """
        self._function: Callable = function  # Decorated method
        self._parent: Union['HTMLExtractor'] = parent  # Method's parent class

        # Metadata
        self._field_name: str = self._function.__name__  # Field name
        self._data = self._parent.data  # Parent's class data storage

        # Function to trigger if the field is missing. Options are arguments
        # passed to this function.
        self._missing_function_name: str = missing_function_name
        self._options: dict = options or {}

    def __get_missing_function(self) -> Optional[Callable]:
        """
        Return the method associated with the given function name in the
        parent class. This method is the one called of the data is missing.
        It should return values that get added to the data dictionary later.
        """
        if self._missing_function_name:
            return self._parent.__getattribute__(self._missing_function_name)
        return None

    def __append_value(self, value: Any) -> None:
        """
        Append the given value to the data dictionary. If the value is a
        dictionary, it will extend the current data. If it's any other thing,
        it get attributed with the field_name as key.
        """
        # Extend the data
        if isinstance(value, dict):
            self._data |= value

        # Attribute with 'field_name' as key
        else:
            self._data[self._field_name] = value

    def __call_decorated_function(self, *args, **kwargs) -> Optional[Any]:
        """
        Call the decorated function. Pass a FieldContext object to it if the
        function has a 'context' parameter. Otherwise, call it without anything.
        """

        # Pass a FieldContext if the function expect a 'context' parameter
        if 'context' in inspect.getfullargspec(self._function).args:
            field_context = FieldContext(
                name=self._field_name
            )
            return self._function(self._parent, *args, context=field_context, **kwargs)

        # Run the function directly without context
        else:
            return self._function(self._parent, *args, **kwargs)

    def __call__(self, *args, **kwargs) -> Optional[Any]:
        """
        Field decorator. Run the 'missing_function' if the data is missing.
        Then run the decorated function, and return the field data.
        """

        # If the data is missing, populate it
        if self._field_name not in self._data:
            field_value = None

            # Use the missing function
            if missing_function := self.__get_missing_function():
                field_value: Any = missing_function(**self._options)

            # Append the data
            self.__append_value(field_value)

        # Call the decorated function and return it's content
        if result := self.__call_decorated_function(*args, **kwargs):
            return result

        # Return the data if the function doesn't return anything
        return self._data[self._field_name]


def field(
        missing_func: Optional[str] = None,
        args: Optional[dict] = None
) -> Callable:
    """Field decorator factory.

    :param missing_func: The function to execute if the field is missing.
        This function has to return the value of the field, or a dictionary
        containing all the fields to be added.
    :param args: The arguments to pass when missing_func is called.
    """
    def inner(func):

        # Set this function as field
        func.__dict__['is_field'] = True

        @wraps(func)
        def wrapper(self, *args_, **kwargs):
            return _Field(
                function=func,
                parent=self,
                missing_function_name=missing_func,
                options=args
            )(*args_, **kwargs)
        return wrapper
    return inner

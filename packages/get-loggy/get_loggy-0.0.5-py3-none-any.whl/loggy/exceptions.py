import functools
from typing import Any, List


class MutuallyExclusiveArgumentsError(Exception):
    """Arguments that are mutually exclusive."""
    def __init__(self, kwarg_names) -> None:
        err = f"These groups or arguments are mutually exclusive: {', '.join(kw for kw in kwarg_names)}"
        super().__init__(err)


def exclusive_args(kwarg_names: List[str]) -> Any:
    """Mutually exclusive argument wrapper.

    Takes a list of arguments then compares them to
    what was passed in.

    Functions can be wrapped multiple times with different
    combinations of mutually exclusive arguments.

    Params:
        kwarg_names (List[str]): List of argument names to use.

    Returns:
        function call

    Raises:
        MutuallyExclusiveArugmentsError: If there are arguments that
            are not allowed to be combined, this will be raised.

    Source:
        https://stackoverflow.com/a/50118390/12387496
    """
    def inner(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            count = 0
            # Iterate kwargs
            for kw in kwargs:
                if kw in kwarg_names and kwargs[kw] is not None:
                    count += 1

            # Raise if not allowed
            if count > 1:
                raise MutuallyExclusiveArgumentsError(kwarg_names)

            # Call wrapped function
            return f(*args, **kwargs)
        return wrapped
    return inner


from functools import wraps
from .logger import log_error
from .screenshot import save_screenshot


def capture_on_failure(func):
    """
    A decorator function to capture and log exceptions raised during the execution 
    of a wrapped function. Additionally, it saves a screenshot for debugging purposes.

    Args:
        func (callable): The function to be wrapped.

    Returns:
        callable: A wrapped function with enhanced error-handling capabilities.

    Behavior:
        - Executes the decorated function.
        - If an exception occurs:
            1. Logs the error with the function name and exception details.
            2. Saves a screenshot associated with the failure.
            3. Reraises the original exception.

    Example:
        @capture_on_failure
        def example_function(self):
            # Function logic here
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            func_name = func.__name__
            save_screenshot(self, func_name)
            raise e
    return wrapper

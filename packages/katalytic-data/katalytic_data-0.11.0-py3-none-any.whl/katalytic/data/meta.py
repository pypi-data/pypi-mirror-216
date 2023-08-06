"""
This module implements meta-programming utilities.
They should be used only when absolutely necessary.
"""
import inspect


def reference_caller_function(*, depth=1):
    """
    Returns a reference to the calling function, based on the specified depth.

    This function inspects the stack frames to retrieve the function that called it.
    The depth parameter specifies how many frames back to look:
        - a depth of 0 will return the function from which the call is made
        - a depth of 1 (the default) will return the immediate caller
        - a depth of 2 will return the caller's caller, and so on

    Parameters:
        depth (int, optional): The number of stack frames back to inspect to find the calling function. (default: 1)

    Returns:
        function: A reference to the function at the specified depth.

    Raises:
        TypeError: If depth is not an integer.
        ValueError: If depth is less than 0 or more than the number of available stack frames.

    Example:
        >>> def foo():
        ...     caller = reference_caller_function()
        ...     print(f'foo() has been called by {caller.__name__}()')
        >>>
        >>> def bar():
        ...     foo()
        >>>
        >>> bar()
        foo() has been called by bar()

    """
    if not isinstance(depth, int) or isinstance(depth, bool):
        raise TypeError(f'depth must be an integer, not {type(depth)}')
    elif depth < 0:
        raise ValueError(f'depth must be >= 0, not {depth}')

    frame = inspect.currentframe().f_back
    try:
        for i in range(depth):
            frame = frame.f_back
    except AttributeError:
        raise ValueError(f'You\'re getting ahead of yourself. There are only {i} frames in the stack.')

    caller = frame.f_code.co_name
    if caller in frame.f_globals:
        return frame.f_globals[caller]
    else:
        for k, obj in frame.f_globals.items():
            if k.startswith('__'):
                continue

            obj_2 = getattr(obj, '__dict__', {})
            if caller in obj_2:
                return obj_2[caller]


def reference_current_function():
    """
    Returns a reference to the current function.
    This is a more explicit version of reference_caller_function(depth=0)

    Returns:
        function: A reference to the current function.

    Example:
        >>> def foo():
        ...     this = reference_current_function()
        ...     print(f'Hello from inside the "{this.__name__}" function')
        >>>
        >>> foo()
        Hello from inside the "foo" function

    """
    # reference_current_function() adds an extra frame to the stack so you should use depth=1
    return reference_caller_function(depth=1)

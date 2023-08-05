import datetime
import os.path
from functools import wraps
from typing import Any, Callable, Union
import traceback

from touchtouch import touch


def break_KeyboardInterrupt(
    f_py: Union[None, Callable] = None,
    v: Any = None,
    active: bool = True,
):
    """
    Decorator that handles the KeyboardInterrupt exception.

    Args:
        f_py (Callable, optional): Function to be decorated. Defaults to None. DON'T PASS ANYTHING HERE - it is reserved for the decorated function!
        v (Any, optional): Value to return when KeyboardInterrupt occurs. Defaults to None.
        active (bool, optional): Flag to determine if the decorator is active or not. Defaults to True.

    Returns:
        Callable: Decorated function.
    """

    assert callable(f_py) or f_py is None

    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except KeyboardInterrupt as e:
                if not active:
                    raise e
                result = v

            return result

        return wrapper

    return _decorator(f_py) if callable(f_py) else _decorator


def ignore_all_exceptions(
    f_py: Union[None, Callable] = None,
    v: Any = None,
    print_exceptions: bool = True,
    active: bool = True,
    logfile: str | None = None,
):
    R"""
    Decorator that ignores all exceptions and handles them based on the specified parameters.

    Args:
        f_py (Callable, optional): Function to be decorated. Defaults to None. DON'T PASS ANYTHING HERE - it is reserved for the decorated function!
        v (Any, optional): Value to return when an exception occurs. Defaults to None.
        print_exceptions (bool, optional): Flag to determine if the exceptions should be printed. Defaults to True.
        active (bool, optional): Flag to determine if the decorator is active or not. Defaults to True.
        logfile (str, optional): Path to the logfile. Defaults to None (logfile will not be written).

    Returns:
        Callable: Decorated function.
    """
    assert callable(f_py) or f_py is None

    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def handle_ex(ex):
                nonlocal result
                if print_exceptions:
                    print(ex)
                if not active:
                    raise ex
                if logfile:
                    _write2logfile(logfile, traceback.format_exc())
                result = v

            result = v
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                handle_ex(e)
            except BaseExceptionGroup as e:
                handle_ex(e)
            except KeyboardInterrupt as e:
                handle_ex(e)
            except SystemExit as e:
                handle_ex(e)
            return result

        return wrapper

    return _decorator(f_py) if callable(f_py) else _decorator


def ignore_Exception(
    f_py: Union[None, Callable] = None,
    v: Any = None,
    print_exceptions: bool = True,
    active: bool = True,
    logfile: str | None = None,
):
    r"""
    Decorator that ignores a specific exception and handles it based on the specified parameters.

    Args:
        f_py (Callable, optional): Function to be decorated. Defaults to None. DON'T PASS ANYTHING HERE - it is reserved for the decorated function!
        v (Any, optional): Value to return when the exception occurs. Defaults to None.
        print_exceptions (bool, optional): Flag to determine if the exception should be printed. Defaults to True.
        active (bool, optional): Flag to determine if the decorator is active or not. Defaults to True.
        logfile (str, optional): Path to the logfile. Defaults to None (logfile will not be written).

    Returns:
        Callable: Decorated function.
    """
    assert callable(f_py) or f_py is None

    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                if print_exceptions:
                    print(e)
                    traceback.print_exc()
                if logfile:
                    _write2logfile(logfile, traceback.format_exc())
                if not active:
                    raise e
                result = v

            return result

        return wrapper

    return _decorator(f_py) if callable(f_py) else _decorator


def _write2logfile(logfile, infos):
    if not os.path.exists(logfile):
        touch(logfile)
    with open(logfile, mode="a", encoding="utf-8") as f:
        f.write(f"\n\n{get_timestamp()}\n{str(infos)}\n---------------------------")


def get_timestamp():
    return datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")

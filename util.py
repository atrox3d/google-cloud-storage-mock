from datetime import datetime
import inspect
from typing import Callable
import logging

logger = logging.getLogger(__name__)
DEBUG = False

def timestamp(format:str='%y/%m/%d %H:%M:%S') -> str:
    return datetime.now().strftime(format)


def printstamp(message:str) -> None:
    # timestamp = datetime.now().strftime('%y/%m/%d %H:%M:%S')
    print(f'{timestamp()} {message}')


def logged(prefix:str=''):
    def decorator(fn:Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                result = fn(*args, **kwargs)
                return result
            finally:
                logger.debug(f'{prefix}{fn.__name__}({args}, {kwargs})')
        return wrapper
    return decorator


def stack_logger(str_message):
    """
    stack info for logging
    """
    f = inspect.currentframe()
    i = inspect.getframeinfo(f.f_back)
    # print(i.code_context)
    # print(i.filename)
    # print(i.index)
    # print(i.lineno)
    return f"[{i.function}] [code line: {str(i.lineno)} ] [ {str_message}]"

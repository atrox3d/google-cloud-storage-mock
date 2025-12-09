from datetime import datetime
import inspect
from typing import Callable, TypeVar
import logging

DEBUG = False
T = TypeVar('T')


def setup_logger(
        name:str, 
        level:int=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(module)10s | %(funcName)15s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        force:bool=True
) -> logging.Logger:
    '''
    Unified source of truth for logging configuration
    '''
    logging.basicConfig(
        format=format,
        datefmt=datefmt,
        level=level,
        force=force
    )
    return logging.getLogger(name)


logger = setup_logger(__name__)

def timestamp(format:str='%y/%m/%d %H:%M:%S') -> str:
    return datetime.now().strftime(format)


def printstamp(message:str) -> None:
    # timestamp = datetime.now().strftime('%y/%m/%d %H:%M:%S')
    print(f'{timestamp()} {message}')


def logged(prefix:str=''):
    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args, **kwargs) -> T:
            try:
                result: T = fn(*args, **kwargs)
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

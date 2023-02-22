from functools import wraps

from loguru import logger


def t(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(
                "Error occurred in module %s while executing the function %s: %s"
                % (func.__module__, func.__name__, e)
            )

    return inner


def at(func):
    @wraps(func)
    async def inner(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(
                "Error occurred in module %s while executing the function %s: %s"
                % (func.__module__, func.__name__, e)
            )

    return inner

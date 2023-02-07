from functools import wraps

from core.constants import ERROR_TEXT_MESSAGE, BotState
from loguru import logger


def t(func, state=BotState.ERROR, text=ERROR_TEXT_MESSAGE):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(
                "Error occurred in module %s while executing the function %s: %s"
                % (func.__module__, func.__name__, e)
            )
            return state

    return inner


def at(func, state=BotState.ERROR, text=ERROR_TEXT_MESSAGE):
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
            return state

    return inner

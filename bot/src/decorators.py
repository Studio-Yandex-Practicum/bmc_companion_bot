import traceback
from functools import wraps

from core.constants import BotState
from handlers.meeting.root_handlers import back_to_start_menu
from loguru import logger


def t(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            logger.error(
                "Error occurred in module %s while executing the function %s: %s"
                % (func.__module__, func.__name__, e)
            )
            return BotState.END

    return inner


def at(func):
    @wraps(func)
    async def inner(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            traceback.print_exc()
            logger.error(
                "Error occurred in module %s while executing the function %s: %s"
                % (func.__module__, func.__name__, e)
            )
            await back_to_start_menu(*args, **kwargs)

            return BotState.STOPPING

    return inner

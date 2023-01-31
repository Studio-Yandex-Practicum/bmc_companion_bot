from telegram.ext import ContextTypes


class BaseContextManager:
    @classmethod
    def set(cls, context: ContextTypes.DEFAULT_TYPE, key, value):
        context.user_data[key] = value

    @classmethod
    def get(cls, context: ContextTypes.DEFAULT_TYPE, key):
        return context.user_data.get(key)

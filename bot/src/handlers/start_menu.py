from core.constants import BotState
from handlers.admin.entrypoint import admin_section
from handlers.base import BaseCommand
from handlers.root_handlers import help_command, start
from telegram.ext import CommandHandler, ConversationHandler


class StartCommand(BaseCommand):
    @classmethod
    def get_handler(cls):
        selection_handlers = [admin_section]

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                BotState.MENU_START_SELECTING_LEVEL: selection_handlers,
            },
            fallbacks=[],
            map_to_parent={},
        )

        return conv_handler


class HelpCommand(BaseCommand):
    @classmethod
    def get_handler(cls):
        return CommandHandler("help", help_command)

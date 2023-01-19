from core.settings import settings
from handlers import register_handlers
from telegram.ext import ApplicationBuilder


def create_app():
    app = ApplicationBuilder().token(settings.BOT_TOKEN).build()

    register_handlers(app)

    return app

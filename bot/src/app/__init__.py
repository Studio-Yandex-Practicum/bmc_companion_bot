from core.settings import BASE_API_URL_V1, settings
from request.base import ApiClient
from services.schedule_service import ScheduleApiService
from services.user_service import UserApiService
from telegram.ext import ApplicationBuilder

api_client_v1 = ApiClient(base_url=BASE_API_URL_V1)
user_service_v1 = UserApiService(api_client=api_client_v1)
schedule_service_v1 = ScheduleApiService(api_client=api_client_v1)


def create_app():
    app = ApplicationBuilder().token(settings.BOT_TOKEN).build()

    register_handlers(app)

    return app


from handlers import register_handlers

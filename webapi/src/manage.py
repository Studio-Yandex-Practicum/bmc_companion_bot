from app import create_app
from app.core.settings import settings

app = create_app()

if __name__ == "__main__":
    app.run(host=settings.APP_HOST, port=settings.APP_PORT)

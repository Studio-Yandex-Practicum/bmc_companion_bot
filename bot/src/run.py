import logging

from app import create_app

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

app = create_app()


if __name__ == "__main__":
    app.run_polling()

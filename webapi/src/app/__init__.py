from app.core.settings import settings
from app.db.pg import db, migrate
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.api import bp as api_bp

    app.register_blueprint(api_bp)

    return app


from app import models

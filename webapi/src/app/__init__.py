from app.core.exceptions import errors
from app.core.settings import settings
from app.db.pg import db, migrate
from flask import Flask
from flask_restful import Api


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app, errors=errors)

    from app.api import bp as api_bp
    from app.api.v1.register_routes import register_routes

    app.register_blueprint(api_bp)
    register_routes(api)

    return app


from app import models

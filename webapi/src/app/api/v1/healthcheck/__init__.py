from flask import Blueprint

bp = Blueprint("healthcheck", __name__, url_prefix="/healthcheck")

from app.api.v1.healthcheck import routes

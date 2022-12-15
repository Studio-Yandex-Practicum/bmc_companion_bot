from app.api.v1.healthcheck import bp as healthcheck_bp
from flask import Blueprint

bp = Blueprint("v1", __name__, url_prefix="/v1")

bp.register_blueprint(healthcheck_bp)

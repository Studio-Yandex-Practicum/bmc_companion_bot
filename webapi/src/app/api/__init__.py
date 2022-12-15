from app.api.v1 import bp as api_v1
from flask import Blueprint

bp = Blueprint("api", __name__, url_prefix="/api")

bp.register_blueprint(api_v1)

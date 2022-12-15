import redis
from app.core.settings import settings

redis_db = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

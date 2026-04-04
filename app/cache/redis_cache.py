import json 
import redis
from app.core.config import settings

redis_client = redis.StrictRedis.from_url(settings.REDIS_URL, decode_response = True)


def get_cached_prediction(key : str):

    value = redis_client.get(key)
    return eval(value) if value else None


def set_cached_prediction(key : str, value : dict,  expiry = 3600):

    redis_client.set(key, str(value))
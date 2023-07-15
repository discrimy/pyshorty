from redis.asyncio import StrictRedis

from pyshorty import settings


def get_redis_connection() -> StrictRedis:
    redis_url = settings.app_settings.REDIS_URL
    db = int(redis_url.path.strip("/"))
    return StrictRedis(
        host=redis_url.host,
        port=redis_url.port,
        db=db,
        password=redis_url.password,
        encoding="utf-8",
        decode_responses=True,
    )

from fastapi import APIRouter, Depends
from redis.asyncio import StrictRedis

from pyshorty.common.redis import get_redis_connection

router = APIRouter()


@router.get("/get/:key")
async def get_by_key(
    key: str, r_con: StrictRedis = Depends(get_redis_connection)
) -> dict:
    value = await r_con.get(key)
    return {"value": value}


@router.post("/set/:key")
async def set_by_key(
    key: str, value: str, r_con: StrictRedis = Depends(get_redis_connection)
) -> dict:
    await r_con.set(key, value)
    return {"status": "ok"}

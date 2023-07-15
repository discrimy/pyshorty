from http import HTTPStatus

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from redis.asyncio.client import StrictRedis
from starlette.requests import Request
from starlette.responses import RedirectResponse, PlainTextResponse

from pyshorty.common.redis import get_redis_connection
from pyshorty.shortlinks import services

router = APIRouter()


@router.post("/", response_class=PlainTextResponse)
async def create_shortlink(
    destination_url: str = Body(
        ...,
        media_type="text/plain",
        pattern=r"^(http|https):\/\/[^\s/$.?#].[^\s]*$",
        examples=["https://google.com"],
    ),
    r_con: StrictRedis = Depends(get_redis_connection),
) -> str:
    short_id = await services.create_shortlink(r_con, destination_url)
    return short_id


@router.get("/{short_id}", response_class=RedirectResponse)
async def redirect_by_short_id(
    short_id: str, r_con: StrictRedis = Depends(get_redis_connection)
) -> RedirectResponse:
    destination_url = await services.get_destination_url_by_short_id(r_con, short_id)
    if not destination_url:
        raise HTTPException(HTTPStatus.NOT_FOUND)
    await services.increase_hits(r_con, short_id)
    return RedirectResponse(destination_url, status_code=HTTPStatus.TEMPORARY_REDIRECT)

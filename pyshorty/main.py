from fastapi import FastAPI

from pyshorty.debug.routes import router as debug_router
from pyshorty.shortlinks.routes import router as shortlinks_router

app = FastAPI()


@app.get("/hello")
async def hello() -> str:
    return "Hello world!"


app.include_router(debug_router, prefix="/debug", tags=["debug"])
app.include_router(shortlinks_router, prefix="", tags=["shortlinks"])

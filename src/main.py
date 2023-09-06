from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.image_reader.router import router_images, router_images_2
from redis import asyncio as aioredis


app = FastAPI(
    title='Images'
)


app.include_router(router_images)
app.include_router(router_images_2)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
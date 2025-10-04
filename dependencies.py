# backend/dependencies.py
from fastapi import Request, Depends
import redis.asyncio as redis

async def get_redis(request: Request) -> redis.Redis:
    return request.app.state.redis
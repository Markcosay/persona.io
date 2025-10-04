# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
from contextlib import asynccontextmanager

from api import video, companions, webrtc, chat
from ws.signaling import router as ws_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = redis.Redis(host="localhost", port=6379, decode_responses=True)
    yield
    await app.state.redis.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video.router, prefix="/api/video")
app.include_router(companions.router, prefix="/api")
app.include_router(webrtc.router, prefix="/api/webrtc")
app.include_router(chat.router, prefix="/api/chat")
app.include_router(ws_router)
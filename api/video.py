# backend/api/video.py
from datetime import datetime, timedelta
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import uuid
import os

from dependencies import get_redis
import redis.asyncio as redis

router = APIRouter()

@router.post("/rooms")
async def create_video_room(redis_client: redis.Redis = Depends(get_redis)):
    room_id = str(uuid.uuid4())
    companion_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    expires_at = (datetime.utcnow() + timedelta(hours=24)).isoformat() + "Z"
    
    room_data = {
        "roomId": room_id,
        "companionId": companion_id,
        "userId": user_id,
        "expiresAt": expires_at,
        "status": "active"
    }
    
    await redis_client.hset(f"room:{room_id}", mapping=room_data)
    await redis_client.expire(f"room:{room_id}", 86400)
    
    return {
        "roomId": room_id,
        "companionId": companion_id,
        "userId": user_id,
        "expiresAt": expires_at
    }

@router.get("/rooms/{room_id}")
async def get_video_room(room_id: str, redis_client: redis.Redis = Depends(get_redis)):
    room_data = await redis_client.hgetall(f"room:{room_id}")
    if not room_data:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return {
        "roomId": room_id,
        "status": room_data.get("status", "active")
    }

@router.post("/recordings")
async def upload_recording(
    file: UploadFile = File(...),
    room_id: str = None,
    redis_client: redis.Redis = Depends(get_redis)
):
    recording_id = str(uuid.uuid4())
    filename = f"recording_{recording_id}_{file.filename}"
    file_path = f"./recordings/{filename}"
    
    os.makedirs("./recordings", exist_ok=True)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    recording_data = {
        "recordingId": recording_id,
        "roomId": room_id or "unknown",
        "url": f"/recordings/{filename}"
    }
    await redis_client.hset(f"recording:{recording_id}", mapping=recording_data)
    
    return {
        "recordingId": recording_id,
        "roomId": room_id or "unknown",
        "url": f"/recordings/{filename}"
    }
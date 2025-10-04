# backend/api/chat.py
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import redis.asyncio as redis

from dependencies import get_redis

class ChatMessage(BaseModel):
    roomId: str
    from_user: str
    text: str
    ts: str

router = APIRouter()

@router.post("/messages")
async def send_chat_message(
    message: ChatMessage,
    redis_client: redis.Redis = Depends(get_redis)
):
    room_exists = await redis_client.exists(f"room:{message.roomId}")
    if not room_exists:
        raise HTTPException(status_code=404, detail="Room not found")
    
    message_id = f"msg:{datetime.utcnow().timestamp()}"
    message_data = {
        "roomId": message.roomId,
        "from": message.from_user,
        "text": message.text,
        "ts": message.ts
    }
    
    await redis_client.hset(f"chat:{message_id}", mapping=message_data)
    await redis_client.lpush(f"room:{message.roomId}:messages", message_id)
    await redis_client.expire(f"chat:{message_id}", 86400)
    
    return {"status": "delivered", "messageId": message_id}
# backend/ws/signaling.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

active_connections = {}

@router.websocket("/signal")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    current_room = None
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                event_type = message.get("type")
                room_id = message.get("roomId")
                
                if not room_id:
                    await websocket.send_text(json.dumps({"error": "roomId required"}))
                    continue
                
                if event_type == "join":
                    current_room = room_id
                    if room_id not in active_connections:
                        active_connections[room_id] = []
                    active_connections[room_id].append(websocket)
                    continue
                
                if current_room != room_id:
                    await websocket.send_text(json.dumps({"error": "Not in room"}))
                    continue
                
                if event_type in ["offer", "answer", "candidate", "leave", "end"]:
                    # Get Redis from app state via WebSocket scope
                    redis_client = websocket.app.state.redis
                    
                    if room_id in active_connections:
                        for connection in active_connections[room_id]:
                            if connection != websocket:
                                try:
                                    await connection.send_text(data)
                                except Exception as e:
                                    logger.error(f"Error sending to connection: {e}")
                    
                    if event_type == "end":
                        await redis_client.delete(f"room:{room_id}")
                        logger.info(f"Room {room_id} ended")
                
                else:
                    await websocket.send_text(json.dumps({"error": "Unknown event type"}))
                    
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"error": "Invalid JSON"}))
                
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
        if current_room and current_room in active_connections:
            active_connections[current_room].remove(websocket)
            if not active_connections[current_room]:
                del active_connections[current_room]
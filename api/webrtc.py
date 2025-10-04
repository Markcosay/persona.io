from fastapi import APIRouter

router = APIRouter()

@router.get("/config")
async def get_webrtc_config():
    """Return WebRTC ICE servers configuration"""
    return {
        "iceServers": [
            {
                "urls": ["stun:stun.l.google.com:19302"]
            },
            {
                "urls": ["turn:global.turn.twilio.com:443?transport=tcp"],
                "username": "TWILIO_USERNAME_PLACEHOLDER",
                "credential": "TWILIO_CREDENTIAL_PLACEHOLDER"
            }
        ]
    }
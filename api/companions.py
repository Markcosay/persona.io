from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter()

@router.get("/companions")
async def get_companions():
    """Proxy to persona fetcher API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://persona-fetcher-api.up.railway.app/personas",
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=502, 
            detail=f"Error fetching companions: {str(e)}"
        )
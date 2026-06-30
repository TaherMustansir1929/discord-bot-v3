from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.giphy import get_random_gif

router = APIRouter(prefix="/giphy", tags=["giphy"])

class GiphyRequest(BaseModel):
    search: str
    rating: str = "g"

@router.post("/")
async def giphy_endpoint(req: GiphyRequest):
    try:
        url = await get_random_gif(req.search, req.rating)
        return {"url": url}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in giphy_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

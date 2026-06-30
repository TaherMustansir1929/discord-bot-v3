from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.waifu import get_waifu_image

router = APIRouter(prefix="/waifu", tags=["waifu"])

class WaifuRequest(BaseModel):
    type: str
    category: str

@router.post("/")
async def waifu_endpoint(req: WaifuRequest):
    try:
        url = await get_waifu_image(req.type, req.category)
        return {"url": url}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in waifu_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.imagine import generate_image

router = APIRouter(prefix="/imagine", tags=["imagine"])

class ImagineRequest(BaseModel):
    prompt: str

@router.post("/")
async def imagine_endpoint(req: ImagineRequest):
    try:
        url = await generate_image(req.prompt)
        return {"url": url}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in imagine_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

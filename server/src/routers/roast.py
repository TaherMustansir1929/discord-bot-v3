import json
from pydantic import BaseModel
from fastapi import APIRouter, Response, HTTPException

from src.agents import roast_agent
from src.utils import get_google_model

router = APIRouter(prefix="/roast", tags=["roast"])

class RoastRequest(BaseModel):
    message: str

@router.post("/")
async def roast(req: RoastRequest):
    print(f"[LOG]: User > {req.message}")
    try:
        model = get_google_model("gemini-3-flash-preview")
        response = await roast_agent(req.message, model)
        print(f"[LOG]: Bot > {response}")
        return Response(
            content=json.dumps({"message": response}),
            status_code=200,
            media_type="application/json",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=json.dumps({"message": str(e)}),
        )

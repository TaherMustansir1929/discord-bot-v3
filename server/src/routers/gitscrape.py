from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.gitscrape import scrape_repositories

router = APIRouter(prefix="/gitscrape", tags=["gitscrape"])

class GitscrapeRequest(BaseModel):
    query: str

@router.post("/")
async def gitscrape_endpoint(req: GitscrapeRequest):
    try:
        repos = await scrape_repositories(req.query)
        return {"repositories": repos}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in gitscrape_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

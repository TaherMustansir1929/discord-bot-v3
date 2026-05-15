from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from src.repo_controller import repo_controller

app = FastAPI()


class RepoScrapeRequest(BaseModel):
    query: str


@app.post("/scrape/repo")
async def scrape_repo(req: RepoScrapeRequest, authorization: str = Header(...)):
    if not authorization.startswith("Bearer"):
        raise HTTPException(detail="[Error]: Invalid authorization", status_code=400)
    token = authorization

    query = req.query

    if not query:
        raise HTTPException(detail="[Error]: Query not provided", status_code=400)

    try:
        result = await repo_controller(query, token)
        return result
    except ValueError as e:
        raise HTTPException(detail=f"[Error]: {str(e)}", status_code=400)
    except Exception as e:
        raise HTTPException(
            detail=f"[Internal Server Error]: {str(e)}", status_code=500
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)

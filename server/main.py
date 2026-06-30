import json
from fastapi import FastAPI, Response

from src.routers.giphy import router as giphy_router
from src.routers.imagine import router as imagine_router
from src.routers.speech import router as speech_router
from src.routers.waifu import router as waifu_router
from src.routers.gitscrape import router as gitscrape_router
from src.routers.roast import router as roast_router


app = FastAPI()

app.include_router(giphy_router)
app.include_router(imagine_router)
app.include_router(speech_router)
app.include_router(waifu_router)
app.include_router(gitscrape_router)
app.include_router(roast_router)


@app.get("/")
async def health_check():
    response = {"message": "[Success]: ZeosSarcasticCat server is running"}
    return Response(
        content=json.dumps(response), status_code=200, media_type="application/json"
    )
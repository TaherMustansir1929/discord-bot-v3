import httpx
from fastapi import HTTPException

CATEGORIES = {
    "sfw": [
        "waifu", "neko", "shinobu", "megumin", "bully", "cuddle",
        "cry", "hug", "kiss", "pat", "smug", "bonk", "blush",
        "smile", "wave", "bite", "glomp", "slap", "dance", "wink",
    ],
    "nsfw": ["waifu", "neko", "trap", "blowjob"],
}

async def get_waifu_image(type: str, category: str) -> str:
    if type not in CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Invalid type ⚠️.\nValid types are: `{', '.join(CATEGORIES.keys())}`")
    if category not in CATEGORIES[type]:
        raise HTTPException(status_code=400, detail=f"Invalid category ⚠️.\nValid categories for {type} are: `{', '.join(CATEGORIES[type])}`")

    url = f"https://api.waifu.pics/{type}/{category}"
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch image from waifu.pics")
            
        data = response.json()
        image_url = data.get("url")
        if not image_url:
            raise HTTPException(status_code=404, detail="No image URL in response")
        return image_url

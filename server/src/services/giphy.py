import os
import random
import httpx
from fastapi import HTTPException

async def get_random_gif(search: str, rating: str) -> str:
    url = "https://api.giphy.com/v1/gifs/search"
    api_key = os.getenv("GIPHY_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GIPHY_API_KEY is not set.")

    LIMIT = 10
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params={
                "api_key": api_key,
                "q": search,
                "limit": LIMIT,
                "rating": rating,
                "remove_low_contrast": False,
            },
        )
        response.raise_for_status()
        
        data = response.json().get("data", [])
        if not data:
            raise HTTPException(status_code=404, detail="No GIF found.")
            
        gifs_len = len(data)
        gif_url = data[random.randint(0, gifs_len - 1)].get("url")
        if not gif_url:
            raise HTTPException(status_code=404, detail="No GIF found.")
            
        return gif_url

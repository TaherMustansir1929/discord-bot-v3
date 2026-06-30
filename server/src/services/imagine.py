import os
import asyncio
import httpx
from fastapi import HTTPException

async def generate_image(prompt: str) -> str:
    bfl_api_key = os.getenv("BFL_API_KEY")
    if not bfl_api_key:
        raise HTTPException(status_code=500, detail="BFL_API_KEY is not set.")

    url = "https://api.bfl.ai/v1/flux-2-pro-preview"
    headers = {
        "accept": "application/json",
        "x-key": bfl_api_key,
        "Content-Type": "application/json",
    }
    payload = {"prompt": prompt, "width": 1440, "height": 2048}

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        polling_url = response.json()["polling_url"]

        while True:
            await asyncio.sleep(0.5)
            poll_response = await client.get(polling_url, headers={"accept": "application/json", "x-key": bfl_api_key})
            poll_response.raise_for_status()
            
            result = poll_response.json()
            status = result["status"]
            if status == "Ready":
                return result["result"]["sample"]
            elif status in ["Error", "Failed"]:
                raise HTTPException(status_code=500, detail="Error generating image")

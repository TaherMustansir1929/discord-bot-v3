import os

import httpx

BASE_URL = os.getenv("ZEOS_SARCASTIC_CAT_URL", "http://localhost:8001")


async def fetch_roast_api(message: str):
    payload = {"message": message}
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=60.0) as client:
        res = await client.post(f"{BASE_URL}/roast", json=payload, headers=headers)
        if res.status_code != 200:
            raise RuntimeError(f"Failed to fetch roast API: {res.status_code}")
        return res.json()

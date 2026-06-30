import os
from typing import Any, Dict

import httpx

BASE_URL = os.getenv("SERVER_URL", "http://localhost:8001")


async def post_to_server(endpoint: str, payload: Dict[str, Any]) -> httpx.Response:
    """
    Sends a POST request to the FastAPI server.
    """
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response


async def get_from_server(endpoint: str, params: Dict[str, Any] | None = None) -> httpx.Response:
    """
    Sends a GET request to the FastAPI server.
    """
    url = f"{BASE_URL}{endpoint}"
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response

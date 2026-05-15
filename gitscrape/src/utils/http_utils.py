import httpx


# === Utitlity fetch function ===
async def fetch_url_httpx(
    client: httpx.AsyncClient, url: str, params: dict | None = None
) -> dict:

    response = await client.get(url, params=params)
    response.raise_for_status()
    return response.json()

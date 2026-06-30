import os
import httpx
from fastapi import HTTPException

BASE_URL = "https://api.github.com/search/repositories"

async def scrape_repositories(query: str) -> list[dict]:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise HTTPException(status_code=500, detail="GITHUB_TOKEN environment variable is not set")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "FastAPI-Server"
    }
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 10,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(BASE_URL, headers=headers, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch from GitHub API")
            
        data = response.json()
        items = data.get("items", [])
        
        repositories = []
        for item in items:
            owner = item.get("owner", {})
            license_data = item.get("license") or {}
            
            repo = {
                "id": item.get("id"),
                "name": item.get("name"),
                "owner": owner.get("login"),
                "owner_avatar": owner.get("avatar_url"),
                "stars": item.get("stargazers_count", 0),
                "forks": item.get("forks_count", 0),
                "watchers": item.get("watchers_count", 0),
                "description": item.get("description") or "No description available",
                "language": item.get("language") or "Unknown",
                "topics": item.get("topics", []),
                "updated_at": item.get("updated_at"),
                "url": item.get("html_url"),
                "license": license_data.get("name", "No license"),
                "has_issues": item.get("has_issues", False),
            }
            repositories.append(repo)
            
        return repositories

import os

import httpx
from discord import Interaction
from dotenv import load_dotenv

from .create_repo_embed import create_repo_embed
from .Repository import Repository

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("[Error]: GITHUB_TOKEN environment variable is not set")


async def gitscrape_handler(interaction: Interaction, query: str):
    await interaction.response.defer()

    BASE_URL = os.getenv("GITSCRAPE_URL", "http://localhost:8000")
    URL = f"{BASE_URL}/scrape/repo"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    body = {"query": query}

    async with httpx.AsyncClient(headers=headers, timeout=60.0) as client:
        response = await client.post(URL, json=body)
        if response.status_code != 200:
            error_data = response.json()
            error_detail = (
                error_data.get("detail", str(error_data))
                if isinstance(error_data, dict)
                else "Unknown API Error"
            )
            return await interaction.followup.send(
                content=f"[Error from API]: {error_detail}"
            )

        top_reranked_repositories = response.json()

    if not top_reranked_repositories:
        return await interaction.followup.send(
            content="[Error]: No repositories found for the given query"
        )

    embeds = []
    for index, repo_dict in enumerate(top_reranked_repositories, start=1):
        repo = Repository(**repo_dict)
        embeds.append(create_repo_embed(repo, index))

    await interaction.followup.send(
        content=f"**GitScrape Results for:** `{query}`", embeds=embeds
    )

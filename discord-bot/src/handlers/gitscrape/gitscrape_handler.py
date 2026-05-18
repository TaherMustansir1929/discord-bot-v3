import os

import httpx
from discord import Interaction
from dotenv import load_dotenv

from .create_repo_embed import create_repo_embed
from .httpx_request import fetch_url_httpx
from .Repository import Repository

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("[Error]: GITHUB_TOKEN environment variable is not set")


async def gitscrape_handler(interaction: Interaction, query: str):
    await interaction.response.defer()

    BASE_URL = "https://api.github.com/search/repositories"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 10,
    }

    top_repositories = await fetch_url_httpx(
        client=httpx.AsyncClient(headers=headers), url=BASE_URL, params=params
    )

    if not top_repositories:
        return await interaction.followup.send(
            content="[Error]: No repositories found for the given query"
        )

    embeds = []
    for index, repo_dict in enumerate(top_repositories, start=1):
        repo = Repository(**repo_dict)
        embeds.append(create_repo_embed(repo, index))

    await interaction.followup.send(
        content=f"**GitScrape Results for:** `{query}`", embeds=embeds
    )

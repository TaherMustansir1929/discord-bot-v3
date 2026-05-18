import os

from discord import Interaction
from dotenv import load_dotenv

from .create_repo_embed import create_repo_embed
from .repo_scraping import scrape_repositories

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("[Error]: GITHUB_TOKEN environment variable is not set")


async def gitscrape_handler(interaction: Interaction, query: str):
    await interaction.response.defer()

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

    top_repositories = await scrape_repositories(query, GITHUB_TOKEN, headers, params)

    if not top_repositories:
        return await interaction.followup.send(
            content="[Error]: No repositories found for the given query"
        )

    embeds = []
    for index, repo in enumerate(top_repositories, start=1):
        embeds.append(create_repo_embed(repo, index))

    await interaction.followup.send(
        content=f"**GitScrape Results for:** `{query}`", embeds=embeds
    )

from discord import Interaction

from src.utils import post_to_server
from .create_repo_embed import create_repo_embed
from .Types import Repository


async def gitscrape_handler(interaction: Interaction, query: str):
    await interaction.response.defer()

    try:
        response = await post_to_server("/gitscrape/", {"query": query})
        data = response.json()
        repos_data = data.get("repositories", [])

        if not repos_data:
            return await interaction.followup.send(
                content="[Error]: No repositories found for the given query"
            )

        embeds = []
        for index, repo_dict in enumerate(repos_data, start=1):
            embeds.append(create_repo_embed(repo_dict, index))

        await interaction.followup.send(
            content=f"**GitScrape Results for:** `{query}`", embeds=embeds
        )
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

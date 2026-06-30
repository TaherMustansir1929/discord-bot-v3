from discord import Interaction

from src.utils import post_to_server


async def giphy_handler(interaction: Interaction, search: str, rating: str):
    await interaction.response.defer()

    try:
        response = await post_to_server("/giphy/", {"search": search, "rating": rating})
        data = response.json()
        await interaction.followup.send(data["url"])
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")
        return

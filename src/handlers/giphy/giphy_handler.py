import os
import random

import requests
from discord import Interaction


async def giphy_handler(interaction: Interaction, search: str, rating: str):
    await interaction.response.defer()

    url = "https://api.giphy.com/v1/gifs/search"
    api_key = os.getenv("GIPHY_API_KEY")
    if not api_key:
        await interaction.followup.send("Something went wrong!")
        raise ValueError("GIPHY_API_KEY is not set.")

    LIMIT: int = 10
    try:
        response = requests.get(
            url,
            params={
                "api_key": api_key,
                "q": search,
                "limit": LIMIT,
                "rating": rating,
                "remove_low_contrast": False,
            },
        )
        response.raise_for_status()

        gifs_len = len(response.json().get("data"))
        gif = response.json().get("data")[random.randint(0, gifs_len)].get("url")
        if not gif:
            await interaction.followup.send("No GIF found.")
            return
        await interaction.followup.send(gif)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")
        return

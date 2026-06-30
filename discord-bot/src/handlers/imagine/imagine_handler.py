from discord import Interaction

from src.utils import post_to_server


async def imagine_handler(interaction: Interaction, prompt: str):
    await interaction.response.defer()

    try:
        response = await post_to_server("/imagine/", {"prompt": prompt})
        data = response.json()
        await interaction.followup.send(data["url"])
    except Exception as e:
        print(f"Error in imagine_handler: {e}")
        await interaction.followup.send(
            "Something went wrong while generating the image!"
        )


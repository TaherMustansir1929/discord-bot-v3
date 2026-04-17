from typing import Literal

from discord import Interaction
from src.handlers.utils import create_discord_file, fetch_and_save_image, fetch_image

CATEGORIES = {
    "sfw": [
        "waifu",
        "neko",
        "shinobu",
        "megumin",
        "bully",
        "cuddle",
        "cry",
        "hug",
        "kiss",
        "pat",
        "smug",
        "bonk",
        "blush",
        "smile",
        "wave",
        "bite",
        "glomp",
        "slap",
        "dance",
        "wink",
    ],
    "nsfw": ["waifu", "neko", "trap", "blowjob"],
}


def validate_category(type: str, category: str):
    if type not in CATEGORIES:
        error_msg = f"Invalid type ⚠️.\nValid types are: `{', '.join(CATEGORIES.keys())}`"
        raise ValueError(error_msg)
    if category not in CATEGORIES[type]:
        error_msg = f"Invalid type ⚠️.\nValid types are: `{', '.join(CATEGORIES[type])}`"
        raise ValueError(error_msg)


def get_categories() -> str:
    msg = f"[SFW Categories] = `{', '.join(CATEGORIES["sfw"])}`\n[NSFW Categories] = `{', '.join(CATEGORIES["nsfw"])}`"
    return msg


async def waifu_handler(interaction: Interaction, type: str, category: str, help: Literal["YES", "NO"]):
    url = f"https://api.waifu.pics/{type}/{category}"
    await interaction.response.defer()

    if help == "YES":
        await interaction.followup.send(get_categories())
        return

    try:
        validate_category(type, category)
    except ValueError as e:
        await interaction.followup.send(str(e))
        return

    try:
        # filepath = await fetch_and_save_image(url, category)
        # file = await create_discord_file(filepath)
        # await interaction.followup.send(file=file)
        image = await fetch_image(url)
        await interaction.followup.send(image)
    except Exception as e:
        await interaction.followup.send(str(e))
        return

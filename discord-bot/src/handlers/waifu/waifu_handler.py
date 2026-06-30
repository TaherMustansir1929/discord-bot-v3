from typing import Literal

from discord import Interaction

from src.utils import post_to_server

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


def get_categories() -> str:
    msg = f"[SFW Categories] = `{', '.join(CATEGORIES['sfw'])}`\n[NSFW Categories] = `{', '.join(CATEGORIES['nsfw'])}`"
    return msg


async def waifu_handler(
    interaction: Interaction, type: str, category: str, help: Literal["YES", "NO"]
):
    await interaction.response.defer()

    if help == "YES":
        await interaction.followup.send(get_categories())
        return

    try:
        response = await post_to_server("/waifu/", {"type": type, "category": category})
        data = response.json()
        await interaction.followup.send(data["url"])
    except Exception as e:
        response = getattr(e, "response", None)
        if response is not None:
            try:
                err_detail = response.json().get("detail", str(e))
                await interaction.followup.send(str(err_detail))
                return
            except ValueError:
                pass
        await interaction.followup.send(f"Error: {str(e)}")
        return


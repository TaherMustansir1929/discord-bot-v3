import discord
from typing import Dict, Any


def create_repo_embed(repo: Dict[str, Any], index: int):

    embed = discord.Embed(
        title=f"{index}. {repo.get('name')}",
        url=repo.get("url"),
        description=(repo.get("description")),
        color=0x5865F2,
    )

    embed.add_field(name="Owner", value=f"*{repo.get('owner')}*", inline=True)

    stars = repo.get('stars', 0)
    embed.add_field(name="Stars", value=f"⭐ {stars:,}", inline=True)

    embed.add_field(name="Language", value=f"**{repo.get('language')}**", inline=True)

    embed.set_footer(text="Powered by Zeoxd's GitScrape")

    owner_avatar = repo.get("owner_avatar")

    if owner_avatar:
        embed.set_thumbnail(url=owner_avatar)

    return embed

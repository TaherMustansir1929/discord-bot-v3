import discord

from .Repository import Repository


def create_repo_embed(repo: Repository, index: int):

    embed = discord.Embed(
        title=f"{index}. {repo.name}",
        url=repo.url,
        description=(repo.description),
        color=0x5865F2,
    )

    embed.add_field(name="Owner", value=f"*{repo.owner}*", inline=True)

    embed.add_field(name="Stars", value=f"⭐ {repo.stars:,}", inline=True)

    embed.add_field(name="Language", value=f"**{repo.language}**", inline=True)

    embed.set_footer(text="Powered by Zeoxd's GitScrape")

    owner_avatar = repo.owner_avatar

    if owner_avatar:
        embed.set_thumbnail(url=owner_avatar)

    return embed

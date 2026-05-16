from discord import Interaction
from discord.ext.commands import Bot
from discord.message import Message

from src.handlers.roast.fetch_response import fetch_roast_api


async def roast_handler(message: Message, bot: Bot):
    if bot.user is None:
        await message.reply("Bot user not found.")
        return
    if not bot.user.mentioned_in(message):
        return

    message.content = message.content.replace(bot.user.mention, "").strip()
    try:
        response = await fetch_roast_api(message.content)
        res_msg = response.get("message")

        if res_msg is None:
            raise RuntimeError("No message in response")

        print(f"Roast response: {res_msg}")
        await message.reply(res_msg)

    except RuntimeError as exc:
        await message.reply(str(exc))
        return


async def roast_handler_appCommand(interaction: Interaction, message: str):
    await interaction.response.defer()

    try:
        response = await fetch_roast_api(message)
        res_msg = response.get("message")

        if res_msg is None:
            raise RuntimeError("No message in response")

        print(f"Roast response: {res_msg}")
        await interaction.followup.send(res_msg)
    except RuntimeError as exc:
        await interaction.followup.send(str(exc))
        return

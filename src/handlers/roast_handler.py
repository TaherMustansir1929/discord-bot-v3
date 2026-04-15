from discord import Interaction
from discord.message import Message
from discord.ext.commands import Bot

from src.agent.agents import roast_agent


async def roast_handler(message: Message, bot: Bot):
    if bot.user is None:
        await message.reply("Bot user not found.")
        return
    if not bot.user.mentioned_in(message):
        return

    message.content = message.content.replace(bot.user.mention, "").strip()
    try:
        response = await roast_agent(message.content)
    except RuntimeError as exc:
        await message.reply(str(exc))
        return

    print(f"Roast response: {response}")
    await message.reply(response)


async def roast_handler_appCommand(interaction: Interaction, message: str):
    await interaction.response.defer()

    try:
        response = await roast_agent(message)
    except RuntimeError as exc:
        await interaction.followup.send(str(exc))
        return

    await interaction.followup.send(response)

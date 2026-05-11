import os
from typing import Literal

import discord
from discord import Interaction, app_commands
from discord.ext import commands
from discord.message import Message
from dotenv import load_dotenv

from src.handlers import (
    giphy_handler,
    gitscrape_handler,
    imagine_handler,
    roast_handler,
    roast_handler_appCommand,
    speech_handler,
    waifu_handler,
)

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

LATEST_UPDATE = "update repo ranking logic"


@bot.event
async def on_ready():
    if not bot.user:
        raise ValueError("Bot user not found.")

    print(f"#- Logged on as {bot.user}!")
    await bot.tree.sync()
    print("i- Slash commands synced.")
    print("#- Connected Guilds:")
    for i, guild in enumerate(bot.guilds):
        print(f"[{i + 1}] {guild.name} (ID: {guild.id})")


@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return

    print(f"Message from {message.author}: {message.content}")
    if "hello" in message.content.lower():
        await message.channel.send("Hello! How can I assist you today?")

    await roast_handler(message=message, bot=bot)
    await bot.process_commands(message)


# ====================
# === PING COMMAND ===
# ====================
@bot.tree.command(name="ping", description="Check the bot's latency.")
@app_commands.choices(
    verbose=[
        app_commands.Choice(name="YES", value="YES"),
    ]
)
async def ping(interaction: Interaction, verbose: str = "NO"):
    latency = round(bot.latency * 1000)  # latency in milliseconds
    print(f"Ping by {interaction.user}. Latency: {latency}ms")
    if verbose == "YES":
        await interaction.response.send_message(
            f"Pong! 🏓 ({latency}ms)\n**Latest Update:** {LATEST_UPDATE}"
        )
    else:
        await interaction.response.send_message(f"Pong! 🏓 ({latency}ms)")


# ===================
# === ZEO COMMAND ===
# ===================
@bot.tree.command(name="zeo", description="Get roasted by Zeo.")
async def zeo(interaction: Interaction, message: str):
    await roast_handler_appCommand(interaction=interaction, message=message)


# =====================
# === WAIFU COMMAND ===
# =====================
@bot.tree.command(name="waifu", description="Get anime waifu images")
@app_commands.choices(
    type=[
        app_commands.Choice(name="SFW", value="sfw"),
        app_commands.Choice(name="NSFW", value="nsfw"),
    ],
    help=[
        app_commands.Choice(name="YES", value="YES"),
        app_commands.Choice(name="NO", value="NO"),
    ],
)
@app_commands.describe(
    type="sfw or nsfw",
    category="keep it blank for default category",
    help="get the list of categories",
)
async def waifu(
    interaction: Interaction,
    type: str = "sfw",
    category: str = "waifu",
    help: Literal["YES", "NO"] = "NO",
):
    await waifu_handler(
        interaction=interaction, type=type, category=category, help=help
    )


# =====================
# === GIPHY COMMAND ===
# =====================
@bot.tree.command(name="giphy", description="Get a random giphy")
@app_commands.choices(
    rating=[
        app_commands.Choice(name="G", value="g"),
        app_commands.Choice(name="PG", value="pg"),
        app_commands.Choice(name="PG-13", value="pg-13"),
        app_commands.Choice(name="R", value="r"),
    ]
)
async def giphy(interaction: Interaction, search: str, rating: str = "g"):
    await giphy_handler(interaction=interaction, search=search, rating=rating)


# =======================
# === IMAGINE COMMAND ===
# =======================
@bot.tree.command(name="imagine", description="Generate an image based on a prompt")
async def imagine(interaction: Interaction, prompt: str):
    await imagine_handler(interaction=interaction, prompt=prompt)


# =======================
# === SPEECH COMMAND ===
# =======================
@bot.tree.command(name="speech", description="tts (text-to-speech)")
@app_commands.choices(
    voice=[
        app_commands.Choice(name="Autumn", value="autumn"),
        app_commands.Choice(name="Diana", value="diana"),
        app_commands.Choice(name="Hannah", value="hannah"),
        app_commands.Choice(name="Austin", value="austin"),
        app_commands.Choice(name="Daniel", value="daniel"),
        app_commands.Choice(name="Troy", value="troy"),
    ]
)
async def speech(interaction: Interaction, prompt: str, voice: str):
    await speech_handler(interaction=interaction, text=prompt, voice=voice)


# =========================
# === GITSCRAPE COMMAND ===
# =========================
@bot.tree.command(name="gitscrape", description="Scrape GitHub repositories")
async def gitscrape(interaction: Interaction, query: str):
    await gitscrape_handler(interaction=interaction, query=query)


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("DISCORD_TOKEN environment variable not set.")
    bot.run(token)

import io

import discord

from src.utils import post_to_server

# ─── 1. Orchestrator ────────────────────────────────────────────────────────


async def speech_handler(
    interaction: discord.Interaction, text: str, voice: str
) -> None:
    await interaction.response.defer()

    try:
        response = await post_to_server("/speech/", {"text": text, "voice": voice})
        audio_bytes = response.read()
        await send_audio_to_discord(interaction, audio_bytes, text)
    except Exception as e:
        await interaction.followup.send(f"❌ Failed to generate audio: {str(e)}")


# ─── 3. Send to Discord ─────────────────────────────────────────────────────


async def send_audio_to_discord(
    interaction: discord.Interaction,
    audio_bytes: bytes,
    text: str,
) -> None:
    buffer = io.BytesIO(audio_bytes)
    buffer.seek(0)  # rewind so discord.py reads from the beginning

    audio_file = discord.File(fp=buffer, filename="audio.wav")

    await interaction.followup.send(
        content=f"**{text}**",
        file=audio_file,
    )

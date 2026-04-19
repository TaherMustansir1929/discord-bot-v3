import io
import os

import discord
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")
client = Groq(api_key=api_key)


# ─── 1. Orchestrator ────────────────────────────────────────────────────────

async def speech_handler(interaction: discord.Interaction, text: str, voice: str) -> None:
    await interaction.response.defer()

    try:
        audio_bytes = generate_audio(text, voice)
        await send_audio_to_discord(interaction, audio_bytes, text)
    except Exception as e:
        await interaction.followup.send(f"❌ Failed to generate audio: {str(e)}")


# ─── 2. Audio generation ────────────────────────────────────────────────────

def generate_audio(text: str, voice: str) -> bytes:
    response = client.audio.speech.create(
        model="canopylabs/orpheus-v1-english",
        voice=voice,
        input=text,
        response_format="wav",
    )

    return response.read()


# ─── 3. Send to Discord ─────────────────────────────────────────────────────

async def send_audio_to_discord(
        interaction: discord.Interaction,
        audio_bytes: bytes,
        text: str,
) -> None:
    buffer = io.BytesIO(audio_bytes)
    buffer.seek(0)  # rewind so discord.py reads from the beginning

    audio_file = discord.File(fp=buffer, filename="audio.mp3")

    await interaction.followup.send(
        content=f"**{text}**",
        file=audio_file,
    )

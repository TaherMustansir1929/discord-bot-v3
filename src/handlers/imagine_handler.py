import os
import requests
import time
from dotenv import load_dotenv

from discord import Interaction

from src.handlers.utils import NOT_FOUND_IMAGE_URL

load_dotenv()


async def imagine_handler(interaction: Interaction, prompt: str):
    await interaction.response.defer()

    bfl_api_key = os.getenv("BFL_API_KEY")
    if not bfl_api_key:
        await interaction.followup.send("Something went wrong!")
        raise ValueError("BFL_API_KEY is not set.")

    try:
        polling_url = await send_image_request(prompt, bfl_api_key)
        image_url = await poll_results(polling_url, bfl_api_key)
        await interaction.followup.send(image_url)
    except Exception as e:
        print(f"Error in imagine_handler: {e}")
        await interaction.followup.send("Something went wrong while generating the image!")


async def send_image_request(prompt: str, bfl_api_key: str) -> str:
    url = "https://api.bfl.ai/v1/flux-2-pro-preview"
    request = requests.post(
        url,
        headers={
            'accept': 'application/json',
            'x-key': bfl_api_key,
            'Content-Type': 'application/json',
        },
        json={
            'prompt': prompt,
            'width': 1440,
            'height': 2048
        },
    ).json()

    polling_url = request["polling_url"]
    print(f"Polling URL: {polling_url}")
    return polling_url


async def poll_results(polling_url: str, bfl_api_key: str) -> str:
    while True:
        time.sleep(0.5)
        result = requests.get(
            polling_url,
            headers={
                'accept': 'application/json',
                'x-key': bfl_api_key,
            },
        ).json()

        status = result["status"]
        if status == "Ready":
            print(f"Image URL: {result['result']['sample']}")
            return result["result"]["sample"]
        elif status in ["Error", "Failed"]:
            print(f"Error generating image")
            return NOT_FOUND_IMAGE_URL

import requests
import os

from discord import File


async def fetch_and_save_image(api_endpoint: str, folder: str) -> str:
    api_response = requests.get(api_endpoint)
    api_response.raise_for_status()

    image_url = api_response.json().get("url")
    if not image_url:
        raise ValueError("No 'url' field found in API response.")

    image_response = requests.get(image_url)
    image_response.raise_for_status()

    filename = image_url.split("/")[-1]  # e.g. "i~RQhRD.png"
    save_dir = f"./public/images/{folder}"
    os.makedirs(save_dir, exist_ok=True)  # create folder if it doesn't exist

    file_path = os.path.join(save_dir, filename)

    with open(file_path, "wb") as f:
        f.write(image_response.content)

    print(f"Image saved to: {file_path}")
    return file_path


async def create_discord_file(file_path: str) -> File:
    with open(file_path, "rb") as image_file:
        discord_file = File(image_file, filename=file_path.split("/")[-1])

    return discord_file

import requests
import os

from discord import File

NOT_FOUND_IMAGE_URL = "https://imgs.search.brave.com/0QkFfmRcEzh3e994MKeo3VGW5DXQM7fmLT0mBa--qoU/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdGF0/aWMudmVjdGVlenku/Y29tL3N5c3RlbS9y/ZXNvdXJjZXMvdGh1/bWJuYWlscy8wMzUv/ODg2LzMzNi9zbWFs/bC9lcnJvci00MDQt/cGFnZS1ub3QtZm91/bmQtd2l0aC1yb2Nr/ZXQtdmVjdG9yLmpw/Zw"


async def fetch_image(api_endpoint: str) -> str:
    response = requests.get(api_endpoint)
    response.raise_for_status()
    image_url = response.json().get("url")

    if image_url is None:
        image_url = NOT_FOUND_IMAGE_URL

    return image_url


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

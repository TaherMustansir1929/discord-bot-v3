import requests

NOT_FOUND_IMAGE_URL = "https://imgs.search.brave.com/0QkFfmRcEzh3e994MKeo3VGW5DXQM7fmLT0mBa--qoU/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdGF0/aWMudmVjdGVlenku/Y29tL3N5c3RlbS9y/ZXNvdXJjZXMvdGh1/bWJuYWlscy8wMzUv/ODg2LzMzNi9zbWFs/bC9lcnJvci00MDQt/cGFnZS1ub3QtZm91/bmQtd2l0aC1yb2Nr/ZXQtdmVjdG9yLmpw/Zw"


async def fetch_image(api_endpoint: str) -> str:
    response = requests.get(api_endpoint)
    response.raise_for_status()
    image_url = response.json().get("url")

    if image_url is None:
        image_url = NOT_FOUND_IMAGE_URL

    return image_url

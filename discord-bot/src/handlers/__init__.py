from .giphy.giphy_handler import giphy_handler
from .gitscrape.gitscrape_handler import gitscrape_handler
from .imagine.imagine_handler import imagine_handler
from .roast.roast_handler import roast_handler, roast_handler_appCommand
from .speech.speech_handler import speech_handler
from .waifu.waifu_handler import waifu_handler

__all__ = [
    "giphy_handler",
    "imagine_handler",
    "roast_handler",
    "roast_handler_appCommand",
    "waifu_handler",
    "speech_handler",
    "gitscrape_handler",
]

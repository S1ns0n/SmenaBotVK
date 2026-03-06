import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
    ADMIN_PEER_ID = os.getenv("ADMIN_PEER_ID")

    BASE_DIR = Path(__file__).parent  # корень проекта
    IMAGES_DIR = BASE_DIR / "bot" / "images"
    START_IMAGE = IMAGES_DIR / "1.png"
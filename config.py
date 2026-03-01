import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
import os
from dotenv import load_dotenv
from pathlib import Path

# =========================
# ENV
# =========================
load_dotenv(Path(__file__).resolve().parent / ".env")

ZIP_CODE = os.getenv("ZIP_CODE")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

DISTANCE = 999999
LIMIT = 100
OFFERED_SINCE_DAYS = 999
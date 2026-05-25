import logging
import json
import requests
from config import BOT_TOKEN, CHAT_ID

logger = logging.getLogger(__name__)

# =========================
# TELEGRAM
# =========================
def format_card(item):

    return f"""
<b>{item.title}</b>

💰 <b>€{item.price}</b>

💬 {item.description}

📍 {item.location.city}

🔗 <a href="{item.link}">Open listing</a>
"""

def build_keyboard(item):

    return {
        "inline_keyboard": [[
            {
                "text": "🔗 Open in Marktplaats",
                "url": item.link
            }
        ]]
    }

def get_image_url(item):

    try:
        images = item.get_images()

        if images:
            return images[0]

    except Exception as e:
        logger.warning(f"Image error: {e}")

    return None

def send_telegram_card(item, message, message_thread_id):

    image_url = get_image_url(item)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    payload = {
        "chat_id": CHAT_ID,
        "caption": message,
        "parse_mode": "HTML",
        "reply_markup": json.dumps(build_keyboard(item))
    }

    if message_thread_id is not None:
        payload["message_thread_id"] = message_thread_id

    if image_url:
        payload["photo"] = image_url

    else:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload["text"] = message
        payload.pop("caption", None)

    try:
        requests.post(url, json=payload, timeout=15)

    except Exception as e:
        logger.error(f"Telegram error: {e}")

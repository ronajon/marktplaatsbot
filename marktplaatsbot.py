import os
import json
import logging
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from logging_config import setup_logging
from telegram import send_telegram_card, format_card
from config import ZIP_CODE, DISTANCE, LIMIT, OFFERED_SINCE_DAYS

from marktplaats import SearchQuery, SortBy, SortOrder, category_from_name


# =========================
# CLI
# =========================
parser = argparse.ArgumentParser()

parser.add_argument(
    "--keywords",
    type=str,
    default="bmw",
    help="Comma-separated keywords (e.g. 'audi,bmw')"
)

parser.add_argument(
    "--categories",
    type=str,
    default="auto-kopen",
    help="Comma-separated categories"
)

parser.add_argument(
    "--message-thread-id",
    type=int,
    default=None,
    help="Telegram topic ID (e.g. 3=oldtimers, 7=electrisch,). Optional."
)

parser.add_argument(
    "--logtoscreen",
    action="store_true",
    help="Enable console logging"
)

parser.add_argument(
    "--logtofile",
    action="store_true",
    help="Enable file logging"
)

parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Run script without sending Telegram message and store results and log to screen."
)

args = parser.parse_args()

KEYWORDS = [k.strip() for k in args.keywords.split(",") if k.strip()] # to search for multiple keywords, separate them with comma
CATEGORIES = [c.strip() for c in args.categories.split(",") if c.strip()] #
SEEN_FILE = "marktplaatsbot_seen.json"
LOG_FILE = "marktplaatsbot.log"
MESSAGE_THREAD_ID = args.message_thread_id
DRY_RUN = False

# =========================
# LOGGING
# =========================
if args.logtoscreen:
    LOG_MODE = "screen"
elif args.logtofile:
    LOG_MODE = "file"
else:
    LOG_MODE = "file"

if args.dry_run:
    DRY_RUN = True
    LOG_MODE = "screen"

handlers = []

if LOG_MODE in ["screen", "both"]:
    handlers.append(logging.StreamHandler())

if LOG_MODE in ["file", "both"]:
    handlers.append(logging.FileHandler(LOG_FILE))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=handlers
)


# =========================
# SEEN SYSTEM
# =========================
def load_seen():
    if os.path.exists(SEEN_FILE):
        return set(json.load(open(SEEN_FILE)))
    return set()

def save_seen(seen):
    json.dump(list(seen), open(SEEN_FILE, "w"))

# =========================
# SEARCH
# =========================
def search():

    results = []

    for cat in CATEGORIES:

        category = category_from_name(cat)

        for kw in KEYWORDS:

            search = SearchQuery(
                query=kw,
                category=category,
                zip_code=ZIP_CODE,
                distance=DISTANCE,
                limit=LIMIT,
                sort_by=SortBy.DATE,
                sort_order=SortOrder.DESC,
                offered_since=datetime.now() - timedelta(days=OFFERED_SINCE_DAYS)
            )

            results.extend(
                search.get_listings()
            )

    return results

# =========================
# MAIN
# =========================
def main():

    logger = setup_logging(args, LOG_FILE)
    logger.info("START: " + str(KEYWORDS))

    seen = load_seen()

    items = search()

    for item in items:

        if item.id in seen:
            continue # skip the rest of the for loop, next item

        if DRY_RUN:
            logger.info(str(item.date) + ": " + str(item.title))
            continue

        seen.add(item.id)

        message = format_card(item)
        send_telegram_card(item, message, MESSAGE_THREAD_ID)

    if not DRY_RUN:
        save_seen(seen)

    logger.info("DONE")

if __name__ == "__main__":
    main()

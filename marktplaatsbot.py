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

KEYWORDS = [k.strip() for k in args.keywords.split(",") if k.strip()]
CATEGORIES = [c.strip() for c in args.categories.split(",") if c.strip()]
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
def seen_file_for_thread(thread_id):
    if thread_id is None:
        return "marktplaatsbot_seen.json"
    return f"marktplaatsbot_seen_topic{thread_id}.json"

def load_seen(thread_id):
    seen_file = seen_file_for_thread(thread_id)
    if os.path.exists(seen_file):
        return set(json.load(open(seen_file)))
    return set()

def save_seen(seen, current_ids, thread_id):
    seen_file = seen_file_for_thread(thread_id)
    pruned = seen & current_ids  # drop IDs no longer in search results
    json.dump(list(pruned), open(seen_file, "w"))


# =========================
# SEARCH
# =========================
def search():

    results = []

    for cat in CATEGORIES:

        category = category_from_name(cat)

        for kw in KEYWORDS:

            query = SearchQuery(
                query=kw,
                category=category,
                zip_code=ZIP_CODE,
                distance=DISTANCE,
                limit=LIMIT,
                sort_by=SortBy.DATE,
                sort_order=SortOrder.DESC,
                offered_since=datetime.now() - timedelta(days=OFFERED_SINCE_DAYS)
            )

            results.extend(query.get_listings())

    return results


# =========================
# MAIN
# =========================
def main():

    logger = setup_logging(args, LOG_FILE)
    logger.info("START: " + str(KEYWORDS))

    seen = load_seen(MESSAGE_THREAD_ID)

    items = search()
    current_ids = {item.id for item in items}

    newitems = 0
    olditems = 0

    for item in items:

        if item.id in seen:
            olditems += 1
            continue

        newitems += 1

        if DRY_RUN:
            logger.info(f"{item.date}: {item.title}")
            continue

        seen.add(item.id)

        message = format_card(item)
        send_telegram_card(item, message, MESSAGE_THREAD_ID)

    if not DRY_RUN:
        save_seen(seen, current_ids, MESSAGE_THREAD_ID)

    logger.info(f"Found {newitems} new items & {olditems} existing items")
    logger.info("DONE")

if __name__ == "__main__":
    main()
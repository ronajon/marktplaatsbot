# 📦 Marktplaats Telegram Bot

A Python automation bot that searches listings on Marktplaats and sends new items directly to a Telegram group or topic.

It supports keyword-based searches, category filtering, and Telegram topic routing (forum threads).

---

## 🚀 Features

- 🔍 Search Marktplaats listings by keywords and categories  
- 📍 Location-based filtering (zip code + distance)  
- ⏱ Filters by recently posted items  
- 📬 Sends formatted listings to Telegram  
- 🧵 Supports Telegram topics (forum threads)  
- 🧠 Prevents duplicate alerts using local seen storage  
- 🪵 Flexible logging (console or file)

---

## 📌 Setup Guide

### 🤖 Create a Telegram Bot

This project uses :contentReference[oaicite:0]{index=0} and requires a bot created via :contentReference[oaicite:1]{index=1}.

1. Open Telegram and search for **@BotFather**
2. Start a chat and run:

```text
/newbot
````

3. Choose:

* Bot name (e.g. Marktplaats Bot)
* Username (must end in `bot`)

4. You will receive a token:

```text
123456789:AAHbCDefGhiJKlmnOPQRsTUVwxyz
```

Save this token.

---

### 🔐 Add Bot to Group

1. Create or open your Telegram group
2. Add your bot
3. Promote it to admin

   * Allow sending messages

---

### 🧵 Enable Topics (Forum Mode)

1. Open group
2. Tap group name → Edit
3. Enable Topics / Forum Mode

---

### Create Topics

Example topics:

* Oldtimers
* Electrisch
* Accessories

Each topic has a `message_thread_id`.

---

## ⚙️ Command Line Arguments

The bot uses `argparse`.

| Argument              | Type   | Description                             | Default      |
| --------------------- | ------ | ----------------------------            | ------------ |
| `--keywords`          | string | Comma-separated keywords                | `bmw`        |
| `--categories`        | string | Comma-separated categories              | `auto-kopen` |
| `--message-thread-id` | int    | Telegram topic ID (optional)            | `None`       |
| `--logtoscreen`       | flag   | Enable console logging                  | `False`      |
| `--logtofile`         | flag   | Enable file logging                     | `True`       |
| `--dry-run`           | flag   | Test without sending telegram messages  | `False`      |

---

### 🔍 Example usage

```bash
python main.py \
  --keywords "bmw,audi" \
  --categories "auto-kopen,motoren" \
  --message-thread-id 3 \
  --logtoscreen
```

---

## 🧵 Telegram Routing

* `chat_id` → Telegram group
* `message_thread_id` → topic (optional)

| Topic       | ID               |
| ----------- | ---------------- |
| General     | (default / None) |
| Oldtimers   | 3                |
| Electrisch  | 7                |
| Accessories | 9                |

If omitted → messages go to general topic.

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

```python
ZIP_CODE = "1000AA"
DISTANCE = 50
LIMIT = 25
OFFERED_SINCE_DAYS = 2
```

---

## 🧪 Run

```bash
python main.py
```

---

## 🧠 How it works

1. Parse CLI arguments
2. Load seen items (`marktplaatsbot_seen.json`)
3. Search Marktplaats listings
4. Filter duplicates
5. Format Telegram card
6. Send to Telegram
7. Save seen IDs

---

## 🧠 Duplicate prevention

Seen items stored in:

```text
marktplaatsbot_seen.json
```

---

## 🪵 Logging

Console:

```bash
--logtoscreen
```

File logging (default):

```text
marktplaatsbot.log
```

---

## ⚠️ Notes

* Requires Telegram bot token
* Bot must be added to group
* To find message-thread-id
  * In Telegram app find Topic
  * Click on topic title
  * With hamburger menu, view topic info 
  * message-thread-id is **xyz** part of t.me/c/123456/**xyz**
* Topics are optional
* Without `--message-thread-id`, messages go to general chat

---

## 📜 License

MIT
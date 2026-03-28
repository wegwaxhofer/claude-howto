#!/usr/bin/env python3
import os
import logging
from dotenv import load_dotenv
from anthropic import Anthropic
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ALLOWED_USER_ID = os.getenv("ALLOWED_USER_ID", "").strip()

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

client = Anthropic(api_key=ANTHROPIC_API_KEY)
conversations: dict[int, list] = {}

SYSTEM_PROMPT = """Du bist Orion, Martins persönlicher KI-Assistent.

## Kontext
- Martin ist Selfmade-Unternehmer und Technik-Enthusiast mit einem Proxmox-Homelab
- Er betreibt mehrere Dienste: Home Assistant, n8n, Nextcloud, XWiki, Immich, Unifi
- Er arbeitet an OpenClaw, einer multi-agenten KI-Automatisierungsplattform
- Anrede: "Chef"

## Verhalten
- Direkt, technisch präzise, kein Overhead
- Deutsch, außer Martin schreibt Englisch
- Meinungen haben, widersprechen wenn sinnvoll
- Keine Floskeln wie "Natürlich!" oder "Gerne!"
- Kurze, klare Antworten bevorzugt

## Fähigkeiten
- Allgemeine Fragen beantworten
- Technische Probleme analysieren
- Pläne und Entscheidungen durchdenken
- Code schreiben und erklären
"""

def load_context_from_nextcloud() -> str:
    """Lädt zusätzlichen Context aus Nextcloud wenn verfügbar."""
    try:
        import requests
        nc_url = os.getenv("NEXTCLOUD_URL", "http://192.168.1.225")
        nc_user = os.getenv("NEXTCLOUD_USER", "")
        nc_pass = os.getenv("NEXTCLOUD_PASS", "")
        if not nc_user or not nc_pass:
            return ""
        context_parts = []
        base_path = f"{nc_url}/remote.php/dav/files/{nc_user}/Obsidian/Claude/Context"
        resp = requests.request("PROPFIND", base_path, auth=(nc_user, nc_pass), timeout=5,
                                headers={"Depth": "1"})
        if resp.status_code == 207:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(resp.text)
            for response in root.findall(".//{DAV:}response"):
                href = response.find("{DAV:}href")
                if href is not None and href.text.endswith(".md"):
                    file_url = f"{nc_url}{href.text}"
                    file_resp = requests.get(file_url, auth=(nc_user, nc_pass), timeout=5)
                    if file_resp.status_code == 200:
                        context_parts.append(file_resp.text)
        return "\n\n".join(context_parts)
    except Exception:
        return ""

def get_system_prompt() -> str:
    extra = load_context_from_nextcloud()
    if extra:
        return SYSTEM_PROMPT + "\n\n## Zusätzlicher Kontext\n" + extra
    return SYSTEM_PROMPT

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    conversations[chat_id] = []
    await update.message.reply_text("Orion online. Was liegt an, Chef?")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    conversations[chat_id] = []
    await update.message.reply_text("Konversation zurückgesetzt.")

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Deine Telegram User ID: `{update.effective_user.id}`",
                                     parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if ALLOWED_USER_ID and str(user_id) != ALLOWED_USER_ID:
        await update.message.reply_text("Kein Zugriff.")
        return

    if chat_id not in conversations:
        conversations[chat_id] = []

    user_text = update.message.text
    conversations[chat_id].append({"role": "user", "content": user_text})

    # Max 20 Nachrichten im Verlauf behalten
    if len(conversations[chat_id]) > 20:
        conversations[chat_id] = conversations[chat_id][-20:]

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            system=get_system_prompt(),
            messages=conversations[chat_id],
        )
        assistant_text = response.content[0].text
        conversations[chat_id].append({"role": "assistant", "content": assistant_text})
        await update.message.reply_text(assistant_text)
    except Exception as e:
        logger.error(f"Claude API Fehler: {e}")
        await update.message.reply_text(f"Fehler: {e}")

def main() -> None:
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN nicht gesetzt")
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY nicht gesetzt")

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Orion Telegram Bot gestartet")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

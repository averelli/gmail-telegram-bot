import json
import logging

from telegram import Update
from telegram.ext import Application, ConversationHandler, ContextTypes

from config import QUERIES_PATH, BOT_TOKEN

logger = logging.getLogger("email-telegram-bot")

def get_bot() -> Application:
    return Application.builder().token(BOT_TOKEN).build()


def load_queries() -> list:
    try:
        with open(QUERIES_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.info("Queries file does not exist, creating empty.")
        with open(QUERIES_PATH, "w") as f:
            json.dump([], f)
            return []
    except Exception as e:
        logger.error(f"Error while loading queries: {e}", exc_info=True)
        raise
    

def save_queries(queries:list):
    try:
        with open(QUERIES_PATH, "w") as f:
            json.dump(queries, f, indent=2)
    except Exception as e:
        logger.error(f"Error while saving queries: {e}", exc_info=True)
        raise


async def cancel_fallback(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await upd.message.reply_text("Operation cancelled")
    logger.info("Operation cancelled with /cancel")
    return ConversationHandler.END
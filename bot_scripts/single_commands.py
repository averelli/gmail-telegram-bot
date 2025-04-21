from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from .bot_utils import save_queries, load_queries, cancel_fallback
from config.config import set_chat_id
import logging

logger = logging.getLogger("email-telegram-bot")

async def start(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """First command, updates the chat id inside the cofig.json"""
    logger.info("Start command called, setting chat id")
    chat_id = upd.effective_chat.id
    set_chat_id(chat_id)
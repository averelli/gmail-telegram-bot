import logging

from telegram import Update
from telegram.ext import Application, ConversationHandler, ContextTypes

from config import BOT_TOKEN

logger = logging.getLogger("email-telegram-bot")

def get_bot() -> Application:
    return Application.builder().token(BOT_TOKEN).build()


async def cancel_fallback(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await upd.message.reply_text("Operation cancelled")
    logger.info("Operation cancelled with /cancel")
    return ConversationHandler.END
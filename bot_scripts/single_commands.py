import logging

from telegram import Update
from telegram.ext import ContextTypes

from utils import load_queries
from config import set_chat_id

logger = logging.getLogger("email-telegram-bot")

async def refresh(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Updates the chat id inside the cofig.json."""
    logger.info("Start command called, setting chat id")
    chat_id = upd.effective_chat.id
    set_chat_id(chat_id)


async def list(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """List all the existing queries."""
    logger.info("User called /list")
    try:
        queries = load_queries()

        if len(queries) == 0:
            logger.info("No queries in the file")
            await upd.message.reply_text("There are no queires saved")
            return 

        lines = [f"{query["id"]}: `{query["full_query"]}`" for query in queries]
        message = " \n".join(lines)

        await upd.message.reply_markdown(message)
    except Exception as e:
        logger.error(f"Error during /list command: {e}", exc_info=True)
        await upd.message.reply_text("Something went wrong")
        raise

async def help(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    logger.info("User called /help command")

    message = """
    Use these commands to interact with the bot:
    - /refresh to update the chat id in the config.
    - /list to see all the existing queries.
    - /add to add a new query
    - /del to delete one of the queries
    """
    await upd.message.reply_text(message)
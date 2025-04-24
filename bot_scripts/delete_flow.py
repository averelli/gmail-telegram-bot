import logging

from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

from .bot_utils import cancel_fallback
from utils import save_queries, load_queries

DEL_CHOOSE, = range(1)
logger = logging.getLogger("email-telegram-bot")

async def del_start(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    logger.info("Entered /del_start flow")

    try:
        queries = load_queries()

        if len(queries) == 0:
            logger.info("No queries to delete")
            await upd.message.reply_text("There are no queires to delete")
            return ConversationHandler.END

        lines = [f"{query["id"]}: `{query["full_query"]}`" for query in queries]
        message = " \n".join(lines)

        await upd.message.reply_text("Choose which query to delete:")
        await upd.message.reply_markdown(message)

        return DEL_CHOOSE
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise


async def del_choose(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    del_id = int(upd.message.text.strip())
    logger.info(f"Deleting query id: {del_id}")

    try:
        updated_queries = [query for query in load_queries() if query["id"] != del_id]
        save_queries(updated_queries)
        logger.info("Queries updated")
        await upd.message.reply_text("Query deleted successfully!")
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error while deleting a query [id: {del_id}]: {e}", exc_info=True)
        raise


def build_delete_handler():
    return ConversationHandler(
        entry_points= [CommandHandler("del", del_start)],
        states= {
            DEL_CHOOSE: [MessageHandler(filters.Regex("[0-9]+"), del_choose)], 
        },
        fallbacks= [CommandHandler("cancel", cancel_fallback)],
        name="del_flow"
    )
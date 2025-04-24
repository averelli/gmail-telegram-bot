import logging
from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from .bot_utils import save_queries, load_queries, cancel_fallback

# State constants
ADD_EMAIL, ADD_KEYWORDS, ADD_MSG, ADD_CONFIRM = range(4)

logger = logging.getLogger("email-telegram-bot")

async def add_start(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    logger.info("Entered /add_start flow.")
    await upd.message.reply_text("Add email address to follow")
    return ADD_EMAIL


async def add_email(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    email = upd.message.text.strip()
    logger.info(f"User provided an email address")
    ctx.user_data["email"] = email
    await upd.message.reply_text("Add keywords to look for (space separated)")
    return ADD_KEYWORDS


async def add_keywords(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    keywords = upd.message.text.strip().split()
    logger.info("User provided keywords")
    ctx.user_data["keywords"] = keywords
    await upd.message.reply_text("Add custom notification text")
    return ADD_MSG


async def add_msg(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    notif_msg = upd.message.text.strip()
    logger.info("User provided a notif message")
    ctx.user_data["notif_msg"] = notif_msg
    preview = (
        f"Preview:\n"
        f"`from:{ctx.user_data["email"]} {" ".join(ctx.user_data["keywords"])} is:unread`\n\n"
        f"Message: {notif_msg}\n\n"
        "Type *yes* to save or *no* to cancel."
    )
    await upd.message.reply_markdown(preview)
    return ADD_CONFIRM


async def add_confirm(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    answer = upd.message.text.strip().lower()
    if answer in ("yes", "y"):
        queries = load_queries()
        new_id = max([q["id"] for q in queries]) + 1
        queries.append({
            "id": new_id,
            "email": ctx.user_data["email"],
            "keywords": ctx.user_data["keywords"],
            "notif_msg": ctx.user_data["notif_msg"],
            "full_query": f"from:{ctx.user_data["email"]} {" ".join(ctx.user_data["keywords"])} is:unread"
        })
        save_queries(queries)
        await upd.message.reply_text("Saved!")
        logger.info(f"Query [id: {new_id}] is saved")
    else:
        await upd.message.reply_text("Cancelled!")
        logger.info("User cancelled operation")
    
    return ConversationHandler.END


def build_add_handler():
    return ConversationHandler(
        entry_points = [CommandHandler("add", add_start)],
        states = {
            ADD_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_email)],
            ADD_KEYWORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_keywords)],
            ADD_MSG: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_msg)],
            ADD_CONFIRM: [MessageHandler(filters.Regex("^(yes|y|no|n)$"), add_confirm)],
        },
        fallbacks = [CommandHandler("cancel", cancel_fallback)],
        name = "add_flow"
    )
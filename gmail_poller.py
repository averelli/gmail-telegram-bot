import logging

from telegram.ext import ContextTypes

from utils import load_queries, update_processed_messages
from config import get_chat_id
from gmail_service import GmailService

logger = logging.getLogger("email-telegram-bot")

async def gmail_poller(ctx: ContextTypes.DEFAULT_TYPE):
    logger.info("Starting Gmail poller")
    gs = GmailService(logger)
    chat_id = get_chat_id()

    queries = load_queries()
    if queries:
        logger.info(f"Loaded {len(queries)} queries")
    else:
        logger.info("No queries to use")
        return

    try:
        for q in queries:
            query_id = q["id"]
            logger.info(f"[Query id: {query_id}] Started processing query")
            # get all unread messages
            messages = gs.fetch_emails(query_id=query_id, query=q["full_query"])
            
            if messages:
                # filter out already processed messages
                msg_ids = [msg["id"] for msg in messages if msg["id"] not in q["processed_messages"]]
                for msg_id in msg_ids:
                    logger.info(f"[msg id: {msg_id}] Notifying about the message")
                    # get the subject line
                    subject_line = gs.extract_subject(msg_id)
                    message = q["notif_msg"] + "\n" + subject_line
                    # send the notification
                    await ctx.bot.send_message(chat_id, message)
                    # add the message to the processed messaged list
                    update_processed_messages(query_id, msg_id)
            else:
                continue
    except Exception as e:
        logger.error(f"Error while processing queries: {e}", exc_info=True)
        await ctx.bot.send_message(chat_id, "Error occured while processing queries")
    
    logger.info("Gmail poller finished")
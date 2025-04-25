from bot import build_bot_app
from config import POLL_INTERVAL, setup_logging
from gmail_poller import gmail_poller

logger = setup_logging()

def main():
    logger.info("Starting the bot")
    bot = build_bot_app()
    bot.job_queue.run_repeating(callback=gmail_poller, interval=POLL_INTERVAL, first=1)
    bot.run_polling()
    logger.info("Bot stopped")

if __name__ == "__main__":
    main()
from telegram.ext import CommandHandler, Application
import bot_scripts as scripts
from config import setup_logging

def build_bot_app() -> Application:
    """Adds bot handlers and returns the app"""
    bot = scripts.get_bot()

    bot.add_handler(scripts.build_add_handler())
    bot.add_handler(scripts.build_delete_handler())
    bot.add_handler(CommandHandler("refresh", scripts.refresh))
    bot.add_handler(CommandHandler("list", scripts.list))
    bot.add_handler(CommandHandler("help", scripts.help))

    return bot

if __name__ == "__main__":
    logger = setup_logging()
    bot = build_bot_app()
    logger.info("Running just the bot")
    bot.run_polling()
    logger.info("Bot stopped")
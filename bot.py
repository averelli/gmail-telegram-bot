from telegram.ext import Application, CommandHandler
import bot_scripts as scripts
from config.config import BOT_TOKEN
from config.logging_config import setup_logging

logger = setup_logging()

bot = Application.builder().token(BOT_TOKEN).build()

bot.add_handler(scripts.build_add_handler())
bot.add_handler(scripts.build_delete_handler())
bot.add_handler(CommandHandler("start", scripts.start))

bot.run_polling()
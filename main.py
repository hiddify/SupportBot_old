import logging
from dotenv import load_dotenv
import utils.set_env
from telegram_bot import telegram_bot

# Load environment variables from .env file
load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
telebot.logger.setLevel(logging.INFO)  # Outputs debug messages to console.
logger = telebot.logger

# Run telegram bot
telegram_bot.init()

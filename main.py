from dotenv import load_dotenv
import utils.set_env
from telegram_bot import telegram_bot

# Load environment variables from .env file
load_dotenv()

# Run telegram bot
telegram_bot.init()

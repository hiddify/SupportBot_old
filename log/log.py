# log/log

import logging
import traceback

# Set up logging
logging.basicConfig(filename='bot.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to log errors
def log_error(error):
    error_info = traceback.format_exc()
    logging.error(error_info)
    # logging.error(error)

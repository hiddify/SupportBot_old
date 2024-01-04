# telegram_bot/telegram_bot

import os
import logging
from log import log
import paramiko
import asyncio
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import asyncio_filters
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ForceReply, ReplyKeyboardRemove, Message
from telebot.asyncio_storage import StateMemoryStorage
from messages.common_messages import CommonMessages

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
telebot.logger.setLevel(logging.INFO)  # Outputs debug messages to console.
logger = telebot.logger

# Set env variables
SSH_HOST = os.environ.get('SSH_HOST')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Init storage
state_storage = StateMemoryStorage()
private_key_path = "/root/hiddifysupport/assets/hiddify_support.key"
with open("/root/hiddifysupport/assets/hiddify_support.key.pub", 'r') as file:
    public_key = file.read()

# Exception handler
class ExceptionHandler(telebot.ExceptionHandler):
    def handle(self, exception):
        # Raise error
        logger.error(exception)

# Custom class that representing states for a conversation
class MyStates(StatesGroup):
    SSH_info = State()
    SSH_info_comment = State()
    SSH_info_from_support = State()
    Feedback = State()
    Support = State()
    INIT = State()
    CONTRIBUTE = State()
    INSTALL = State()

# Create a new bot object
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN, state_storage=state_storage, parse_mode="markdown", exception_handler=ExceptionHandler())

# Any state
@bot.message_handler(state="*", commands=['cancel'])
async def any_state(message):
    """
    Handles the cancellation of the current state
    """
    await bot.send_message(message.chat.id, "Canceled! Returning to main menu")
    await bot.delete_state(message.from_user.id, message.chat.id)
    await send_welcome(message)

@bot.message_handler(state=MyStates.CONTRIBUTE, func=lambda message: "/start contribute" not in message.text)
async def contribute_comment(message):
    """
    Handles user-contributed comments
    """
    msgtxt = f'''
`{message.from_user.id} {message.chat.id}` 
[{message.from_user.first_name or ""} {message.from_user.last_name or ""}](tg://user?id={message.from_user.id}) [user:](@{message.from_user.username})  in {message.chat.title}

{message.text}
    '''

    new_message = await bot.send_message(-1001834220158, msgtxt, parse_mode='markdown')
    await bot.send_message(message.chat.id, CommonMessages.THANKS_FOR_YOUR_MESSAGE)
    await bot.set_state(message.from_user.id, MyStates.start, message.chat.id)

@bot.message_handler(commands=['start'], func=lambda message: "contribute" in message.text)
async def send_contribute(message):
    """
    Handles the '/start' command with a request to contribute
    """
    print('state', MyStates.SSH_info, message)
    print(message.from_user.id, message.chat.id, type(message.from_user.id), type(message.chat.id))

    await bot.reply_to(message, CommonMessages.THANKS_FOR_CONTRIBUTING_REQUEST, reply_markup=None,)
    await bot.set_state(message.from_user.id, MyStates.CONTRIBUTE, message.chat.id)    

@bot.message_handler(state=MyStates.INSTALL, func=lambda message: "/start" not in message.text)
async def contribute_comment(message):
    """
    Handles user-contributed comments during the INSTALL state
    """
    msgtxt = f'''
`{message.from_user.id} {message.chat.id}` 
[{message.from_user.first_name or ""} {message.from_user.last_name or ""}](tg://user?id={message.from_user.id}) [user:](@{message.from_user.username})  in {message.chat.title}

{message.text}
    '''

    new_message = await bot.send_message(-1001834220158, msgtxt, parse_mode='markdown')
    await bot.send_message(message.chat.id, CommonMessages.THANKS_FOR_YOUR_MESSAGE)
    await bot.set_state(message.from_user.id, MyStates.start, message.chat.id)

@bot.message_handler(commands=['start'], func=lambda message: "install" in message.text)
async def send_contribute(message):
    """
    Handles the '/start' command with a request to install
    """
    print('state', MyStates.SSH_info, message)
    print(message.from_user.id, message.chat.id, type(message.from_user.id), type(message.chat.id))

    await bot.reply_to(message, CommonMessages.ABOUT_HIDDIFY, reply_markup=None, disable_web_page_preview=True)
    await bot.set_state(message.from_user.id, MyStates.INSTALL, message.chat.id)

@bot.message_handler(func=lambda msg: msg.text == "Critical Bug")
async def ssh(message):
    """
    Handles the detection of a critical bug and initiates SSH information collection
    """
    markup = ForceReply(selective=False)
    await bot.send_message(message.chat.id, CommonMessages.CRITICAL_ERROR)
    await bot.send_message(message.chat.id, CommonMessages.SEND_SSH_INFORMATION.replace('@PUBLIC_KEY', public_key))
    await bot.send_message(message.chat.id, CommonMessages.SEND_SSH_INSTRUCTIONS, reply_markup=markup)
    await bot.set_state(message.from_user.id, MyStates.SSH_info, message.chat.id)

def get_ssh_info(txt):
    """
    Extracts SSH information from the given text
    """
    import re
    pattern = r'^(?:ssh\s+)?(?:(?P<user>\w+)@(?P<host>[^\s@]+))?(?:\s+-p\s+(?P<port>\d+))?\s*$'
    match = re.match(pattern, txt)

    if match:
        groups = match.groupdict()
        try:
            port = int(groups.get('port', '22'))
        except:
            port = 22
        return {'user': groups['user'], 'host': groups['host'], 'port': port}
    return None

async def test_ssh_connection(ssh_info):
    """
    Tests the SSH connection using the provided SSH information
    """
    if not ssh_info:
        return False

    print("Test starting...")
    try:
        # Creating a Paramiko SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connecting to the SSH server
        ssh_client.connect(hostname=ssh_info['host'],
                           port=ssh_info['port'],
                           username=ssh_info['user'],
                           key_filename=private_key_path,
                           timeout=2)

        # Running the command
        stdin, stdout, stderr = ssh_client.exec_command("pip3 freeze | grep hiddifypanel | awk -F ' == ' '{ print $2 }'")
        result = stdout.read().decode() + stderr.read().decode()

        print("Test was successful!")
        return f'"{result}"'

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        # Closing the SSH connection
        ssh_client.close()

@bot.message_handler(state=MyStates.SSH_info)
async def ssh_received(message):
    """
    Processes and tests SSH information received from the user
    """
    ssh_info = get_ssh_info(message.text)
    panel_version = await test_ssh_connection(ssh_info)
    if not panel_version:
        print("We can not connect to your server.")
        await bot.send_message(message.chat.id, CommonMessages.CANNOT_CONNECT_TO_YOUR_SERVER)
        await asyncio.sleep(1)
        return await ssh(message)

    await bot.send_message(message.chat.id, CommonMessages.SSH_INFO_IS_OK.replace('@PANEL_VERSION', panel_version))
    await bot.set_state(message.from_user.id, MyStates.SSH_info_comment, message.chat.id)

    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['SSH_info'] = ssh_info
        data['panel_version'] = panel_version

@bot.message_handler(state=MyStates.SSH_info_comment)
async def ssh_received_comment(message):
    """
    Processes received SSH-related messages
    """
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        ssh_info = data['SSH_info']
        panel_version = data['panel_version']
        msgtxt = f'''
`{message.from_user.id}` `{message.chat.id}` `DN={'support_message' in data}`
[{message.from_user.first_name or ""} {message.from_user.last_name or ""}](tg://user?id={message.from_user.id}) [user:](@{message.from_user.username})  in {message.chat.title}
{panel_version}
`ssh {ssh_info['user']}@{ssh_info['host']} -p {ssh_info['port']}`
[SSH Site](https://{SSH_HOST}/?host={ssh_info['host']}&port={ssh_info['port']}&user={ssh_info['user']}&password=support)

{message.text}
        '''

        new_message = await bot.send_message(-1001834220158, msgtxt, parse_mode='markdown')
        data['SSH_info_comment'] = message

    await bot.send_message(message.chat.id, CommonMessages.THANKS_FOR_YOUR_MESSAGE)
    await bot.send_message(message.chat.id, CommonMessages.SEND_SSH_INFORMATION.replace('@PUBLIC_KEY', public_key))
    await send_welcome(message)

@bot.message_handler(func=lambda msg: msg.text == "Feedback")
async def feedback(message):
    """
    Receive the user feedback
    """
    await bot.send_message(message.chat.id, CommonMessages.SEND_FEEDBACK)
    await bot.set_state(message.from_user.id, MyStates.Feedback, message.chat.id)

@bot.message_handler(state=MyStates.Feedback)
async def feedback_received(message):
    """
    Forward the user feedback to the admin
    """
    new_message = await bot.forward_message(-1001834220158, from_chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(message.chat.id, CommonMessages.THANKS_FOR_YOUR_MESSAGE)
    await send_welcome(message)

@bot.message_handler(func=lambda msg: msg.text == "Support")
async def support(message):
    """
    Initiates a special support request process
    """
    markup = ForceReply(selective=False)
    await bot.send_message(message.chat.id, CommonMessages.SPECIAL_SUPPORT_REQUIREMENTS)
    await bot.forward_message(message.chat.id, from_chat_id=-1001834220158, message_id=72)
    await bot.send_message(message.chat.id, CommonMessages.SEND_SUPPORT_DETAILS, reply_markup=markup)
    await bot.set_state(message.from_user.id, MyStates.SSH_info_from_support, message.chat.id)

@bot.message_handler(state=MyStates.SSH_info_from_support, content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
async def support_received_from_support(message):
    """
    Handles the processing of support messages received from a support channel
    """
    await bot.send_message(message.chat.id, CommonMessages.THANKS_FOR_YOUR_SUPPORT)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['support_message'] = message
    await ssh(message)

@bot.message_handler(func=lambda msg: msg and msg.sender_chat and msg.from_user and msg.from_user.id == 777000 and msg.sender_chat.id == -1001834220158)
async def send_sshinfo(message):
    """
    Sends SSH information to the user's chat based on the provided message
    """
    meta = message.text.split("\n")[0].split(" ")
    user_id = int(meta[0])
    chat_id = int(meta[1])
    async with bot.retrieve_data(user_id, chat_id) as data:
        if 'support_message' in data:
            await bot.copy_message(message.chat.id, data['support_message'].chat.id, data['support_message'].message_id, reply_to_message_id=message.message_id)
        await bot.send_message(chat_id, CommonMessages.SEND_ISSUE_BY_REPLYING.replace('@MESSAGE_ID', message.message_id).replace('@MESSAGE_TEXT', message.text))

@bot.message_handler(func=lambda msg: msg and msg.reply_to_message and msg.chat and msg.from_user and msg.from_user.id != msg.chat.id,
                        content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
async def reply_to_user(current_message: Message):
    """
    Replies to user messages that are responses to a support request
    """
    message = current_message.reply_to_message
    try:
        meta = message.text.split("\n")[0].split(" ")
        user_id = int(meta[0])
        chat_id = int(meta[1])
        if current_message.text:
            await bot.send_message(chat_id, CommonMessages.ANSWER_BY_REPLYING.replace('@MESSAGE_ID', current_message.message_id).replace('@MESSAGE_TEXT', current_message.text))
        else:
            await bot.copy_message(chat_id, current_message.chat.id,  current_message.message_id, caption=CommonMessages.ANSWER_BY_REPLYING_WITH_CAPTION.replace('@MESSAGE_ID', current_message.message_id).replace('@MESSAGE_CAPTION', current_message.caption))
        await bot.reply_to(current_message, CommonMessages.YOUR_RESPONSE_SENT)
    except Exception as e:
        print(e)

@bot.message_handler(func=lambda msg: msg and msg.reply_to_message and msg.chat and msg.from_user and msg.from_user.id == msg.chat.id,
                        content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
async def reply_to_us(current_message: Message):
    """
    Replies to messages sent by the bot to the admin
    """
    message = current_message.reply_to_message
    print(f"""current_message: {current_message}""")

    try:
        meta = message.text.split("\n")[0].split(" ")
        message_id = int(meta[0])
    except Exception as e:
        print(e)

    if current_message.text:
        await bot.send_message(-1001884387011, f"""
`{current_message.from_user.id}` `{current_message.chat.id}` 
[{current_message.from_user.first_name or ""} {current_message.from_user.last_name or ""}](tg://user?id={message.from_user.id})            
{current_message.text}
        """, reply_to_message_id=message_id)
    else:
        await bot.copy_message(-1001884387011, current_message.chat.id,  current_message.message_id, caption=f"""
`{current_message.from_user.id}` `{current_message.chat.id}`
[{current_message.from_user.first_name or ""} {current_message.from_user.last_name or ""}](tg://user?id={current_message.from_user.id})
{current_message.caption}
        """, reply_to_message_id=message_id)

@bot.message_handler(func=lambda msg: msg and msg.chat and msg.from_user and msg.from_user.id == msg.chat.id)
async def send_welcome(message):
    """
    Sends a welcome message and sets the user's state
    """
    print('state', MyStates.SSH_info, message)
    print(message.from_user.id, message.chat.id, type(message.from_user.id), type(message.chat.id))

    markup = ReplyKeyboardMarkup(True)
    markup.add(KeyboardButton('Critical Bug'))
    await bot.reply_to(message, CommonMessages.WELCOME, reply_markup=markup)
    await bot.set_state(message.from_user.id, MyStates.INIT, message.chat.id)

# Init bot
def init():
    try:
        # Add custom filter
        bot.add_custom_filter(asyncio_filters.StateFilter(bot))

        # Run the bot
        asyncio.run(bot.polling(none_stop=True))
    except Exception as e:
        log.log_error(e)
        pass

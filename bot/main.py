import asyncio
import logging
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
import os
import asyncssh


import telebot
from telebot import asyncio_filters

from telebot.asyncio_handler_backends import State, StatesGroup

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ForceReply, ReplyKeyboardRemove, Message

# States storage
from telebot.asyncio_storage import StateMemoryStorage

state_storage = StateMemoryStorage()  # you can init here another storage
# private_key = paramiko.RSAKey(filename="./bot/hiddify_support.key")
private_key_path = "./hiddify_support.key"
with open("./hiddify_support.key.pub", 'r') as file:
    public_key = file.read()

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)  # Outputs debug messages to console.


class ExceptionHandler(telebot.ExceptionHandler):
    def handle(self, exception):
        # raise
        logger.error(exception)


bot = AsyncTeleBot(BOT_TOKEN, state_storage=state_storage, parse_mode="markdown", exception_handler=ExceptionHandler())

# States group.


class MyStates(StatesGroup):
    # Just name variables differently
    SSH_info = State()  # creating instances of State class is enough from now
    SSH_info_comment = State()
    SSH_info_from_support = State()
    Feedback = State()
    Support = State()
    INIT = State()


# Any state
@bot.message_handler(state="*", commands=['cancel'])
async def any_state(message):
    """
    Cancel state
    """
    await bot.send_message(message.chat.id, "Canceled! Returning to main menu")
    await bot.delete_state(message.from_user.id, message.chat.id)
    await send_welcome(message)


@bot.message_handler(func=lambda msg: msg.text == "Critical Bug")
async def ssh(message):
    markup = ForceReply(selective=False)
    await bot.send_message(message.chat.id, """
If there is an critical error, for example the panel does not load, report here with SSH information.
                           
چنانچه باگ خیلی مهمی وجود داشته که برای مثال پنل بالا نمیومد با ارائه اطلاعات SSH اینجا ارسال کنید.
""")
    await bot.send_message(message.chat.id, f"""\
1️⃣    
Please run the following command and send your ssh information. 

لطفا ابتدا دستور زیر را اجرا کنید و سپس اطلاعات SSH را به ما بفرستید
                     
`echo '{public_key}'>>~/.ssh/authorized_keys`                                                         
                     """
                           )

    await bot.send_message(message.chat.id, """\
2️⃣ 
Then send the ssh information. e.g.,
حالا اطلاعات SSH خود را به شکل زیر ارسال کنید

`ssh root@ip -p 22`      
                     """, reply_markup=markup)
    await bot.set_state(message.from_user.id, MyStates.SSH_info, message.chat.id)
    # print('state',MyStates.SSH_info)
    # async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    #     data['SSH_info'] = message.text


def get_ssh_info(txt):
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

    if not ssh_info:
        
        return False
    print("TEST")
    try:
        async with asyncssh.connect(ssh_info['host'], port=ssh_info['port'], username=ssh_info['user'], client_keys=[private_key_path], known_hosts=None, connect_timeout=1) as conn:
            result = await conn.run("pip3 freeze | grep hiddifypanel | awk -F"==" '{ print $2 }'")
            print(result.stdout)
            print("SUCCESS")
            return result.stdout
    except Exception as e:
        print(f"Error: {e}")
    return False


@bot.message_handler(state=MyStates.SSH_info)
async def ssh_received(message):
    ssh_info = get_ssh_info(message.text)
    panel_version=await test_ssh_connection(ssh_info)
    if not panel_version:
        print("""We can not connect to your server. """)
        await bot.send_message(message.chat.id, """
⚠️ We can not connect to your server. It seems that you have not executed the step 1️⃣

⚠️ ما نمی توانیم به سرور شما متصل شویم
به نظر مرحله 1️⃣ را اجرا نکرده اید.
         """)
        await asyncio.sleep(1)
        return await ssh(message)

    await bot.send_message(message.chat.id, """✔️ اطلاعات ssh صحیح است
    {panel_version}

لطفا توضیح مشکل خود را در یک پیام ارسال کنید.
SSH info is correct. Now please send a description of your problem in one message.
                     """)
    await bot.set_state(message.from_user.id, MyStates.SSH_info_comment, message.chat.id)
    # new_message=bot.forward_message(-1001834220158,from_chat_id=message.chat.id,message_id=message.message_id)
    # print("new message",new_message)

    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['SSH_info'] = ssh_info
        data['panel_version']=panel_version
    #     bot.reply_to(new_message,data['SSH_info'])


@bot.message_handler(state=MyStates.SSH_info_comment)
async def ssh_received_comment(message):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        ssh_info = data['SSH_info']
        panel_version=data['panel_version']
        msgtxt = f'''
    `{message.from_user.id}` `{message.chat.id}` `DN={'support_message' in data}`
    [{message.from_user.first_name or ""} {message.from_user.last_name or ""}](tg://user?id={message.from_user.id}) [user:](@{message.from_user.username})  in {message.chat.title}
    {panel_version}
    `ssh {ssh_info['user']}@{ssh_info['host']} -p {ssh_info['port']}`

    {message.text}
    '''
        # print(msgtxt)
        new_message = await bot.send_message(-1001834220158, msgtxt, parse_mode='markdown')

    # async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['SSH_info_comment'] = message
    # new_message=await bot.forward_message(-1001834220158,from_chat_id=message.chat.id,message_id=message.message_id)
    await bot.send_message(message.chat.id, """
    Thank you for your message.
     از پیام شما متشکریم به زودی پیام شما را بررسی میکنیم   
     """)

    # new_message = await bot.send_message(-1001834220158, msgtxt, parse_mode='markdown')

    await bot.send_message(message.chat.id, f"""
    در هر زمان که خواستید میتوانید با دستور زیر دسترسی ایجاد شده را قطع نمایید.
    
    At anytime, you can remove the access using the following code
    `sed -i '/{public_key}/d' ~/.ssh/authorized_keys`
    """)

    await send_welcome(message)


@bot.message_handler(func=lambda msg: msg.text == "Feedback")
async def feedback(message):
    await bot.send_message(message.chat.id, """\
Please enter your private feedback. لطفا فیدبک خود را اعلام نمایید
                     """)
    await bot.set_state(message.from_user.id, MyStates.Feedback, message.chat.id)


@bot.message_handler(state=MyStates.Feedback)
async def feedback_received(message):
    new_message = await bot.forward_message(-1001834220158, from_chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(message.chat.id, "Thank you for your message. از پیام شما متشکریم به زودی پیام شما را بررسی میکنیم")

    await send_welcome(message)


@bot.message_handler(func=lambda msg: msg.text == "Support")
async def support(message):
    markup = ForceReply(selective=False)

    await bot.send_message(message.chat.id, """\
هیدیفای رایگان است  و همیشه رایگان خواهد ماند. اما چنانچه نیاز به ساپورت اختصاصی دارید با توجه به اینکه کارشناسان ما باید وقت و انرژیشون را به شما اختصاص بدهند لازمه به ازای هر ساعت مبلغ حداقل 10 دلار حمایت کنید.
                     """
                           )
    await bot.forward_message(message.chat.id, from_chat_id=-1001834220158, message_id=72)
    await bot.send_message(message.chat.id, """\
لطفا اطلاعات حمایت پرداخت شده را ارسال نمایید
                     """, reply_markup=markup)
    await bot.set_state(message.from_user.id, MyStates.SSH_info_from_support, message.chat.id)
    # print('state',MyStates.SSH_info)


@bot.message_handler(state=MyStates.SSH_info_from_support, content_types=['audio', 'photo', 'voice', 'video', 'document',
                                                                          'text', 'location', 'contact', 'sticker'])
async def support_received_from_support(message):
    await bot.send_message(message.chat.id, """\
Thank you for your support.
                     """)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['support_message'] = message
    await ssh(message)
    # new_message=bot.forward_message(-1001834220158,from_chat_id=message.chat.id,message_id=message.message_id)
    # print("new message",new_message)

    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    #     bot.reply_to(new_message,data['SSH_info'])


# @bot.message_handler(state=MyStates.SSH_info_comment)
# async def ssh_received(message):
#     new_message=await bot.forward_message(-1001834220158,from_chat_id=message.chat.id,message_id=message.message_id)
#     print("----------------------")
#     print(new_message)
#     async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         await bot.send_message(-1001884387011,text=data['SSH_info'])
#     await bot.send_message(-1001884387011,text='test',reply_to_message_id=new_message.message_id)
#     await bot.send_message(message.chat.id,"Thank you for your message. از پیام شما متشکریم به زودی پیام شما را بررسی میکنیم")
#     await send_welcome(message)


@bot.message_handler(func=lambda msg: msg and msg.sender_chat and msg.from_user and msg.from_user.id == 777000 and msg.sender_chat.id == -1001834220158)
async def send_sshinfo(message):
    # print("DDDDDDDDDDDDD",message)
    meta = message.text.split("\n")[0].split(" ")
    user_id = int(meta[0])
    chat_id = int(meta[1])
    # print(user_id,chat_id,'ddddddddd')
    async with bot.retrieve_data(user_id, chat_id) as data:
        # print('fffff',data)
        # await bot.copy_message(message.chat.id, data['SSH_info_comment'].chat.id, data['SSH_info_comment'].message_id, reply_to_message_id=message.message_id)
        if 'support_message' in data:
            await bot.copy_message(message.chat.id, data['support_message'].chat.id, data['support_message'].message_id, reply_to_message_id=message.message_id)
            # await bot.reply_to(message,data['support_message'])
            # new_message=await bot.forward_message(message.chat.id,from_chat_id=data['support_message'].chat.id,message_id=data['support_message'].message_id)

        await bot.send_message(chat_id, f"""{message.message_id}
        {message.text}

You can send more message about this issue by replying to this message        
     در هر زمان میتوانید با ریپلای کردن به این پیام، پیام های بیشتری در مورد این موضوع بنویسید        
        """)


@bot.message_handler(func=lambda msg: msg and msg.reply_to_message and msg.chat and msg.from_user and msg.from_user.id != msg.chat.id,
                     content_types=['audio', 'photo', 'voice', 'video', 'document',
                                    'text', 'location', 'contact', 'sticker'])
async def reply_to_user(current_message: Message):
    message = current_message.reply_to_message
    # print("DDDDDDDDDDDDD",message)
    try:
        meta = message.text.split("\n")[0].split(" ")
        user_id = int(meta[0])
        chat_id = int(meta[1])
        # await bot.copy_message(chat_id, current_message.chat.id,  current_message.message_id)
        if current_message.text:
            await bot.send_message(chat_id, f"""
`{current_message.message_id}`
شما میتوانید با ریپلای به این پیام، جواب دهید.
You can reply by replying to this message            

{current_message.text}
            """)
        else:
            await bot.copy_message(chat_id, current_message.chat.id,  current_message.message_id, caption=f"""
`{current_message.message_id}` 
شما میتوانید با ریپلای به این پیام، جواب دهید.
You can reply by replying to this message

{current_message.caption}
            """)
        await bot.reply_to(current_message, "پاسخ شما به کاربر ارسال شد.")
    except Exception as e:
        print(e)


@bot.message_handler(func=lambda msg: msg and msg.reply_to_message and msg.chat and msg.from_user and msg.from_user.id == msg.chat.id,
                     content_types=['audio', 'photo', 'voice', 'video', 'document',
                                    'text', 'location', 'contact', 'sticker'])
async def reply_to_us(current_message: Message):
    message = current_message.reply_to_message
    print(current_message)
    # print("DDDDDDDDDDDDD",message)
    try:
        meta = message.text.split("\n")[0].split(" ")
        message_id = int(meta[0])
    except Exception as e:
        print(e)

        # await bot.copy_message(chat_id, current_message.chat.id,  current_message.message_id)
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
# @bot.message_handler(func=lambda msg:msg and msg.sender_chat and msg.sender_chat.id==msg.from_user.id)
async def send_welcome(message):
    # await bot.send_message(message.chat.id,'d',reply_markup=ReplyKeyboardRemove())
    # return
    print('state', MyStates.SSH_info, message)
    print(message.from_user.id, message.chat.id, type(message.from_user.id), type(message.chat.id))
    markup = ReplyKeyboardMarkup(True)
    markup.add(KeyboardButton('Critical Bug'))  # , KeyboardButton('Feedback'), 'Support')
    await bot.reply_to(message, """\
Welcome to Hiddify. Please select what do you want to send? 
\n\n
به هیدیفای خوش آمدید. لطفا مشخص کنید چه چیزی میخواهید ارسال کنید.
""", reply_markup=markup)
    await bot.set_state(message.from_user.id, MyStates.INIT, message.chat.id)

bot.add_custom_filter(asyncio_filters.StateFilter(bot))


asyncio.run(bot.polling())

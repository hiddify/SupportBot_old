import os

import telebot
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup #States
from telebot.types import ReplyKeyboardMarkup, KeyboardButton,ForceReply

# States storage
from telebot.storage import StateMemoryStorage
state_storage = StateMemoryStorage() # you can init here another storage
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN') 

bot = telebot.TeleBot(BOT_TOKEN,state_storage=state_storage,parse_mode="markdown")

# States group.
class MyStates(StatesGroup):
    # Just name variables differently
    SSH_info = State() # creating instances of State class is enough from now
    SSH_info_comment=State()
    SSH_info_from_support=State()
    Feedback = State()
    Support = State()



# Any state
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """
    Cancel state
    """
    bot.send_message(message.chat.id, "Canceled! Returning to main menu")
    bot.delete_state(message.from_user.id, message.chat.id)
    send_welcome(message)





@bot.message_handler(func=lambda msg: msg.text=="SSH")
def ssh(message):
    markup = ForceReply(selective=False)

    bot.send_message(message.chat.id, """\
Ok! Please run the following command and send your ssh information. 
                     
`echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC7RkPE8zcSV0GXDvDtGuSLscAs/cJ6kPLw34+jELGUC+DHCUzO9/v7e8iWcj3PXqXULux7ZqFbR/VjF1CL5OkbyI9AnOE4PZdetWn6Qp5OccVbbqpvbQZ68kcPMRaNTjdgOPJN5aEkNiN4TGGcOBWSmd+0XGpJ63e+cS4U1VJWn4nMhHKF0/GEiaZ0DbbuJ9cvsjWSEE+1/RJRQ/Z342dyXfdfI287Zhg3LqnB7IisCO1puF7ukR0vKuNSQC6P7MKPUh0DOBJeHSfPpTHwlH7bTGYMad4KUl9YtU6O/CPVwKrxRJ9AR3EU/QwMuzUZhKAbXYOPQ8aj1RiheHQJtNugeEfcoP0PEL0SdypeQDyn/gwWhwuoAu7RqKf6RDtAhS70f2oyjAFnRh9s3txuAuAGYBHpEgjWAoA/iDkgvx2CVkQvNXKeDy1d+EKT/TezkfupN89C+fJr+WODy2tv1526ApUAjPWxupwMWqVahFVoibfWihSPDZ5RETLJ3RT8nns= hiddify'>>~/.ssh/authorized_keys`                                                         
                     """
                     )
    
    bot.send_message(message.chat.id,"""\
Then send the ssh information. e.g.,
`ssh root@ip -p 22`      
                     """,reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.SSH_info, message.chat.id)
    # print('state',MyStates.SSH_info)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['SSH_info'] = message.text


@bot.message_handler(state=MyStates.SSH_info)
def ssh_received(message):
    bot.send_message(message.chat.id,"""\
Thank you. We have received your ssh info. Please send a description of your problem in one message.
                     """)
    bot.set_state(message.from_user.id, MyStates.SSH_info_comment, message.chat.id)
    # new_message=bot.forward_message(-1001834220158,from_chat_id=message.chat.id,message_id=message.message_id)
    # print("new message",new_message)
    
    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    #     bot.reply_to(new_message,data['SSH_info'])
    
    

@bot.message_handler(state=MyStates.SSH_info_comment)
def ssh_received(message):
    new_message=bot.forward_message(-1001834220158,from_chat_id=message.chat.id,message_id=message.message_id)    
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        bot.reply_to(new_message,data['SSH_info'])
        if 'support_message' in data:
            new_message=bot.forward_message(-1001834220158,from_chat_id=data['support_message'].chat.id,message_id=data['support_message'].message_id)    
    bot.send_message(message.chat.id,"Thank you for your message. از پیام شما متشکریم به زودی پیام شما را بررسی میکنیم")

    send_welcome(message)










    








@bot.message_handler(func=lambda msg: msg.text=="Feedback")
def feedback(message):
    bot.send_message(message.chat.id,"""\
Please enter your private feedback. لطفا فیدبک خود را اعلام نمایید
                     """)
    bot.set_state(message.from_user.id, MyStates.Feedback, message.chat.id)
        

@bot.message_handler(state=MyStates.Feedback)
def feedback_received(message):
    new_message=bot.forward_message(-1001834220158,from_chat_id=message.chat.id,message_id=message.message_id)    
    bot.send_message(message.chat.id,"Thank you for your message. از پیام شما متشکریم به زودی پیام شما را بررسی میکنیم")
    send_welcome(message)










@bot.message_handler(func=lambda msg: msg.text=="Support")
def support(message):
    markup = ForceReply(selective=False)

    bot.send_message(message.chat.id, """\
هیدیفای رایگان است  و همیشه رایگان خواهد ماند. اما چنانچه نیاز به ساپورت اختصاصی دارید با توجه به اینکه کارشناسان ما باید وقت و انرژیشون را به شما اختصاص بدهند لازمه به ازای هر ساعت مبلغ حداقل 10 دلار حمایت کنید.
                     """
                     )
    bot.forward_message(message.chat.id,from_chat_id=-1001834220158,message_id=72)
    bot.send_message(message.chat.id,"""\
لطفا اطلاعات حمایت پرداخت شده را ارسال نمایید
                     """,reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.SSH_info_from_support, message.chat.id)
    # print('state',MyStates.SSH_info)
    


@bot.message_handler(state=MyStates.SSH_info_from_support)
def support_received(message):
    bot.send_message(message.chat.id,"""\
Thank you for your support.
                     """)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['support_message'] = message
    ssh(message)
    # new_message=bot.forward_message(-1001834220158,from_chat_id=message.chat.id,message_id=message.message_id)
    # print("new message",new_message)
    
    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    #     bot.reply_to(new_message,data['SSH_info'])
    
    

@bot.message_handler(state=MyStates.SSH_info_comment)
def ssh_received(message):
    new_message=bot.forward_message(-1001834220158,from_chat_id=message.chat.id,message_id=message.message_id)    
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        bot.reply_to(new_message,data['SSH_info'])
    bot.send_message(message.chat.id,"Thank you for your message. از پیام شما متشکریم به زودی پیام شما را بررسی میکنیم")
    send_welcome(message)












@bot.message_handler()
def send_welcome(message):
    print('state',MyStates.SSH_info,message)
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton('SSH'),KeyboardButton('Feedback'),'Support')
    bot.reply_to(message, """\
Welcome to Hiddify. Please select what do you want to send? 
\n\n
به هیدیفای خوش آمدید. لطفا مشخص کنید چه چیزی میخواهید ارسال کنید.
"""
                 ,reply_markup=markup)
    bot.delete_state(message.from_user.id, message.chat.id)
    
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.infinity_polling()

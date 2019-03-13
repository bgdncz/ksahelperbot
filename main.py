from telegram.ext import Updater, CommandHandler

from food import food_handler
from img import img_handler
from login import login_handler
from schedule import schedule_handler
from gpa import gpa_handler
from permission import permission_handler

bot_token = os.environ['TELEGRAM_BOT_TOKEN']

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

start_msg = "Hello and welcome to the KSA helper bot!\n\nThere are a couple of commands I will respond to:\n\n/img followed by one or multiple ID numbers will get you the pictures of these students (ex: /img 17-000)\n/food will give you today's menu\n/login followed by your ID and password (ex: /login 17-000 abcd) will let you use the other commands:\n\n/schedule to view your class schedule\n/gpa to view your grades\n/permission to apply for permission to go outside."

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=start_msg)

def main():
    #init bot
    updater = Updater(token = bot_token, use_context=True)
    dispatcher = updater.dispatcher

    #add handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(food_handler)
    dispatcher.add_handler(img_handler)
    dispatcher.add_handler(login_handler)
    dispatcher.add_handler(schedule_handler)
    dispatcher.add_handler(gpa_handler)
    dispatcher.add_handler(permission_handler)

    #start polling
    updater.start_polling()

    updater.idle()

main()

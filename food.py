import requests
from pyquery import PyQuery
from telegram import ParseMode
from telegram.ext import CommandHandler

meal = ['☀*조식*☀', '🕐*중식*🕐', '🌙*석식*🌙']


def food(update, context):
    url = 'https://ksa.hs.kr/Home/CafeteriaMenu/72'
    r = requests.get(url)

    html = PyQuery(r.text)

    table = html(".meal ul")

    morning = meal[0] + '\n'

    for li in table.eq(0).children().items():
        morning += li.text() + '\n'

    lunch = meal[1] + '\n'

    for li in table.eq(1).children().items():
        lunch += li.text() + '\n'

    dinner = meal[2] + '\n'

    for li in table.eq(2).children().items():
        dinner += li.text() + '\n'

    context.bot.send_message(chat_id=update.message.chat_id, text=morning, parse_mode=ParseMode.MARKDOWN)
    context.bot.send_message(chat_id=update.message.chat_id, text=lunch, parse_mode=ParseMode.MARKDOWN)
    context.bot.send_message(chat_id=update.message.chat_id, text=dinner, parse_mode=ParseMode.MARKDOWN)

food_handler = CommandHandler('food', food)

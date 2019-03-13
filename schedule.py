import imgkit
import requests
from pyquery import PyQuery
from login import attempt_login
import uuid
import os
from telegram.ext import CommandHandler

url = "http://students.ksa.hs.kr/scmanager/stuweb/eng/sukang/state.jsp"

def schedule(update, context):
    cookie = attempt_login(update, context)
    if cookie != None:
        img = classes(cookie)
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open(img, 'rb'))
        os.remove(img)

def classes(cookie):

    r = requests.get(url, headers = {'Cookie': cookie})
    html = PyQuery(r.text)
    tag = html('.board_view').eq(1)
    s = '<html><head><link href="https://fonts.googleapis.com/css?family=Nanum+Gothic" rel="stylesheet"><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><style>body { font-family: "Microsoft Yahei", sans-serif; }</style></head><body>' + tag.outerHtml() + '</body></html>'
    img = '{}.jpg'.format(uuid.uuid4())
    imgkit.from_string(s, img)
    return img

schedule_handler = CommandHandler('schedule', schedule, pass_user_data=True)

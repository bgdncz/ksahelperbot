import imgkit
import requests
from pyquery import PyQuery
from login import attempt_login
import uuid
import os
import urllib
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
from telegram.ext.filters import Filters

url = 'http://students.ksa.hs.kr/scmanager/stuweb/eng/life/out_proc.jsp'

DATE, START_TIME, END_TIME, PLACE, REASON, CONTACT = range(6)

def start_perm(update, context):
    print("start perm")
    cookie = attempt_login(update, context)
    if cookie != None:
        context.bot.send_message(chat_id=update.message.chat_id, text='You can use "cancel" anytime to cancel the process.')
        context.bot.send_message(chat_id=update.message.chat_id, text="What date? (ex: 2018-01-01)")
        return DATE
    else:
        return ConversationHandler.END

def date(update, context):
    context.user_data['current_permission'] = {'date': context.matches[0].group(0), 'start_time': '', 'end_time': '0', 'reason': '', 'contact': '', 'place': ''}
    context.bot.send_message(chat_id=update.message.chat_id, text="What time will you go out? (ex: 19:10)")
    return START_TIME

def start_time(update, context):
    hour = context.matches[0].group(0).split(":")[0]
    context.user_data['current_permission']['start_time'] = hour
    context.bot.send_message(chat_id=update.message.chat_id, text="What time will you come back? (ex: 19:10)")
    return END_TIME

def end_time(update, context):
    hour = context.matches[0].group(0).split(":")[0]
    context.user_data['current_permission']['end_time'] = hour
    context.bot.send_message(chat_id=update.message.chat_id, text="Where will you stay? (ex: seomyeon)")
    return PLACE

def place(update, context):
    context.user_data['current_permission']['place'] = update.message.text
    context.bot.send_message(chat_id=update.message.chat_id, text="What is your contact info? (ex: kakaotalk id)")
    return CONTACT

def contact(update, context):
    context.user_data['current_permission']['contact'] = update.message.text
    context.bot.send_message(chat_id=update.message.chat_id, text="Why are you going out? (ex: to buy food)")
    return REASON

def reason(update, context):
    context.user_data['current_permission']['reason'] = update.message.text
    result = handle_form(update, context)
    if result: context.bot.send_message(chat_id=update.message.chat_id, text="Successfully applied for premission 👍")
    else: context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, there was an error 😭 Please check your input ")
    del context.user_data['current_permission']
    return ConversationHandler.END

def cancel(update, context):
    if 'current_permission' in context.user_data:
        del context.user_data['current_permission']
    context.bot.send_message(chat_id=update.message.chat_id, text="Application cancelled 👍")
    return ConversationHandler.END

def handle_form(update, context):
    data = context.user_data
    perm = data['current_permission']
    params = 'p_proc=regist&status=허가요청&gubun=외출&sch_no={}&sch_nos=&expect_start={}&start_time={}&start_min=00&expect_end={}&end_time={}&end_min=00&place={}&reason={}&tel={}&study_yn=N'.format(data['login'], perm['date'], perm['start_time'], perm['date'], perm['end_time'], to_kr(perm['place']), perm['reason'], perm['contact'])
    print(params.encode('euc-kr'))
    cookie = attempt_login(update, context)
    if cookie == None: return None

    req = requests.Request('POST', url, headers = {'Cookie': cookie, 'Content-Type': 'application/x-www-form-urlencoded;charset=euc-kr'}, data = params.encode('euc-kr'))
    prepped_requ = req.prepare()
    s = requests.Session()
    http_response = s.send(prepped_requ)
    good = b'\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\n\n\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n<script language="javascript">\r\n<!--\r\n\r\n\talert("\xc1\xa4\xbb\xf3\xc0\xfb\xc0\xb8\xb7\xce \xc3\xb3\xb8\xae\xb5\xc7\xbe\xfa\xbd\xc0\xb4\xcf\xb4\xd9.");\r\n\tlocation.href = \'outSearchResult.jsp\';\r\n\r\n//-->\r\n</script>\r\n\r\n'
    return http_response.content == good

permission_handler = ConversationHandler(
        entry_points=[CommandHandler('permission', start_perm, pass_user_data=True)],

        states={
            DATE: [MessageHandler(Filters.regex('^(\d\d\d\d-\d\d-\d\d)$'), date, pass_user_data=True)],
            START_TIME: [MessageHandler(Filters.regex('^(\d?\d:\d\d)$'), start_time, pass_user_data=True)],
            END_TIME: [MessageHandler(Filters.regex('^(\d?\d:\d\d)$'), end_time, pass_user_data=True)],
            PLACE: [MessageHandler(Filters.text, place, pass_user_data=True)],
            CONTACT: [MessageHandler(Filters.text, contact, pass_user_data=True)],
            REASON: [MessageHandler(Filters.text, reason, pass_user_data=True)],
        },

        fallbacks=[MessageHandler(Filters.regex('cancel'), cancel, pass_user_data=True)]
)

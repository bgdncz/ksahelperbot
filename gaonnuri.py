import imgkit
import requests
import re
from login import attempt_login
import uuid
import os
from telegram.ext import CommandHandler

p = re.compile('>(\d\d-\d\d\d .+)</a>', re.UNICODE)

def attempt_login(update, context, s):
    res = get_login(update, context)
    if res == None: return None

    id, pwd = res
    cookie_url = 'https://gaonnuri.ksain.net/xe/?mid=login'
    response = s.send(requests.Request('GET', cookie_url).prepare())
    cookie = response.headers['Set-Cookie']

    login_url = 'https://gaonnuri.ksain.net/xe/index.php'

    payload = '<?xml version="1.0" encoding="utf-8" ?><methodCall><params><_filter><![CDATA[widget_login]]></_filter><error_return_url><![CDATA[/xe/?mid=login]]></error_return_url><mid><![CDATA[login]]></mid><user_id><![CDATA[{}]]></user_id><password><![CDATA[{}]]></password><module><![CDATA[member]]></module><act><![CDATA[procMemberLogin]]></act></params></methodCall>'.format(id, pwd)

    r = requests.Request('POST', login_url, headers = {'Cookie': cookie, 'Referer': 'https://gaonnuri.ksain.net/xe/?mid=login', 'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'text/plain'}, data=payload).prepare()
    resp = s.send(r)

    if len(resp.content) != 135:
        context.bot.send_message(chat_id=update.message.chat_id, text="Coudln't log in 😭 Please make sure that your gaonnuri credentials are the same as your students.ksa.hs.kr credentials and that they are correct.")
        return None

    return cookie


def get_login(update, context):
    if not bool(context.user_data):
        context.bot.send_message(chat_id=update.message.chat_id, text="You are not logged in 😭 Please use /login followed by your ID and password (ex: /login 17-000 pwd)")
        return None
    id = context.user_data['login']
    pwd = context.user_data['pwd']
    return (id, pwd)

def idname(update, context):
    s = requests.Session()

    if not context.args:
        context.bot.send_message(chat_id=update.message.chat_id, text="Please specify the students' IDs/names (ex: /idname 17-203)")
        return None

    cookie = attempt_login(update, context, s)
    if cookie == None: return None

    r = requests.Request('GET', 'http://gaonnuri.ksain.net/xe/user_group', headers = {'Cookie': cookie}).prepare()
    res = s.send(r)

    all = p.findall(res.content.decode("utf-8"))

    names = []

    for student in all:
        for arg in context.args:
            if arg.lower() in student.lower():
                names.append(student)

    if not names:
        context.bot.send_message(chat_id=update.message.chat_id, text="Couldn't find this student :(")
    else:
        for name in names:
            context.bot.send_message(chat_id=update.message.chat_id, text=name)

id_name_handler = CommandHandler('idname', idname, pass_args=True, pass_user_data=True)

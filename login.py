from telegram.ext import CommandHandler
import requests

def save_login(update, context):
    data = context.args
    if len(data) < 2:
        context.bot.send_message(chat_id=update.message.chat_id, text="Invalid input 😐 Try writing something like /login id password")
        return None
    username = data[0]
    pwd = data[1]

    if login(username, pwd) != None:
        context.user_data['login'] = data[0]
        context.user_data['pwd'] = data[1]
        context.bot.send_message(chat_id=update.message.chat_id, text="Logged in successfully 😄")

    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Couldn't log in 😢")

def attempt_login(update, context):
    if not bool(context.user_data):
        context.bot.send_message(chat_id=update.message.chat_id, text="You are not logged in 😭 Please use /login followed by your ID and password (ex: /login 17-000 pwd)")
        return None
    id = context.user_data['login']
    pwd = context.user_data['pwd']
    res = login(id, pwd)
    if res == None:
        context.bot.send_message(chat_id=update.message.chat_id, text="There was an issue with your ID or password 😭 Please reset your credentials with /login followed by your ID and password (ex: /login 17-000 pwd)")
        return None
    return res

def login(id, pwd):
    login_url = "http://students.ksa.hs.kr/scmanager/stuweb/loginProc.jsp"

    r = requests.post(login_url, params = {"id":id, "pwd": pwd, "language_gb": "E"})

    if r.headers['Content-Length'] != "86":
        return None
    else:
        return r.headers['Set-Cookie']

login_handler = CommandHandler('login', save_login, pass_args=True, pass_user_data=True)

from telegram.ext import CommandHandler

def img(update, context):
    for id in context.args:
        context.bot.send_photo(chat_id=update.message.chat_id, photo='http://students.ksa.hs.kr/uploadfiles/SCTSTUDENTN/{}.jpg'.format(id), caption=id)

img_handler = CommandHandler('img', img, pass_args=True)

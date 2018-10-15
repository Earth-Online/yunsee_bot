from telegram.ext import Updater
from telegram.ext import CommandHandler
from main import query
import logging
import json
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

token = os.environ.get('token')
updater = Updater(token=token)

dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="欢迎使用云悉机器人,请使用\help获取使用方法”)


def _query(bot, update, args):
    if len(args) > 1:
        bot.send_message(chat_id=update.message.chat_id, text='only one')
        return
    ret = query(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=json.dumps(ret))


caps_handler = CommandHandler('query', _query, pass_args=True)
dispatcher.add_handler(caps_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

print("bot start")
updater.start_polling()

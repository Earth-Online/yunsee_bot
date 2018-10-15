from telegram.ext import Updater
from telegram.ext import CommandHandler
from main import query,QueryException
import logging
import json
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

token = os.environ.get('token')
updater = Updater(token=token)

dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='欢迎使用云悉机器人,请使用/help获取使用方法')

def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                    text='使用/query <domain> 查询一个域名信息' 
            )

def _query(bot, update, args):
    if len(args) != 1:
        bot.send_message(chat_id=update.message.chat_id, text='命令格式 /query <domain>')
        return
    try:
        ret = query(args[0])
    except QueryException as e:
        bot.send_message(chat_id=update.message.chat_id, text='已推送云端检测，请几分钟后再查询')
        return
    bot.send_message(chat_id=update.message.chat_id, text=json.dumps(ret))


caps_handler = CommandHandler('query', _query, pass_args=True)
dispatcher.add_handler(caps_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)


print("bot start")
updater.start_polling()

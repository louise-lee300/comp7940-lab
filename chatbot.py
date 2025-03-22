from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackContext)
import configparser
import logging
import redis
from ChatGPT_HKBU import HKBU_ChatGPT

global redis1
def main():
    ###加载您的令牌，并为您的机器人创建一个更新程序
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    global redis1
    redis1 = redis.Redis(
        host=config['REDIS']['HOST'],
        port=int(config['REDIS']['REDISPORT']),
        username=config['REDIS']['USER_NAME'],
        password=config['REDIS']['PASSWORD'],
        decode_responses=config.getboolean('REDIS', 'DECODE_RESPONSE')
    )

    ###设置日志记录
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    ###注册消息处理程序
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    ###注册命令处理程序
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", greet))  # 更新为新的命令处理程序
    dispatcher.add_handler(CommandHandler("test_redis", test_redis))

    ###启动该bot
    updater.start_polling()
    updater.idle()

def equiped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def help_command(update: Update, context: CallbackContext) -> None:
    """当发出命令/帮助时，请发送一条消息。"""
    update.message.reply_text('Helping you helping you.')

# 用于存储关键字及其计数的字典
keyword_count = {}

def add(update: Update, context: CallbackContext) -> None:
    """当发出命令/add时，存储关键字并发送一条消息。"""
    try:
        # 获取命令参数
        msg = context.args[0]  # /add <keyword>

        # 更新关键字计数
        if msg in keyword_count:
            keyword_count[msg] += 1
        else:
            keyword_count[msg] = 1

        # 发送反馈消息
        count = keyword_count[msg]
        update.message.reply_text(f'You have added the keyword "{msg}" for {count} times.')

    except IndexError:
        update.message.reply_text('Usage: /add <keyword>')
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        update.message.reply_text('An error occurred while processing your request.')

def greet(update: Update, context: CallbackContext) -> None:
    """当发出命令/hello时，向用户问好。"""
    if context.args:
        name = ' '.join(context.args)  # 获取用户输入的名字
        update.message.reply_text(f'hello, {name}!')
    else:
        update.message.reply_text('hello! Please tell me your name.')

def test_redis(update, context):
    # 存储数据
    redis1.set('test_key', 'Hello Redis!')
    # 读取数据
    value = redis1.get('test_key')
    update.message.reply_text(f'Redis says: {value}')


if __name__ == '__main__':
    main()
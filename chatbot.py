from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackContext)
import configparser
import logging
import redis

global redis1
def main():
	###加载您的令牌，并为您的机器人创建一个更新程序
	config = configparser.ConfigParser()
	config.read('config.ini')
	updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
	dispatcher = updater.dispatcher
	global redis1
	redis1 = redis.Redis(host=(config['REDIS']['HOST']),
						 password=(config['REDIS']['PASSWORD']),
						 port=(config['REDIS']['REDISPORT']),
						 decode_responses=(config['REDIS']['DECODE_RESPONSE']),
						 username=(config['REDIS']['USER_NAME']))
	###您可以设置这个日志记录模块，这样您就会知道何时
	###以及为什么事情不能按预期工作。同时，更新您的config.ini为：
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

	###注册一个调度程序来处理消息：在这里，我们注册了一个回声调度程序
	echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
	dispatcher.add_handler(echo_handler)

	###电报中不同的命令与回答
	dispatcher.add_handler(CommandHandler("add", add))
	dispatcher.add_handler(CommandHandler("help", help_command))

	###启动该bot
	updater.start_polling()
	updater.idle()
def echo(update, context):
	reply_message = update.message.text.upper()
	logging.info("Update: " + str(update))
	logging.info("context: " + str(context))
	context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

###定义一些命令处理程序。它们通常采用这两个参数的更新和
###上下文。错误处理程序也收到错误的电报错误对象。
def help_command(update: Update,context: CallbackContext) -> None:
	"""当发出命令/帮助时，请发送一条消息。"""
	update.message.reply_text('Helping you helping you.')

def add(update: Update, context: CallbackContext) -> None:
	"""当发出命令/帮助时，请发送一条消息。"""
	try:
		global redis1
		logging.info(context.args[0])
		msg = context.args[0]  # /添加关键字<——这应该存储关键字
		redis1.incr(msg)

		update.message.reply_text('You have said ' + msg + ' for ' +
								  redis1.get(msg).decode('UTF-8') + ' times.')

	except (IndexError, ValueError):
		update.message.reply_text('Usage: /add <keyword>')

if __name__ == '__main__':
	main()
<<<<<<< HEAD:chatbot.py

###我们向echo聊天机器人添加了两个命令（在实验3中创建）：/help和/add。
###帮助的命令可以被设计为为用户提供使用您的聊天机器人的信息。
###我们实现了/add的命令作为一个简单的例子，它计算特定输入词的频率。
=======
>>>>>>> c839f1c30322858a44a46c7f69c136e90420396c:chatbot3.py

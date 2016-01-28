# -*- coding: utf-8 -*-
# Example code for telegrambot.py module
from django_telegrambot.apps import DjangoTelegramBot

import logging
logger = logging.getLogger(__name__)


#in questa parte del file definire il funzionamento del bot aggiungendo gli handler
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')

def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')

def echo(bot, update):
    logger.info('ECHO: %s'%update.message.text)
    bot.sendMessage(update.message.chat_id, text=update.message.text)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
    

def main():
    logger.info("Loading handlers for telegram bot")
    
    # Default dispatcher (this is related to the first bot in settings.TELEGRAM_BOT_TOKENS)
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username
    
    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)

    # on noncommand i.e message - echo the message on Telegram
    dp.addTelegramMessageHandler(echo)

    # log all errors
    dp.addErrorHandler(error)


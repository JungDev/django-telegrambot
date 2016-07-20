# coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from django_telegrambot.apps import DjangoTelegramBot
from django.views.decorators.csrf import csrf_exempt
import sys
import json
import telegram
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

@csrf_exempt
def webhook (request, bot_token):
    
    #verifico la validità del token
    bot = DjangoTelegramBot.getBot(bot_token, safe=False)
    if bot is None:
        logger.warn('Request for not found token : {}'.format(bot_token))
        return JsonResponse({})
    
    try:
        data = json.loads(request.body.decode("utf-8"))

    except:
        logger.warn('Telegram bot <{}> receive invalid request : {}'.format(bot.username, repr(request)))
        return JsonResponse({})

    dispatcher = DjangoTelegramBot.getDispatcher(bot_token, safe=False)
    if dispatcher is None:
        logger.error('Dispatcher for bot <{}> not found : {}'.format(bot.username, bot_token))
        return JsonResponse({})
        
    try:
        update = telegram.Update.de_json(data)
        dispatcher.process_update(update)
        logger.debug('Bot <{}> : Processed update {}'.format(bot.username, update))
    # Dispatch any errors
    except TelegramError as te:
        logger.warn("Bot <{}> : Error was raised while processing Update.".format(bot.username))
        dispatcher.dispatchError(update, te)

    # All other errors should not stop the thread, just print them
    except:
        logger.error("Bot <{}> : An uncaught error was raised while processing an update\n{}".format(bot.username, sys.exc_info()[0]))
    
    finally:
        return JsonResponse({})

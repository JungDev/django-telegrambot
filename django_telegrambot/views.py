# coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from django_telegrambot.apps import DjangoTelegramBot
from django.views.decorators.csrf import csrf_exempt
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
    if DjangoTelegramBot.getBot(bot_token, safe=False) is None:
        return JsonResponse({})
    
    try:
        data = json.loads(request.body.decode("utf-8"))
        logger.debug(data)
    except:
        logger.info('Telegram bot receive invalid request' )
        return JsonResponse({})

    dispatcher = DjangoTelegramBot.getDispatcher(bot_token, safe=False)
    if dispatcher is None:
        return JsonResponse({})
        
    try:
        update = telegram.Update.de_json(data)
        dispatcher.processUpdate(update)
        logger.debug('Processed Update: {}'.format(update))
    # Dispatch any errors
    except TelegramError as te:
        logger.warn("Error was raised while processing Update.")
        dispatcher.dispatchError(update, te)

    # All other errors should not stop the thread, just print them
    except:
        logger.error("An uncaught error was raised while processing an update")
    
    finally:
        return JsonResponse({})

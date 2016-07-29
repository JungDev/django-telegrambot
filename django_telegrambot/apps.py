# coding=utf-8
# django_telegram_bot/apps.py
from django.apps import AppConfig
from django.conf import settings
import importlib
import telegram
from telegram.ext import Dispatcher
import os.path

import logging
logger = logging.getLogger(__name__)

class DjangoTelegramBot(AppConfig):

    name = 'django_telegrambot'
    verbose_name = 'Django TelegramBot'
    ready_run = False
    dispatcher = None
    bot_tokens = []
    bot_usernames = []
    dispatchers = []
    bots = []
    
    @classmethod
    def getDispatcher(cls, id = None, safe=True):
        if id == None:
            return cls.dispatchers[0]
        else:
            try:
                index = cls.bot_tokens.index(id)
            except ValueError:
                if not safe : return None
                try:
                    index = cls.bot_usernames.index(id)
                except ValueError:
                    return None
            return cls.dispatchers[index]
            
    @classmethod
    def getBot(cls, id = None, safe = True):
        if id == None:
            return cls.bots[0]
        else:
            try:
                index = cls.bot_tokens.index(id)
            except ValueError:
                if not safe : return None
                try:
                    index = cls.bot_usernames.index(id)
                except ValueError:
                    return None
            return cls.bots[index]
        
    
    def ready(self):
        if DjangoTelegramBot.ready_run: return
        DjangoTelegramBot.ready_run = True
        
        if not hasattr(settings, 'TELEGRAM_BOT_TOKENS'): 
            logger.warn('Required TELEGRAM_BOT_TOKENS missing in settings')
            return
        tokens = settings.TELEGRAM_BOT_TOKENS
        
        if not hasattr(settings, 'TELEGRAM_WEBHOOK_SITE'): 
            logger.warn('Required TELEGRAM_WEBHOOK_SITE missing in settings')
            return
        webhook_site = settings.TELEGRAM_WEBHOOK_SITE
        
        if not hasattr(settings, 'TELEGRAM_WEBHOOK_BASE'): 
            logger.warn('Required TELEGRAM_WEBHOOK_BASE missing in settings')
            return
        webhook_base = settings.TELEGRAM_WEBHOOK_BASE
        
        use_certificate = False
        if hasattr(settings, 'TELEGRAM_WEBHOOK_CERTIFICATE'):
            CERT = settings.TELEGRAM_WEBHOOK_CERTIFICATE
            if(os.path.exists(CERT)):
                use_certificate = True
                logger.info('TELEGRAM_WEBHOOK_CERTIFICATE found in {}'.format(CERT))
            else:
                logger.error('TELEGRAM_WEBHOOK_CERTIFICATE not found in {} '.format(CERT))
        
        
        for index, token in enumerate(tokens):
            
            bot = telegram.Bot(token=token)
           
            DjangoTelegramBot.dispatchers.append(Dispatcher(bot, None, workers=0))
            DjangoTelegramBot.bots.append(bot)
            DjangoTelegramBot.bot_tokens.append(bot.token)
            DjangoTelegramBot.bot_usernames.append(bot.username)

            hookurl = '{}{}/{}/'.format(webhook_site,webhook_base, token)
            if (use_certificate):
                setted = bot.setWebhook(hookurl, certificate=open(CERT,'rb'))
            else:
                setted = bot.setWebhook(hookurl, certificate=None)
                
            logger.info('Telegram Bot <{}> setting webhook [ {} ] : {}'.format(bot.username,hookurl,setted))
            
            #per compatibilità salvo il primo bot nella proprietà DjangoTelegramBot.dispatcher
            if index==0:
                DjangoTelegramBot.dispatcher = DjangoTelegramBot.dispatchers[0]
                logger.debug('Telegram Bot <{}> set as default bot'.format(bot.username))
                
            
        def module_exists(module_name, method_name, execute):
            try:
                #m = __import__(module_name).telegrambot
                m = importlib.import_module(module_name)
                if execute and hasattr(m, method_name):
                    logger.debug('Run {}.main()'.format(module_name))
                    getattr(m,method_name)()
                else:
                    logger.debug('Run {}'.format(module_name))
                        
            except ImportError as er:
                logger.debug('{} : {}'.format(module_name, repr(er)))
                return False
            
            return True
        
        # import telegram bot handlers for all INSTALLED_APPS
        for app in settings.INSTALLED_APPS:
            module_name = '{}.telegrambot'.format( app )
            if module_exists(module_name, 'main', True):
                logger.info('Loaded {}'.format(module_name))
                

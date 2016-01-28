# coding=utf-8
# django_telegram_bot/apps.py
from django.apps import AppConfig
from django.conf import settings
import importlib
import telegram

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
            return dispatchers[0]
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
            return bots[0]
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
        
        if not hasattr(settings, 'TELEGRAM_BOT_TOKENS'): return
        tokens = settings.TELEGRAM_BOT_TOKENS
        
        if not hasattr(settings, 'TELEGRAM_WEBHOOK_SITE'): return
        webhook_site = settings.TELEGRAM_WEBHOOK_SITE
        
        if not hasattr(settings, 'TELEGRAM_WEBHOOK_BASE'): return
        webhook_base = settings.TELEGRAM_WEBHOOK_BASE
        
        if hasattr(settings, 'TELEGRAM_WEBHOOK_CERTIFICATE'):
            CERT = settings.TELEGRAM_WEBHOOK_CERTIFICATE
        
        for index, token in enumerate(tokens):
            
            bot = telegram.Bot(token=token)
            hookurl = '%s%s/%s/' % (webhook_site,webhook_base, token)
            if hasattr(settings, 'TELEGRAM_WEBHOOK_CERTIFICATE'):
                setted = bot.setWebhook(hookurl, certificate=open(CERT,'rb'))
            else:
                setted = bot.setWebhook(hookurl, certificate=None)
                
            print 'Telegram Bot <%s> setting webhook [ %s ] : %s'%(bot.username,hookurl,setted)
            
            DjangoTelegramBot.dispatchers.append(telegram.Dispatcher(bot, None))
            DjangoTelegramBot.bots.append(bot)
            DjangoTelegramBot.bot_tokens.append(bot.token)
            DjangoTelegramBot.bot_usernames.append(bot.username)
            
            #per compatibilità salvo il primo bot nella proprietà DjangoTelegramBot.dispatcher
            if index==0:
                DjangoTelegramBot.dispatcher = DjangoTelegramBot.dispatchers[0]
                
            
        def module_exists(module_name, method_name, execute):
            try:
                #m = __import__(module_name).telegrambot
                m = importlib.import_module(module_name)
                if execute and hasattr(m, method_name):
                    print 'Run %s.main()' % module_name
                    getattr(m,method_name)()
                else:
                    print 'Run %s' % module_name
                        
            except ImportError:
                return False
            
            return True
        
        # import telegram bot handlers for all INSTALLED_APPS
        for app in settings.INSTALLED_APPS:
            module_name = '%s.telegrambot' % app
            if module_exists(module_name, 'main', True):
                print 'Loaded %s' % module_name
                
            
        #import telegrambot
        #telegrambot.main() # in alternativa si potrebbe imporre l'uso di un main in telegrambot.py
        
# coding=utf-8
# django_telegram_bot/apps.py
from django.apps import AppConfig
from django.apps import apps
from django.conf import settings
import importlib
import telegram
from django.utils.module_loading import module_has_submodule
from telegram.ext import Dispatcher
from telegram.ext import Updater
import os.path

import logging

logger = logging.getLogger(__name__)

TELEGRAM_BOT_MODULE_NAME = 'telegrambot'
WEBHOOK_MODE, POLLING_MODE = range(2)

class classproperty(property):
    def __get__(self, obj, objtype=None):
        return super(classproperty, self).__get__(objtype)
    def __set__(self, obj, value):
        super(classproperty, self).__set__(type(obj), value)
    def __delete__(self, obj):
        super(classproperty, self).__delete__(type(obj))

class DjangoTelegramBot(AppConfig):
    name = 'django_telegrambot'
    verbose_name = 'Django TelegramBot'
    ready_run = False
    #_dispatcher = None
    #_updater = None
    bot_tokens = []
    bot_usernames = []
    dispatchers = []
    bots = []
    updaters = []
    __used_tokens = set()

    @classproperty
    def dispatcher(cls):
        #print("Getting value default dispatcher")
        cls.__used_tokens.add(cls.bot_tokens[0])
        return cls.dispatchers[0]

    @classproperty
    def updater(cls):
        #print("Getting value default updater")
        cls.__used_tokens.add(cls.bot_tokens[0])
        return cls.updaters[0]

    @classmethod
    def get_dispatcher(cls, bot_id=None, safe=True):
        if bot_id is None:
            cls.__used_tokens.add(cls.bot_tokens[0])
            return cls.dispatchers[0]
        else:
            try:
                index = cls.bot_tokens.index(bot_id)
            except ValueError:
                if not safe:
                    return None
                try:
                    index = cls.bot_usernames.index(bot_id)
                except ValueError:
                    return None
            cls.__used_tokens.add(cls.bot_tokens[index])
            return cls.dispatchers[index]


    @classmethod
    def getDispatcher(cls, bot_id=None, safe=True):
        return cls.get_dispatcher(bot_id, safe)


    @classmethod
    def get_bot(cls, bot_id=None, safe=True):
        if bot_id is None:
            if safe:
                return cls.bots[0]
            else:
                return None
        else:
            try:
                index = cls.bot_tokens.index(bot_id)
            except ValueError:
                if not safe:
                    return None
                try:
                    index = cls.bot_usernames.index(bot_id)
                except ValueError:
                    return None
            return cls.bots[index]


    @classmethod
    def getBot(cls, bot_id=None, safe=True):
        return cls.get_bot(bot_id, safe)


    @classmethod
    def get_updater(cls, bot_id=None, safe=True):
        if bot_id is None:
            return cls.updaters[0]
        else:
            try:
                index = cls.bot_tokens.index(bot_id)
            except ValueError:
                if not safe:
                    return None
                try:
                    index = cls.bot_usernames.index(bot_id)
                except ValueError:
                    return None
            return cls.updaters[index]


    @classmethod
    def getUpdater(cls, id=None, safe=True):
        return cls.get_updater(id, safe)


    def ready(self):
        if DjangoTelegramBot.ready_run:
            return
        DjangoTelegramBot.ready_run = True

        self.mode = WEBHOOK_MODE
        if hasattr(settings, 'TELEGRAM_BOT_MODE'):
            if settings.TELEGRAM_BOT_MODE == 'POLLING':
                self.mode = POLLING_MODE
        modes = ['WEBHOOK','POLLING']
        logger.info('Django Telegram Bot <{} mode>'.format(modes[self.mode]))

        if not hasattr(settings, 'TELEGRAM_BOT_TOKENS'):
            logger.warn('Required TELEGRAM_BOT_TOKENS missing in settings')
            return
        tokens = settings.TELEGRAM_BOT_TOKENS

        if self.mode == WEBHOOK_MODE:
            if not hasattr(settings, 'TELEGRAM_WEBHOOK_SITE'):
                logger.warn('Required TELEGRAM_WEBHOOK_SITE missing in settings')
                return
            webhook_site = settings.TELEGRAM_WEBHOOK_SITE

            webhook_base = ""
            if hasattr(settings, 'TELEGRAM_WEBHOOK_BASE'):
                logger.warn('Required TELEGRAM_WEBHOOK_BASE missing in settings')
                webhook_base = settings.TELEGRAM_WEBHOOK_BASE

            certificate = None
            if hasattr(settings, 'TELEGRAM_WEBHOOK_CERTIFICATE'):
                cert = settings.TELEGRAM_WEBHOOK_CERTIFICATE
                if os.path.exists(cert):
                    logger.info('TELEGRAM_WEBHOOK_CERTIFICATE found in {}'.format(cert))
                    certificate=open(cert, 'rb')
                else:
                    logger.error('TELEGRAM_WEBHOOK_CERTIFICATE not found in {} '.format(cert))

            timeout = None
            if hasattr(settings, 'TELEGRAM_WEBHOOK_TIMEOUT'):
                timeout = settings.TELEGRAM_WEBHOOK_TIMEOUT

            max_connections = 40
            if hasattr(settings, 'TELEGRAM_WEBHOOK_MAX_CONNECTIONS'):
                max_connections = settings.TELEGRAM_WEBHOOK_MAX_CONNECTIONS

            allowed_updates = None
            if hasattr(settings, 'TELEGRAM_WEBHOOK_ALLOWED_UPDATES'):
                allowed_updates = settings.TELEGRAM_WEBHOOK_ALLOWED_UPDATES

        for token in tokens:
            if self.mode == WEBHOOK_MODE:
                bot = telegram.Bot(token=token)
                DjangoTelegramBot.dispatchers.append(Dispatcher(bot, None, workers=0))
                hookurl = '{}{}/{}/'.format(webhook_site, webhook_base, token)
                setted = bot.setWebhook(hookurl, certificate=certificate, timeout=timeout, max_connections=max_connections, allowed_updates=allowed_updates)
                webhook_info = bot.getWebhookInfo()
                real_allowed = webhook_info.allowed_updates if webhook_info.allowed_updates else ["ALL"]
                bot.more_info = webhook_info
                logger.info('Telegram Bot <{}> setting webhook [ {} ] max connections:{} allowed updates:{} pending updates:{} : {}'.format(bot.username, webhook_info.url, webhook_info.max_connections, real_allowed, webhook_info.pending_update_count, setted))
            else:
                updater = Updater(token=token)
                bot = updater.bot
                bot.delete_webhook()
                DjangoTelegramBot.updaters.append(updater)
                DjangoTelegramBot.dispatchers.append(updater.dispatcher)
                DjangoTelegramBot.__used_tokens.add(token)

            DjangoTelegramBot.bots.append(bot)
            DjangoTelegramBot.bot_tokens.append(token)
            DjangoTelegramBot.bot_usernames.append(bot.username)


        logger.debug('Telegram Bot <{}> set as default bot'.format(DjangoTelegramBot.bots[0].username))

        def module_exists(module_name, method_name, execute):
            try:
                m = importlib.import_module(module_name)
                if execute and hasattr(m, method_name):
                    logger.debug('Run {}.{}()'.format(module_name,method_name))
                    getattr(m, method_name)()
                else:
                    logger.debug('Run {}'.format(module_name))

            except ImportError as er:
                logger.debug('{} : {}'.format(module_name, repr(er)))
                return False

            return True

        # import telegram bot handlers for all INSTALLED_APPS
        for app_config in apps.get_app_configs():
            if module_has_submodule(app_config.module, TELEGRAM_BOT_MODULE_NAME):
                module_name = '%s.%s' % (app_config.name, TELEGRAM_BOT_MODULE_NAME)
                if module_exists(module_name, 'main', True):
                    logger.info('Loaded {}'.format(module_name))

        num_bots=len(DjangoTelegramBot.__used_tokens)
        if self.mode == POLLING_MODE and num_bots>0:
            logger.info('Please manually start polling update for {0} bot{1}. Run command{1}:'.format(num_bots, 's' if num_bots>1 else ''))
            for token in DjangoTelegramBot.__used_tokens:
                updater = DjangoTelegramBot.get_updater(bot_id=token)
                logger.info('python manage.py botpolling --username={}'.format(updater.bot.username))





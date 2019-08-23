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
from telegram.error import InvalidToken, TelegramError
from telegram.utils.request import Request
from telegram.ext import messagequeue as mq
from .mqbot import MQBot
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
        if settings.DJANGO_TELEGRAMBOT.get('MODE', 'WEBHOOK') == 'POLLING':
            self.mode = POLLING_MODE

        modes = ['WEBHOOK','POLLING']
        logger.info('Django Telegram Bot <{} mode>'.format(modes[self.mode]))

        bots_list = settings.DJANGO_TELEGRAMBOT.get('BOTS', [])

        if self.mode == WEBHOOK_MODE:
            webhook_site = settings.DJANGO_TELEGRAMBOT.get('WEBHOOK_SITE', None)
            if not webhook_site:
                logger.warn('Required TELEGRAM_WEBHOOK_SITE missing in settings')
                return
            if webhook_site.endswith("/"):
                webhook_site = webhook_site[:-1]

            webhook_base = settings.DJANGO_TELEGRAMBOT.get('WEBHOOK_PREFIX','/')
            if webhook_base.startswith("/"):
                webhook_base = webhook_base[1:]
            if webhook_base.endswith("/"):
                webhook_base = webhook_base[:-1]

            cert = settings.DJANGO_TELEGRAMBOT.get('WEBHOOK_CERTIFICATE', None)
            certificate = None
            if cert and os.path.exists(cert):
                logger.info('WEBHOOK_CERTIFICATE found in {}'.format(cert))
                certificate=open(cert, 'rb')
            elif cert:
                logger.error('WEBHOOK_CERTIFICATE not found in {} '.format(cert))

        for b in bots_list:
            token = b.get('TOKEN', None)
            if not token:
                break

            allowed_updates = b.get('ALLOWED_UPDATES', None)
            timeout = b.get('TIMEOUT', None)
            proxy = b.get('PROXY', None)
            
            if self.mode == WEBHOOK_MODE:
                try:
                    if b.get('MESSAGEQUEUE_ENABLED',False):
                        q = mq.MessageQueue(all_burst_limit=b.get('MESSAGEQUEUE_ALL_BURST_LIMIT',29),
                        all_time_limit_ms=b.get('MESSAGEQUEUE_ALL_TIME_LIMIT_MS',1024))
                        if proxy:
                            request = Request(proxy_url=proxy['proxy_url'], urllib3_proxy_kwargs=proxy['urllib3_proxy_kwargs'], con_pool_size=b.get('MESSAGEQUEUE_REQUEST_CON_POOL_SIZE',8))
                        else:
                            request = Request(con_pool_size=b.get('MESSAGEQUEUE_REQUEST_CON_POOL_SIZE',8))
                        bot = MQBot(q, token=token, request=request)
                    else:
                        request = None
                        if proxy:
                            request = Request(proxy_url=proxy['proxy_url'], urllib3_proxy_kwargs=proxy['urllib3_proxy_kwargs'])
                        bot = telegram.Bot(token=token, request=request)
                        
                    DjangoTelegramBot.dispatchers.append(Dispatcher(bot, None, workers=0))
                    hookurl = '{}/{}/{}/'.format(webhook_site, webhook_base, token)
                    max_connections = b.get('WEBHOOK_MAX_CONNECTIONS', 40)
                    setted = bot.setWebhook(hookurl, certificate=certificate, timeout=timeout, max_connections=max_connections, allowed_updates=allowed_updates)
                    webhook_info = bot.getWebhookInfo()
                    real_allowed = webhook_info.allowed_updates if webhook_info.allowed_updates else ["ALL"]

                    bot.more_info = webhook_info
                    logger.info('Telegram Bot <{}> setting webhook [ {} ] max connections:{} allowed updates:{} pending updates:{} : {}'.format(bot.username, webhook_info.url, webhook_info.max_connections, real_allowed, webhook_info.pending_update_count, setted))

                except InvalidToken:
                    logger.error('Invalid Token : {}'.format(token))
                    return
                except TelegramError as er:
                    logger.error('Error : {}'.format(repr(er)))
                    return

            else:
                try:
                    updater = Updater(token=token, request_kwargs=proxy)
                    bot = updater.bot
                    bot.delete_webhook()
                    DjangoTelegramBot.updaters.append(updater)
                    DjangoTelegramBot.dispatchers.append(updater.dispatcher)
                    DjangoTelegramBot.__used_tokens.add(token)
                except InvalidToken:
                    logger.error('Invalid Token : {}'.format(token))
                    return
                except TelegramError as er:
                    logger.error('Error : {}'.format(repr(er)))
                    return

            DjangoTelegramBot.bots.append(bot)
            DjangoTelegramBot.bot_tokens.append(token)
            DjangoTelegramBot.bot_usernames.append(bot.username)


        logger.debug('Telegram Bot <{}> set as default bot'.format(DjangoTelegramBot.bots[0].username))

        def module_imported(module_name, method_name, execute):
            try:
                m = importlib.import_module(module_name)
                if execute and hasattr(m, method_name):
                    logger.debug('Run {}.{}()'.format(module_name,method_name))
                    getattr(m, method_name)()
                else:
                    logger.debug('Run {}'.format(module_name))

            except ImportError as er:
                if settings.DJANGO_TELEGRAMBOT.get('STRICT_INIT'):
                    raise er
                else:
                    logger.error('{} : {}'.format(module_name, repr(er)))
                    return False

            return True

        # import telegram bot handlers for all INSTALLED_APPS
        for app_config in apps.get_app_configs():
            if module_has_submodule(app_config.module, TELEGRAM_BOT_MODULE_NAME):
                module_name = '%s.%s' % (app_config.name, TELEGRAM_BOT_MODULE_NAME)
                if module_imported(module_name, 'main', True):
                    logger.info('Loaded {}'.format(module_name))

        num_bots=len(DjangoTelegramBot.__used_tokens)
        if self.mode == POLLING_MODE and num_bots>0:
            logger.info('Please manually start polling update for {0} bot{1}. Run command{1}:'.format(num_bots, 's' if num_bots>1 else ''))
            for token in DjangoTelegramBot.__used_tokens:
                updater = DjangoTelegramBot.get_updater(bot_id=token)
                logger.info('python manage.py botpolling --username={}'.format(updater.bot.username))

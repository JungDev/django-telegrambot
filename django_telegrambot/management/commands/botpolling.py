import logging

from django.core.management.base import BaseCommand
#from telegram.ext import Updater

from django_telegrambot.apps import DjangoTelegramBot


class Command(BaseCommand):
    help = "Run telegram bot in polling mode"
    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('--username', '-i', help="Bot username", default=None)
        parser.add_argument('--token', '-t', help="Bot token", default=None)
        pass

    def get_updater(self, username=None, token=None):
        updater = None
        if username is not None:
            updater = DjangoTelegramBot.get_updater(bot_id=username)
            if not updater:
                self.stderr.write("Cannot find default bot with username {}".format(username))
        elif token:
            updater = DjangoTelegramBot.get_updater(bot_id=token)
            if not updater:
                self.stderr.write("Cannot find bot with token {}".format(token))
        return updater

    def handle(self, *args, **options):
        from django.conf import settings
        if settings.DJANGO_TELEGRAMBOT.get('MODE', 'WEBHOOK') == 'WEBHOOK':
            self.stderr.write("Webhook mode active in settings.py, change in POLLING if you want use polling update")
            return

        updater = self.get_updater(username=options.get('username'), token=options.get('token'))
        if not updater:
            self.stderr.write("Bot not found")
            return
        # Enable Logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)
        logger = logging.getLogger("telegrambot")
        logger.setLevel(logging.INFO)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(console)


        bots_list = settings.DJANGO_TELEGRAMBOT.get('BOTS', [])
        b = None
        for bot_set in bots_list:
            if bot_set.get('TOKEN', None) == updater.bot.token:
                b = bot_set
                break
        if not b:
            self.stderr.write("Cannot find bot settings")
            return

        allowed_updates = b.get('ALLOWED_UPDATES', None)
        timeout = b.get('TIMEOUT', 10)
        poll_interval = b.get('POLL_INTERVAL', 0.0)
        clean = b.get('POLL_CLEAN', False)
        bootstrap_retries = b.get('POLL_BOOTSTRAP_RETRIES', 0)
        read_latency = b.get('POLL_READ_LATENCY', 2.)

        self.stdout.write("Run polling...")
        updater.start_polling(poll_interval=poll_interval,
                      timeout=timeout,
                      clean=clean,
                      bootstrap_retries=bootstrap_retries,
                      read_latency=read_latency,
                      allowed_updates=allowed_updates)
        self.stdout.write("the bot is started and runs until we press Ctrl-C on the command line.")
        updater.idle()
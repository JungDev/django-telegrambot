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
        if not settings.TELEGRAM_BOT_MODE == 'POLLING':
            self.stderr.write("Webhook mode active, change it in your settings if you want use polling update")
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

        #wbinfo = updater.bot.getWebhookInfo()
        #logger.warn(wbinfo)
        #updater.bot.deleteWebhook() #not yet present in python-telegram-bot 5.3.1
        self.stdout.write("Run polling...")
        updater.start_polling()
        self.stdout.write("the bot is started and runs until we press Ctrl-C on the command line.")
        updater.idle()
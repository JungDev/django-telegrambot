import logging

from django.apps.registry import Apps
from django.test import TestCase
from django_telegrambot.apps import DjangoTelegramBot
import mock

logging.basicConfig(level=logging.INFO)


# Need to mock some of the Telegram Bot's methods with dummy values to make
# sure that the initialisation completes with mock credentials.
@mock.patch('telegram.bot.Bot.delete_webhook', lambda bot: None)
@mock.patch('telegram.bot.Bot.username', 'mock_bot')
@mock.patch('django_telegrambot.apps.DjangoTelegramBot.ready_run', False)
@mock.patch('django_telegrambot.apps.logger')
class TestDjangoTelegramBot(TestCase):

    def setUp(self):
        self.app = DjangoTelegramBot.create('django_telegrambot')

    @mock.patch('django_telegrambot.apps.apps',
                Apps(installed_apps=('tests.test_app',)))
    def test_good_app_loading(self, log):
        """Normal initialisation - should complete without error messages."""
        self.assertFalse(DjangoTelegramBot.ready_run)
        self.app.ready()
        self.assertEquals(log.error.call_count, 0)
        self.assertTrue(DjangoTelegramBot.ready_run)

    @mock.patch('django_telegrambot.apps.apps',
                Apps(installed_apps=('tests.test_bad_app',)))
    def test_bad_app_loading(self, log):
        """If a telegrambot.py module in some of the apps contains a mistake,
        an error message should be loaded."""
        self.app.ready()
        self.assertEquals(log.error.call_count, 1)

    @mock.patch('django_telegrambot.apps.apps',
                Apps(installed_apps=('tests.test_bad_app',)))
    @mock.patch.dict('django_telegrambot.apps.settings.DJANGO_TELEGRAMBOT',
                     STRICT_INIT=True)
    def test_bad_app_loading_strict(self, _):
        """With STRICT_INIT set to true in the DJANGO_TELEGRAMBOT settings, the
        app must not start if the telegrambot.py files are not imported
        successfully."""
        with self.assertRaises(ImportError):
            self.app.ready()

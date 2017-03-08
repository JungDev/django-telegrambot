=============================
django-telegrambot
=============================

.. image:: https://badge.fury.io/py/django-telegrambot.png
    :target: https://badge.fury.io/py/django-telegrambot

.. image:: https://travis-ci.org/JungDev/django-telegrambot.png?branch=master
    :target: https://travis-ci.org/JungDev/django-telegrambot

A simple app to develop Telegram bots with Django

Documentation
-------------

The full documentation is at https://django-telegrambot.readthedocs.org.

Quickstart
----------

Install django-telegrambot::

    pip install django-telegrambot

Configure your installation
---------------------------

Add ``django_telegrambot`` in ``INSTALLED_APPS`` ::

       #settings.py
       INSTALLED_APPS = (
           ...
           'django_telegrambot',
           ...
       )

And set your bots::

        #settings.py
        #Django Telegram Bot settings
        TELEGRAM_BOT_TOKENS = ('BOT_1_token','BOT_2_token',)
        TELEGRAM_WEBHOOK_SITE = 'https://mysite.it'
        TELEGRAM_WEBHOOK_BASE = '/baseurl'
        #TELEGRAM_WEBHOOK_CERTIFICATE = 'cert.pem' #If your site use self-signed certificate, must be set with location of your public key certificate. (More info at https://core.telegram.org/bots/self-signed )


Include in your urls.py the ``django_telegrambot.urls`` using the same value of ``TELEGRAM_WEBHOOK_BASE`` ::

        #urls.py
        urlpatterns = [
            ...
            url(r'^baseurl/', include('django_telegrambot.urls')),
            ...
        ]

Then use it in a project creating a module ``telegrambot.py`` in your app ::

        #myapp/telegrambot.py
        # Example code for telegrambot.py module
        from telegram.ext import CommandHandler, MessageHandler, Filters
        from django_telegrambot.apps import DjangoTelegramBot

        import logging
        logger = logging.getLogger(__name__)


        # Define a few command handlers. These usually take the two arguments bot and
        # update. Error handlers also receive the raised TelegramError object in error.
        def start(bot, update):
            bot.sendMessage(update.message.chat_id, text='Hi!')


        def help(bot, update):
            bot.sendMessage(update.message.chat_id, text='Help!')


        def echo(bot, update):
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
            dp.add_handler(CommandHandler("start", start))
            dp.add_handler(CommandHandler("help", help))

            # on noncommand i.e message - echo the message on Telegram
            dp.add_handler(MessageHandler([Filters.text], echo))

            # log all errors
            dp.add_error_handler(error)

            # log all errors
            dp.addErrorHandler(error)



Features
--------

* Multiple bots

Contributing
------------

Patches and bug reports are welcome, just please keep the style consistent with the original source.

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python runtests.py

Sample Application
------------------
There a sample application in `sampleproject` directory. Here is installation instructions:

1. Install requirements with command

        pip install -r requirements.txt
2. Copy file `local_settings.sample.py` as `local_settings.py` and edit your bot token

        cp sampleproject/local_settings.sample.py sampleproject/local_settings.py

        nano sampleproject/local_settings.py
3. Run Django migrations

        python manage.py migrate
4. Run server

        python manage.py runserver
5. To test webhook locally install `ngrok` application and run command

        ./ngrok http 8000
And change TELEGRAM_WEBHOOK_SITE and ALLOWED_HOSTS in local_settings.py file

Credits
---------
Required package:
* `Python Telegram Bot`_

.. _`Python Telegram Bot`: https://github.com/python-telegram-bot/python-telegram-bot

Tools used in rendering this package:

*  Cookiecutter_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter


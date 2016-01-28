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
        from django_telegrambot.apps import DjangoTelegramBot 

        def start(bot, update):
            bot.sendMessage(update.message.chat_id, text='Hi!')
        
        def help(bot, update):
            bot.sendMessage(update.message.chat_id, text='Help!')
        
        def echo(bot, update):
            bot.sendMessage(update.message.chat_id, text=update.message.text)
        
        def error(bot, update, error):
            logger.warn('Update "%s" caused error "%s"' % (update, error))
            
        
        def main():
            print "Handlers for telegram bot"
            
            #Utilizzare questa variabile per ottenere il dispatcher relativo al default bot
            dp = DjangoTelegramBot.dispatcher
            
            # in alternativa si può selezionare quale bot usare utilizzando la seguente funzione:
            '''
            dp = DjangoTelegramBot.getDispatcher('BOT_2_token')     #by bot
            dp = DjangoTelegramBot.getDispatcher('BOT_2_username')  #by bot username

            '''
            
            # on different commands - answer in Telegram
            dp.addTelegramCommandHandler("start", start)
            dp.addTelegramCommandHandler("help", help)
        
            # on noncommand i.e message - echo the message on Telegram
            dp.addTelegramMessageHandler(echo)
        
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

Credits
---------
Required package:
* `Python Telegram Bot`_

.. _`Python Telegram Bot`: https://github.com/python-telegram-bot/python-telegram-bot

Tools used in rendering this package:

*  Cookiecutter_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter


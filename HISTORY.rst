.. :changelog:

History
-------
1.1.0 (unreleased)
++++++++++++++++++
* Fix error on startup when using ``MESSAGEQUEUE_ENABLED`` [Nachatlb]

1.0.0 (2017-05-25)
++++++++++++++++++
* IMPORTANT: If you upgrade from a previous version, you MUST change how to include django_telegrambot.urls and settings.py.
* Added admin dashboard, available at /admin/django-telegrambot
* Added polling mode from management command (an easy to way to run bot in local machine, not recommended in production)
* More setting available
* Improved AppConfig
* Improved sample project

0.2.6 (2017-04-08)
++++++++++++++++++
* Improved module loading
* Added sample project

0.2.5 (2017-03-06)
++++++++++++++++++
* Fix compatibility with python-telegram-bot 5.1

0.2.4 (2016-10-04)
++++++++++++++++++
* Fix compatibility with Django 1.10

0.2.3 (2016-07-30)
++++++++++++++++++
* Fix default dispatcher and bot

0.2.2 (2016-07-27)
++++++++++++++++++
* Fix multi workers

0.2.1 (2016-07-24)
++++++++++++++++++
* Update for python-telegram-bot release v5.0

0.2.0 (2016-04-27)
++++++++++++++++++

* Update for python-telegram-bot release v4.0.1

0.1.8 (2016-03-22)
++++++++++++++++++

* Update for deprecation in python-telegram-bot release v3.4

0.1.5 (2016-01-28)
++++++++++++++++++

* Fix compatibility.

0.1.4 (2016-01-28)
++++++++++++++++++

* Fix compatibility.

0.1.3 (2016-01-28)
++++++++++++++++++

* Fix setting certificate.
* Add method DjangoTelegramBot.getBot(); get bot instance by token or username.

0.1.2 (2016-01-26)
++++++++++++++++++

* First release on PyPI.


from django.urls import re_path
from . import views
from django.conf import settings

webhook_base = settings.DJANGO_TELEGRAMBOT.get('WEBHOOK_PREFIX','/')
if webhook_base.startswith("/"):
    webhook_base = webhook_base[1:]
if not webhook_base.endswith("/"):
    webhook_base += "/"

urlpatterns = [
    re_path(r'admin/django-telegrambot/$', views.home, name='django-telegrambot'),
    re_path(r'{}(?P<bot_token>.+?)/$'.format(webhook_base), views.webhook, name='webhook'),
]

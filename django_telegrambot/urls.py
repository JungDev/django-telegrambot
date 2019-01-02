
from django.urls import path, re_path
from . import views
from django.conf import settings

webhook_base = settings.DJANGO_TELEGRAMBOT.get('WEBHOOK_PREFIX', '')
if webhook_base.startswith("/"):
    webhook_base = webhook_base[1:]
if webhook_base is not '' and not webhook_base.endswith("/"):
    webhook_base += "/"

urlpatterns = [
    path('admin/django-telegrambot/', views.home, name='django-telegrambot'),
    re_path('{}(?P<bot_token>[-_:a-zA-Z0-9]+)/'.format(webhook_base), views.webhook, name='webhook'),
]

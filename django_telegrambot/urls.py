
from django.conf.urls import url, include, patterns
from . import views

urlpatterns = [
    url(r'(?P<bot_token>.+?)/$', views.webhook, name='webhook'),
]
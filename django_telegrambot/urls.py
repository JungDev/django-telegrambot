
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'(?P<bot_token>.+?)/$', views.webhook, name='webhook'),
]

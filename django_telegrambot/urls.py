
from django.conf.urls import url, include, patterns
from views import webhook

urlpatterns = [
    url(r'(?P<bot_token>.+?)/$', webhook, name='webhook'),
]
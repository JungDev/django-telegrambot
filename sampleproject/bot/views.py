from django.shortcuts import render
from django_telegrambot.apps import DjangoTelegramBot

# Create your views here.
def index(request):
    bot_list = DjangoTelegramBot.bots
    context = {'bot_list': bot_list}
    return render(request, 'bot/index.html', context)

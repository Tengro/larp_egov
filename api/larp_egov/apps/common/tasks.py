from larp_egov import celery_app
import requests
from django_telegrambot.apps import DjangoTelegramBot


@celery_app.task
def refresh_hook():
    token = DjangoTelegramBot.dispatcher.bot.token
    requests.get(f"https://api.telegram.org/bot{token}/setWebhook?url=https://atomlarp.com/bot/{token}/")

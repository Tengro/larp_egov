from larp_egov import celery_app
import requests
from django_telegrambot.apps import DjangoTelegramBot
from larp_egov.apps.accounts.models import UserAccount


@celery_app.task
def refresh_hook():
    token = DjangoTelegramBot.dispatcher.bot.token
    requests.get(f"https://api.telegram.org/bot{token}/setWebhook?url=https://atomlarp.com/bot/{token}/")
    UserAccount.objects.get_service_account().send_message('Hook refreshed')

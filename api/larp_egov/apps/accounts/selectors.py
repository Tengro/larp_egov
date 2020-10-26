from django.db.models import Q
from larp_egov.apps.accounts.models import UserAccount


def get_all_users():
    return UserAccount.objects.active()


def get_user_by_character_id(character_id):
    return UserAccount.objects.active().filter(character_id=character_id).first()


def get_all_admins():
    return UserAccount.objects.filter(Q(is_staff=True) | Q(is_superuser=True))


def get_user_by_telegram_id(telegram_id):
    return UserAccount.objects.active().filter(character_id=character_id).first()


def get_all_characters_in_game():
    return UserAccount.objects.active().exclude(is_staff=True).exclude(is_superuser=True).exclude(is_corporate_fiction_account=True)

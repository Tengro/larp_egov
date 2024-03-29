from larp_egov.apps.accounts.selectors import (
    get_user_by_character_id, get_user_by_telegram_id,
)
from django.utils.translation import ugettext_lazy as _
from larp_egov.apps.banking.models import BankSubscription, BankUserSubscriptionIntermediary
from larp_egov.apps.common.bot_commands._common_texts import UNREGISTERED, NO_SUBSCRIPTION, NO_ACCESS_COMMAND, NO_ACCESS_DATA, validate_police


def display_all_subscriptions(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    return "\n\n".join([x.display for x in BankSubscription.objects.all()])


def display_own_subscriptions(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    return "\n\n".join([x.display for x in requester.bankusersubscriptionintermediary_set.all()])


def display_user_subscriptions(update, override_permissions=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    code = update.message.text[22:]
    user = get_user_by_character_id(code)
    if not user:
        return NO_USER
    if not validate_police(requester):
        return NO_ACCESS_DATA
    return "\n\n".join([x.display for x in user.bankusersubscriptionintermediary_set.all()])


def approve_user_subscription(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    code = update.message.text[22:]
    subscription = BankUserSubscriptionIntermediary.objects.filter(subscription_request_id=code).first()
    if not subscription:
        return NO_SUBSCRIPTION
    try:
        subscription.approve_subscription(requester)
    except ValueError as e:
        return f"{e}"


def user_request_subscription(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    code = update.message.text[22:]
    subscription = BankSubscription.objects.filter(subscription_id=code).first()
    if not subscription:
        return NO_SUBSCRIPTION
    if BankUserSubscriptionIntermediary.objects.filter(subscriber=requester, subscription=subscription).exists():
        return _("You are already subscribed!")
    subscription.create_subscription(requester)


def user_stop_subscription(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    code = update.message.text[13:]
    subscription = BankSubscription.objects.filter(subscription_id=code).first()
    if not subscription:
        return NO_SUBSCRIPTION
    subscription.cancel_subscription(requester)


def user_forced_subscription_stop(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not requester.is_staff:
        return NO_ACCESS_COMMAND
    message = update.message.text[19:]
    user_code, subscription = message.split(' ')
    user = get_user_by_character_id(user_code)
    if not user:
        return NO_USER
    subscription = BankSubscription.objects.filter(subscription_id=subscription).first()
    if not subscription:
        return NO_SUBSCRIPTION
    subscription.cancel_subscription(user, forced=True)

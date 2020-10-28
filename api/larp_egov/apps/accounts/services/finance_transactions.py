import decimal
from larp_egov.apps.accounts.selectors import (
    get_user_by_character_id, get_user_by_telegram_id,
)
from larp_egov.apps.banking.models import BankTransaction
from ._common_texts import UNREGISTERED, NO_ACCESS_DATA, NO_USER, validate_security


def get_own_bank_data(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    return '\n\n'.join(
        [
            x.user_transaction_log(requester) for x in BankTransaction.objects.get_user_bank_history(requester).order_by('created')
        ]
    )


def get_full_bank_data(update, override_permissions=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not validate_security(requester) and not override_permissions:
        return NO_ACCESS_DATA
    return '\n\n'.join(
        [
            x.transaction_log for x in BankTransaction.objects.all().order_by('created')
        ]
    )


def get_user_bank_data(update, override_permissions=False, is_full=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not validate_security(requester) and not override_permissions:
        return NO_ACCESS_DATA
    code = update.message.text[23:]
    user = get_user_by_character_id(code)
    if not user:
        return NO_USER
    if not is_full:
        return '\n\n'.join(
            [
                x.user_transaction_log(user) for x in BankTransaction.objects.get_user_bank_history(requester).order_by('created')
            ]
        )
    return '\n\n'.join(
            [
                x.transaction_Log for x in BankTransaction.objects.get_user_bank_history(requester).order_by('created')
            ]
        )


def create_transaction(update, is_anonymous=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    message = update.message.text[6:]
    user_code, amount = message.split(' ')
    user = get_user_by_character_id(user_code)
    if not user:
        return "Can\'t find user in database; transaction not sent"
    try:
        amount = decimal.Decimal(amount)
    except decimal.InvalidOperation:
        return "Incorrect amount!"
    try:
        BankTransaction.create_transaction(requester, user, amount, is_anonymous)
    except ValueError as e:
        return f'{e}'


def cancel_transaction(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    transaction_id = update.message.text[8:]
    transaction = BankTransaction.objects.unresolved().filter(sender=requester).filter(transaction_id=transaction_id).first()
    if not transaction:
        return "Can\'t cancel transaction of selected UUID; check status/UUID"
    transaction.cancel_transaction()

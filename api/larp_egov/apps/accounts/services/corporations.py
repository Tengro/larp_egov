import decimal
from larp_egov.apps.accounts.selectors import (
    get_user_by_character_id, get_user_by_telegram_id,
)
from larp_egov.apps.banking.models import Corporation, CorporationMembership
from ._common_texts import UNREGISTERED, NO_USER, NO_SUBSCRIPTION, NO_ACCESS_COMMAND, NO_ACCESS_DATA, NO_CORP, validate_police, validate_security


def display_all_corporations(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    return "\n\n".join([x.display for x in Corporation.objects.all()])


def display_own_corporations(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    return "\n\n".join([x.display for x in CorporationMembership.objects.filter(member=requester)])


def display_user_corporations(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    code = update.message.text[21:]
    user = get_user_by_character_id(code)
    if not user:
        return NO_USER
    if not validate_police(user) and not override_permissions:
        return NO_ACCESS_DATA
    return "\n\n".join([x.display for x in CorporationMembership.objects.filter(member=user)])


def display_corporation_members(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    code = update.message.text[21:]
    corproration = Corporation.objects.filter(linked_account__character_id=code).first()
    if not corproration:
        return NO_CORP
    return corproration.display_members(requester)


def security_display_corporation_members(update, override_permissions=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    code = update.message.text[30:]
    corproration = Corporation.objects.filter(linked_account__character_id=code).first()
    if not corproration:
        return NO_CORP
    if not validate_security(requester):
        return NO_ACCESS_DATA
    return corproration.display_members(requester, override_access=True)


def make_corporation_withdrawal(update, override_permissions=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    message = update.message.text[22:]
    code, amount = message.split(' ')
    corproration = Corporation.objects.filter(linked_account__character_id=code).first()
    if not corproration:
        return NO_CORP
    try:
        amount = decimal.Decimal(amount)
    except decimal.InvalidOperation:
        return "Incorrect amount!"
    try:
        corproration.withdraw_funds(requester, amount)
    except ValueError as e:
        return f'{e}'


def make_corporation_deposit(update, override_permissions=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    message = update.message.text[21:]
    code, amount = message.split(' ')
    corproration = Corporation.objects.filter(linked_account__character_id=code).first()
    if not corproration:
        return NO_CORP
    try:
        amount = decimal.Decimal(amount)
    except decimal.InvalidOperation:
        return "Incorrect amount!"
    try:
        corproration.deposit_funds(requester, amount)
    except ValueError as e:
        return f'{e}'


def display_corporation_financial_history(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    code = update.message.text[21:]
    corproration = Corporation.objects.filter(linked_account__character_id=code).first()
    if not corproration:
        return NO_CORP
    return corproration.display_transaction_history(requester)


def display_security_corporation_financial_history(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not validate_security(requester) and not override_permissions:
        return NO_ACCESS_DATA
    code = update.message.text[30:]
    corproration = Corporation.objects.filter(linked_account__character_id=code).first()
    if not corproration:
        return NO_CORP
    return corproration.display_transaction_history(requester, override_access=True)


def _corporation_preparation(update, number_to_skip, function_name):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    code, corp_code = update.message.text[24:].split(' ')
    user = get_user_by_character_id(code)
    if not user:
        return NO_USER
    corproration = Corporation.objects.filter(linked_account__character_id=code).first()
    if not corproration:
        return NO_CORP
    getattr(corproration, function_name)(requester, user)


def add_user_to_corporation(update):
    result = _corporation_preparation(update, 24, 'add_user')
    if result:
        return result


def kick_user_from_corporation(update):
    result = _corporation_preparation(update, 27, 'remove_user')
    if result:
        return result


def promote_user_in_corporation(update):
    result = _corporation_preparation(update, 28, 'promote_user')
    if result:
        return result


def demote_user_in_corporation(update):
    result = _corporation_preparation(update, 27, 'demote_user')
    if result:
        return result

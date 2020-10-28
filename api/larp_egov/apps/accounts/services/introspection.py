from larp_egov.apps.accounts.selectors import (
    get_user_by_character_id, get_user_by_telegram_id,
    get_all_characters_in_game
)
from ._common_texts import UNREGISTERED, NO_ACCESS_DATA, NO_USER


def validate_police(character):
    return (character.is_police or character.is_security)


def validate_security(character):
    return character.is_security


def get_introspection(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    return requester.get_user_introspect()


def get_master_user_data(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not requester.is_staff:
        return NO_ACCESS_DATA
    code = update.message.text[13:]
    user = get_user_by_character_id(code)
    if not user:
        return NO_USER
    return user.get_full_user_introspect()


def get_public_data(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    code = update.message.text[15:]
    user = get_user_by_character_id(code)
    if not user:
        return NO_USER
    return user.common_introspect_data


def get_police_data(update, override_permissions=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not override_permissions and not validate_police(requester):
        return NO_ACCESS_DATA
    code = update.message.text[15:]
    user = get_user_by_character_id(code)
    if not user:
        return NO_USER
    return user.get_user_police_data()


def get_security_data(update, override_permissions=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not override_permissions and not validate_security(requester):
        return NO_ACCESS_DATA
    code = update.message.text[17:]
    user = get_user_by_character_id(code)
    if not user:
        return NO_USER
    return user.get_user_security_data()


def get_master_user_list(update, override_permissions=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not override_permissions and not requester.is_staff:
        return NO_ACCESS_DATA
    all_users = get_all_characters_in_game()
    user_data = [x.display_data for x in all_users]
    return '\n'.join(user_data)

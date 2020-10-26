from larp_egov.apps.accounts.selectors import (
    get_user_by_character_id, get_user_by_telegram_id,
    get_all_characters_in_game
)


def validate_police(character):
    return (character.is_police or character.is_security)


def validate_security(character):
    return character.is_security


def get_introspection(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    return requester.get_user_introspect()


def get_master_user_data(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    if not requester.is_staff:
        return "You have no access to this data"
    code = update.message.text[14:]
    user = get_user_by_character_id(code)
    if not user:
        return "No such user exists"
    return user.__dict__


def get_public_data(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    code = update.message.text[15:]
    user = get_user_by_character_id(code)
    if not user:
        return "No such user exists"
    return user.common_introspect_data


def get_police_data(update, override_permissions=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    if not override_permissions and not validate_police(requester):
        return "You have no access to this data"
    code = update.message.text[15:]
    user = get_user_by_character_id(code)
    if not user:
        return "No such user exists"
    return user.get_user_police_data()


def get_security_data(update, override_permissions=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    if not override_permissions and not validate_security(requester):
        return "You have no access to this data"
    code = update.message.text[17:]
    user = get_user_by_character_id(code)
    if not user:
        return "No such user exists"
    return user.get_user_security_data()


def get_master_user_list(update, override_permissions=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    if not override_permissions and not requester.is_staff:
        return "You have no access to this data"
    all_users = get_all_characters_in_game()
    user_data = [x.display_data for x in all_users]
    return '\n'.join(user_data)
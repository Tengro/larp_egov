from larp_egov.apps.accounts.selectors import get_user_by_character_id, get_user_by_telegram_id


def bind_user(update):
    code = update.message.text[10:]
    user = get_user_by_character_id(code)
    telegram_id = update.message.chat_id
    if user is None:
        return (False, "Немає такого користувача")
    if user.telegram_id is not None:
        return (False, "Уже зареєстровано")
    tg_user = get_user_by_telegram_id(telegram_id)
    if tg_user is not None:
        return (False, "Уже зареєстровано")
    user.telegram_id = telegram_id
    user.save()
    return (True, user)


def delete_user(update):
    code = update.message.text[8:]
    user = get_user_by_character_id(code)
    if user is None:
        return (False, "Немає такого користувача")
    tg_id = user.telegram_id
    user.delete()
    return (True, tg_id)


def verify_user(update):
    code = update.message.text[8:]
    user = get_user_by_character_id(code)
    if user is None:
        return (False, "No such user")
    if user.is_verified:
        return (False, "Already verified")
    user.is_verified = True
    user.save()
    return (True, user)

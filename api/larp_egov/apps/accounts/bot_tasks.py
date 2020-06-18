from larp_egov.apps.accounts.selectors import get_all_admins


def notify_admins(bot, user):
    admins = get_all_admins()
    for admin in admins:
        bot.sendMessage(
            admin.telegram_id,
            f"User {user.get_full_name()}, character ID {user.character_id}, successfully registered"
        )

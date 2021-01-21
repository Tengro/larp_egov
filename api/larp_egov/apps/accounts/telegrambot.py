from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot
from larp_egov.apps.accounts.services.deeplink import bind_user, delete_user, verify_user
from larp_egov.apps.accounts.bot_tasks import notify_admins
from larp_egov.apps.accounts.bot_commands.introspection import (
    get_introspection, get_police_data, get_security_data,
    get_public_data, get_master_user_list, get_master_user_data
)

import logging
logger = logging.getLogger(__name__)


def help(update, context):
    context.bot.sendMessage(update.message.chat_id, text='Help!')


def register(update, context):
    success, result = bind_user(update)
    if not success:
        context.bot.sendMessage(update.message.chat_id, text=result)
        return
    notify_admins(context.bot, result)
    context.bot.sendMessage(update.message.chat_id, text="You've been successfully linked; await for verification")


def verify(update, context):
    success, result = verify_user(update)
    if not success:
        context.bot.sendMessage(update.message.chat_id, text=result)
        return
    context.bot.sendMessage(result.telegram_id, text="Your character was successfully verified")


def delete(update, context):
    success, result = delete_user(update)
    if not success:
        context.bot.sendMessage(update.message.chat_id, text=result)
        return
    context.bot.sendMessage(result, text="Your character was deleted by administration")


# introspection and general data
def get_master_data(update, context):
    context.bot.sendMessage(update.message.chat_id, text=get_master_user_data(update))


def get_user_introspection(update, context):
    context.bot.sendMessage(update.message.chat_id, text=get_introspection(update))


def get_public_record(update, context):
    context.bot.sendMessage(update.message.chat_id, text=get_public_data(update))


def get_security_record(update, context):
    context.bot.sendMessage(update.message.chat_id, text=get_security_data(update))


def get_police_personal_record(update, context):
    context.bot.sendMessage(update.message.chat_id, text=get_police_data(update))


def get_user_list(update, context):
    context.bot.sendMessage(update.message.chat_id, text=get_master_user_list(update))


def error(update, error):
    from accounts.models import UserAccount
    user = UserAccount.objects.get_service_account()
    user.send_message(f"Update {update} caused error {error}")
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    logger.info("Loading handlers for telegram bot")

    dp = DjangoTelegramBot.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("verify", verify))
    dp.add_handler(CommandHandler("delete", delete))
    # introspections: CHECKED
    dp.add_handler(CommandHandler("my_record", get_user_introspection))
    dp.add_handler(CommandHandler("public_record", get_public_record))
    dp.add_handler(CommandHandler("police_record", get_police_personal_record))
    dp.add_handler(CommandHandler("security_record", get_security_record))
    dp.add_handler(CommandHandler("master_data", get_master_data))
    dp.add_handler(CommandHandler("user_list", get_user_list))
    # log all errors
    dp.add_error_handler(error)

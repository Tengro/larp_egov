from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot
from larp_egov.apps.accounts.services.deeplink import bind_user, delete_user, verify_user
from larp_egov.apps.accounts.bot_tasks import notify_admins
from larp_egov.apps.accounts.services.introspection import (
    get_introspection, get_police_data, get_security_data,
    get_public_data, get_master_user_list, get_master_user_data
)

import logging
logger = logging.getLogger(__name__)


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def register(bot, update):
    success, result = bind_user(update)
    if not success:
        bot.sendMessage(update.message.chat_id, text=result)
        return
    notify_admins(bot, result)
    bot.sendMessage(update.message.chat_id, text="You've been successfully linked; await for verification")


def verify(bot, update):
    success, result = verify_user(update)
    if not success:
        bot.sendMessage(update.message.chat_id, text=result)
        return
    bot.sendMessage(result.telegram_id, text="Your character was successfully verified")


def delete(bot, update):
    success, result = delete_user(update)
    if not success:
        bot.sendMessage(update.message.chat_id, text=result)
        return
    bot.sendMessage(result, text="Your character was deleted by administration")


# introspection and general data
def get_master_data(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_master_user_data(update))


def get_user_introspection(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_introspection(update))


def get_public_record(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_public_data(update))


def get_security_record(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_security_data(update))


def get_police_personal_record(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_police_data(update))


def get_user_list(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_master_user_list(update))


def error(bot, update, error):
    user = UserAccount.objects.get_service_account()
    user.send_message(f"Update {update} caused error {error}")
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username

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
    # coproprations
    dp.add_handler(CommandHandler("corporations", get_own_corporations))
    dp.add_handler(CommandHandler("police_corporations", get_corporations))
    dp.add_handler(CommandHandler("security_corporation_members", get_security_corporation_members_list))
    dp.add_handler(CommandHandler("corporation_members", get_corporation_members_list))
    dp.add_handler(CommandHandler("corporation_withdraw", get_corporation_finances))
    dp.add_handler(CommandHandler("corporation_deposit", pass_finances_to_corporation))
    dp.add_handler(CommandHandler("corporation_history", get_corporation_financial_history))
    dp.add_handler(CommandHandler("security_corporation_history", get_security_corporation_financial_history))
    dp.add_handler(CommandHandler("add_corporation_member", add_to_corporation))
    dp.add_handler(CommandHandler("remove_corporation_member", remove_from_corporation))
    dp.add_handler(CommandHandler("promote_corporation_member", promote_in_corporation))
    dp.add_handler(CommandHandler("demote_corporation_member", demote_in_corporation))
    dp.add_handler(CommandHandler("all_corporations", get_all_corporations))
    # subscriptions
    dp.add_handler(CommandHandler("all_subscriptions", get_all_subscriptions))
    dp.add_handler(CommandHandler("subscriptions", get_own_subscriptions))
    dp.add_handler(CommandHandler("police_subscriptions", get_user_subscriptions))
    dp.add_handler(CommandHandler("approve_subscription", approve_subscription))
    dp.add_handler(CommandHandler("request_subscription", request_subscription))
    dp.add_handler(CommandHandler("unsubscribe", stop_subscription))
    dp.add_handler(CommandHandler("forced_unsubscrbe", master_break_subscription))
    # bank data: CHECKED;
    dp.add_handler(CommandHandler("all_bank_history", get_full_bank_histoty))
    dp.add_handler(CommandHandler("bank_history", get_own_bank_history))
    dp.add_handler(CommandHandler("security_bank_history", get_bank_history))
    dp.add_handler(CommandHandler("send", bot_create_transaction))
    dp.add_handler(CommandHandler("cancel", bot_cancel_transaction))
    # log all errors
    dp.add_error_handler(error)

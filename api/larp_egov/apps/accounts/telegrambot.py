from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot
from larp_egov.apps.accounts.services.deeplink import bind_user, delete_user, verify_user
from larp_egov.apps.accounts.bot_tasks import notify_admins
from larp_egov.apps.accounts.services.introspection import (
    get_introspection, get_police_data, get_security_data,
    get_public_data, get_master_user_list
)
from larp_egov.apps.accounts.services.misconduct_history import (
    get_own_misconduct_reports,
    get_user_misconduct_reports,
    get_filed_misconduct_reports,
    get_user_filed_misconduct_reports,
    get_all_misconduct_types,
    get_unassigned_misconduct_reports,
    get_open_assigned_misconduct_reports,
    get_all_assigned_misconduct_reports,
    get_all_police_misconduct_reports,
)
from larp_egov.apps.accounts.services.misconduct_reports import (
    file_misconduct_report,
    assign_report_to_yourself,
    decline_selected_report,
    process_assigned_report,
    finish_assigned_report,
    set_penalty_to_report,
    approve_autopenalty_to_report
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
    bot.sendMessage(update.message.chat_id, text=get_master_introspection(update))


def get_introspection(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_introspection(update))


def get_public_record(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_public_data(update))


def get_security_record(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_security_data(update))


def get_police_personal_record(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_police_data(update))


def get_user_list(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_master_user_list(update))


# misconduct_data
def list_misconduct_types(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_all_misconduct_types(update))


def file_misconduct_report(bot, update):
    result = file_misconduct_report(update)
    if result:
        bot.sendMessage(update.message.chat_id, text=result)


def assign_report(bot, update):
    result = assign_report_to_yourself(update)
    if result:
        bot.sendMessage(update.message.chat_id, text=result)


def decline_report(bot, update):
    result = decline_selected_report(update)
    if result:
        bot.sendMessage(update.message.chat_id, text=result)


def process_report(bot, update):
    result = process_assigned_report(update)
    if result:
        bot.sendMessage(update.message.chat_id, text=result)


def finish_report(bot, update):
    result = finish_assigned_report(update)
    if result:
        bot.sendMessage(update.message.chat_id, text=result)


def set_penalty(bot, update):
    result = set_penalty_to_report(update)
    if result:
        bot.sendMessage(update.message.chat_id, text=result)


def approve_autopenalty(bot, update):
    result = approve_autopenalty_to_report(update)
    if result:
        bot.sendMessage(update.message.chat_id, text=result)


def get_assigned_reports(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_all_assigned_misconduct_reports(update))


def get_open_assigned_reports(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_open_assigned_misconduct_reports(update))


def get_unassigned_reports(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_unassigned_misconduct_reports(update))


def get_misconduct_records(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_user_misconduct_reports(update))


def get_own_misconducts(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_own_misconducts(update))


def get_filed_misconducts(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_own_filed_misconducts(update))


def get_own_filed_misconducts(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_user_filed_misconduct_reports(update))


def get_all_police_misconduct_reports(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_all_police_misconduct_reports(update))


# bank_interactions
def get_bank_history(bot, update):
    pass

def get_own_bank_history(bot, update):
    pass

def create_transaction(bot, update):
    pass

def cancel_transaction(bot, update):
    pass

# subscriptions_data
def get_user_subscriptions(bot, update):
    pass

def get_own_subscriptions(bot, update):
    pass

def request_subscription(bot, update):
    pass

def get_all_subscriptions(bot, update):
    pass

def stop_subscription(bot, update):
    pass

def approve_subscription(bot, update):
    pass

def master_break_subscription(bot, update):
    pass


# corporations_data
def get_corporations(bot, update):
    pass

def get_own_corporations(bot, update):
    pass

def get_corporation_members_list(bot, update):
    pass

def get_corporation_finances(bot, update):
    pass

def pass_finances_to_corporation(bot, update):
    pass

def get_corporation_financial_history(bot, update):
    pass

def get_corporation_public_data(bot, update):
    pass

def add_to_corporation(bot, update):
    pass

def promote_in_corporation(bot, update):
    pass

def demote_in_corporation(bot, update):
    pass

def remove_from_corporation(bot, update):
    pass


def error(bot, update, error):
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
    # introspections
    dp.add_handler(CommandHandler("me", get_introspection))
    dp.add_handler(CommandHandler("public_record", get_public_record))
    dp.add_handler(CommandHandler("police_record", get_police_personal_record))
    dp.add_handler(CommandHandler("security_record", get_security_record))
    dp.add_handler(CommandHandler("master_data", get_master_data))
    # misconducts
    dp.add_handler(CommandHandler("misconducts", get_own_misconducts))
    dp.add_handler(CommandHandler("police_misconducts", get_misconduct_records))
    dp.add_handler(CommandHandler("filed_misconducts", get_filed_misconducts))
    dp.add_handler(CommandHandler("police_filed_misconducts", get_filed_misconduct_reports))
    dp.add_handler(CommandHandler("misconduct_types", get_all_misconduct_types))
    dp.add_handler(CommandHandler("open_misconducts", get_open_assigned_reports))
    dp.add_handler(CommandHandler("assigned_misconducts", get_assigned_reports))
    dp.add_handler(CommandHandler("unsassigned_misconducts", get_unassigned_reports))
    dp.add_handler(CommandHandler("police_records_full", get_all_police_misconduct_reports))
    # misconduct processing
    dp.add_handler(CommandHandler("report", file_misconduct_report))
    dp.add_handler(CommandHandler("assign", assign_report))
    dp.add_handler(CommandHandler("close", decline_report))
    dp.add_handler(CommandHandler("process", process_report))
    dp.add_handler(CommandHandler("finish", finish_report))
    dp.add_handler(CommandHandler("set_penalty", set_penalty))
    dp.add_handler(CommandHandler("autopenalty", approve_autopenalty))
    # coproprations
    dp.add_handler(CommandHandler("corporations", get_own_corporations))
    dp.add_handler(CommandHandler("police_corporations", get_corporations))
    dp.add_handler(CommandHandler("corporation_members", get_corporation_members_list))
    dp.add_handler(CommandHandler("corporation_withdraw", get_corporation_finances))
    dp.add_handler(CommandHandler("corporation_deposit", pass_finances_to_corporation))
    dp.add_handler(CommandHandler("corporation_history", get_corporation_financial_history))
    dp.add_handler(CommandHandler("corporation_public", get_corporation_public_data))
    dp.add_handler(CommandHandler("add_corporation_member", add_to_corporation))
    dp.add_handler(CommandHandler("remove_corporation_member", remove_from_corporation))
    dp.add_handler(CommandHandler("promote_corporation_member", promote_in_corporation))
    dp.add_handler(CommandHandler("demote_corporation_member", demote_in_corporation))
    # subscriptions
    dp.add_handler(CommandHandler("all_subscriptions", get_all_subscriptions))
    dp.add_handler(CommandHandler("subscriptions", get_own_subscriptions))
    dp.add_handler(CommandHandler("police_subscriptions", get_user_subscriptions))
    dp.add_handler(CommandHandler("approve_subscription", approve_subscription))
    dp.add_handler(CommandHandler("request_subscription", request_subscription))
    dp.add_handler(CommandHandler("unsubscribe", stop_subscription))
    dp.add_handler(CommandHandler("forced_unsubscrbe", master_break_subscription))
    # bank data
    dp.add_handler(CommandHandler("bank_history", get_own_bank_history))
    dp.add_handler(CommandHandler("security_bank_history", get_bank_history))
    dp.add_handler(CommandHandler("create_transaction", create_transaction))
    dp.add_handler(CommandHandler("cancel_transaction", cancel_transaction))
    # log all errors
    dp.add_error_handler(error)

from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot

from larp_egov.apps.common.bot_commands.safe_message_send import safe_message_send
from larp_egov.apps.banking.bot_commands.finance_transactions import (
    get_own_bank_data,
    get_user_bank_data,
    get_full_bank_data,
    create_transaction,
    cancel_transaction
)
from larp_egov.apps.banking.bot_commands.subscriptons import (
    display_all_subscriptions,
    display_own_subscriptions,
    display_user_subscriptions,
    approve_user_subscription,
    user_request_subscription,
    user_stop_subscription,
    user_forced_subscription_stop
)
from larp_egov.apps.banking.bot_commands.corporations import (
    display_corporation_members,
    display_all_corporations,
    display_own_corporations,
    display_user_corporations,
    security_display_corporation_members,
    make_corporation_deposit,
    make_corporation_withdrawal,
    display_corporation_financial_history,
    display_security_corporation_financial_history,
    add_user_to_corporation,
    kick_user_from_corporation,
    promote_user_in_corporation,
    demote_user_in_corporation,
    display_corporation_account_data,
)

import logging
logger = logging.getLogger(__name__)


# bank_interactions
def get_full_bank_histoty(update, context):
    safe_message_send(context.bot, update.message.chat_id, text=get_full_bank_data(update))


def get_bank_history(update, context):
    safe_message_send(context.bot, update.message.chat_id, text=get_user_bank_data(update))


def get_own_bank_history(update, context):
    safe_message_send(context.bot, update.message.chat_id, text=get_own_bank_data(update))


def bot_create_transaction(update, context):
    result = create_transaction(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def bot_cancel_transaction(update, context):
    result = cancel_transaction(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


# subscriptions_data
def get_user_subscriptions(update, context):
    safe_message_send(context.bot, update.message.chat_id, text=display_user_subscriptions(update))


def get_own_subscriptions(update, context):
    safe_message_send(context.bot, update.message.chat_id, text=display_own_subscriptions(update))


def request_subscription(update, context):
    result = user_request_subscription(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def get_all_subscriptions(update, context):
    safe_message_send(context.bot, update.message.chat_id, text=display_all_subscriptions(update))


def stop_subscription(update, context):
    result = user_stop_subscription(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def approve_subscription(update, context):
    result = approve_user_subscription(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def master_break_subscription(update, context):
    result = user_forced_subscription_stop(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


# corporations_data
def get_corporations(update, context):
    result = display_user_corporations(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def get_own_corporations(update, context):
    result = display_own_corporations(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def get_corporation_members_list(update, context):
    result = display_corporation_members(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def get_corporation_finances(update, context):
    result = make_corporation_withdrawal(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def pass_finances_to_corporation(update, context):
    result = make_corporation_deposit(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def get_corporation_financial_history(update, context):
    result = display_corporation_financial_history(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def add_to_corporation(update, context):
    result = add_user_to_corporation(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def promote_in_corporation(update, context):
    result = promote_user_in_corporation(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def demote_in_corporation(update, context):
    result = demote_user_in_corporation(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def remove_from_corporation(update, context):
    result = kick_user_from_corporation(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def get_security_corporation_financial_history(update, context):
    result = display_security_corporation_financial_history(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def get_security_corporation_members_list(update, context):
    result = security_display_corporation_members(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def get_all_corporations(update, context):
    result = display_all_corporations(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def get_own_account_data(update, context):
    result = display_corporation_account_data(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username
    # corporations: CHECKED
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
    dp.add_handler(CommandHandler("display_account_data", get_own_account_data))
    dp.add_handler(CommandHandler("all_corporations", get_all_corporations))
    # subscriptions: CHECKED
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

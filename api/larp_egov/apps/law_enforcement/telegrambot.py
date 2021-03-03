from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot

from larp_egov.apps.common.bot_commands.safe_message_send import safe_message_send
from larp_egov.apps.law_enforcement.bot_commands.misconduct_history import (
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
from larp_egov.apps.law_enforcement.bot_commands.misconduct_reports import (
    file_misconduct_report,
    assign_report_to_yourself,
    decline_selected_report,
    process_assigned_report,
    finish_assigned_report,
    set_penalty_to_report,
    approve_autopenalty_to_report
)

import logging
from common.utils.throttling import throttling_decorator
logger = logging.getLogger(__name__)


@throttling_decorator
def list_misconduct_types(update, context):
    safe_message_send(context.bot, update.message.chat_id, text=get_all_misconduct_types(update))


@throttling_decorator
def user_file_misconduct_report(update, context):
    result = file_misconduct_report(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


@throttling_decorator
def assign_report(update, context):
    result = assign_report_to_yourself(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


@throttling_decorator
def decline_report(update, context):
    result = decline_selected_report(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


@throttling_decorator
def process_report(update, context):
    result = process_assigned_report(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


@throttling_decorator
def finish_report(update, context):
    result = finish_assigned_report(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


@throttling_decorator
def set_penalty(update, context):
    result = set_penalty_to_report(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


@throttling_decorator
def approve_autopenalty(update, context):
    result = approve_autopenalty_to_report(update)
    if result:
        safe_message_send(context.bot, update.message.chat_id, text=result)


@throttling_decorator
def get_assigned_reports(update, context):
    safe_message_send(context.bot, update.message.chat_id, text=get_all_assigned_misconduct_reports(update))


@throttling_decorator
def get_open_assigned_reports(update, context):
    safe_message_send(context.bot, update.message.chat_id, text=get_open_assigned_misconduct_reports(update))


@throttling_decorator
def get_unassigned_reports(update, context):
    safe_message_send(context.bot, update.message.chat_id, text=get_unassigned_misconduct_reports(update))


@throttling_decorator
def get_misconduct_records(update, context):
    safe_message_send(context.bot, update.message.chat_id, text=get_user_misconduct_reports(update))


@throttling_decorator
def get_user_own_misconducts(update, context):
    safe_message_send(context.bot, update.message.chat_id, text=get_own_misconduct_reports(update))


@throttling_decorator
def get_filed_misconducts(update, context):
    safe_message_send(context.bot, update.message.chat_id, text=get_filed_misconduct_reports(update))


@throttling_decorator
def get_user_filed_misconducts(update, context):
    safe_message_send(context.bot, update.message.chat_id, text=get_user_filed_misconduct_reports(update))


@throttling_decorator
def bot_get_all_police_misconduct_reports(update, context):
    safe_message_send(context.bot, update.message.chat_id, text=get_all_police_misconduct_reports(update))


def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username

    # misconducts: CHECKED;
    dp.add_handler(CommandHandler("misconducts", get_user_own_misconducts))
    dp.add_handler(CommandHandler("police_misconducts", get_misconduct_records))
    dp.add_handler(CommandHandler("filed_misconducts", get_filed_misconducts))
    dp.add_handler(CommandHandler("police_filed_misconducts", get_user_filed_misconducts))
    dp.add_handler(CommandHandler("misconduct_types", list_misconduct_types))
    dp.add_handler(CommandHandler("open_misconducts", get_open_assigned_reports))
    dp.add_handler(CommandHandler("assigned_misconducts", get_assigned_reports))
    dp.add_handler(CommandHandler("unassigned_misconducts", get_unassigned_reports))
    dp.add_handler(CommandHandler("police_records_full", bot_get_all_police_misconduct_reports))
    # misconduct processing: CHECKED;
    dp.add_handler(CommandHandler("report", user_file_misconduct_report))
    dp.add_handler(CommandHandler("assign", assign_report))
    dp.add_handler(CommandHandler("close", decline_report))
    dp.add_handler(CommandHandler("process", process_report))
    dp.add_handler(CommandHandler("finish", finish_report))
    dp.add_handler(CommandHandler("set_penalty", set_penalty))
    dp.add_handler(CommandHandler("autopenalty", approve_autopenalty))

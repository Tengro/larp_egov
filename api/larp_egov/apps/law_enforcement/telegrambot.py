from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot

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
logger = logging.getLogger(__name__)


def list_misconduct_types(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_all_misconduct_types(update))


def user_file_misconduct_report(bot, update):
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


def get_user_own_misconducts(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_own_misconduct_reports(update))


def get_filed_misconducts(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_own_filed_misconducts(update))


def get_user_filed_misconducts(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_user_filed_misconduct_reports(update))


def bot_get_all_police_misconduct_reports(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_all_police_misconduct_reports(update))


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

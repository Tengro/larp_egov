from larp_egov.apps.hacking.bot_commands.common import (
    initiate_hack, hack_create_report,
    hack_create_transaction, hack_decline_report, hack_delete_report,
    hack_finish_report, hack_inspect_special, hack_perform_special,
    hack_user_corporations, hack_user_subscriptions, hack_user_bank_history,
    hack_user_misconduct_records, hack_user_police_data, hack_user_security_data,
)
from larp_egov.apps.hacking.models import HackingSession
from larp_egov.apps.accounts.selectors import (
    get_user_by_character_id, get_user_by_telegram_id,
)
from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot
from larp_egov.apps.hacking.config import HACK_LEVEL_COST_MAPPING
from larp_egov.apps.common.bot_commands._common_texts import UNREGISTERED, NO_ACTIVE_HACK
import logging
logger = logging.getLogger(__name__)


def get_active_hack(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    hack = HackingSession.objects.filter(is_active=True, hacker=requester).first()
    if hack:
        return hack
    return NO_ACTIVE_HACK


def initiate_hack_noob(update, context):
    hacker = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    target = get_user_by_character_id(update.message.text[5:])
    initiate_hack(hakcer, target, 'noob')


def initiate_hack_mid(update, context):
    hacker = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    target = get_user_by_character_id(update.message.text[5:])
    initiate_hack(hakcer, target, 'middle')


def initiate_hack_pro(update, context):
    hacker = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    target = get_user_by_character_id(update.message.text[5:])
    initiate_hack(hakcer, target, 'pro')


def hack_create_report_noob(update, context):
    message = update.message.text[5:]
    user_code, misconduct_type = message.split(' ')
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_create_report(hack, 'noob', user_code, misconduct_type))


def hack_create_report_mid(update, context):
    message = update.message.text[5:]
    user_code, misconduct_type = message.split(' ')
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_create_report(hack, 'middle', user_code, misconduct_type))


def hack_create_report_pro(update, context):
    message = update.message.text[5:]
    user_code, misconduct_type = message.split(' ')
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_create_report(hack, 'pro', user_code, misconduct_type))


def hack_create_transaction_noob(update, context):
    message = update.message.text[6:]
    user_code, amount = message.split(' ')
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_create_transaction(hack, 'noob', user_code, amount))


def hack_create_transaction_mid(update, context):
    message = update.message.text[6:]
    user_code, amount = message.split(' ')
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_create_transaction(hack, 'middle', user_code, amount))


def hack_create_transaction_pro(update, context):
    message = update.message.text[6:]
    user_code, amount = message.split(' ')
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_create_transaction(hack, 'pro', user_code, amount))


def hack_decline_report_noob(update, context):
    misconduct_id = update.message.text[5:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_decline_report(hack, 'noob', misconduct_id))


def hack_decline_report_mid(update, context):
    misconduct_id = update.message.text[5:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_decline_report(hack, 'middle', misconduct_id))


def hack_decline_report_pro(update, context):
    misconduct_id = update.message.text[5:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_decline_report(hack, 'pro', misconduct_id))


def hack_delete_report_noob(update, context):
    misconduct_id = update.message.text[5:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_delete_report(hack, 'noob', misconduct_id))


def hack_delete_report_mid(update, context):
    misconduct_id = update.message.text[5:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_delete_report(hack, 'middle', misconduct_id))


def hack_delete_report_pro(update, context):
    misconduct_id = update.message.text[5:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_delete_report(hack, 'pro', misconduct_id))


def hack_finish_report_noob(update, context):
    misconduct_id = update.message.text[5:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_finish_report(hack, 'noob', misconduct_id))


def hack_finish_report_mid(update, context):
    misconduct_id = update.message.text[5:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_finish_report(hack, 'middle', misconduct_id))


def hack_finish_report_pro(update, context):
    misconduct_id = update.message.text[5:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_finish_report(hack, 'pro', misconduct_id))


def hack_inspect_special_noob(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_inspect_special(hack, 'noob'))


def hack_inspect_special_mid(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_inspect_special(hack, 'middle'))


def hack_inspect_special_pro(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_inspect_special(hack, 'pro'))


def hack_perform_special_noob(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_perform_special(hack, 'noob'))


def hack_perform_special_mid(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_perform_special(hack, 'middle'))


def hack_perform_special_pro(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_perform_special(hack, 'pro'))


def hack_user_corporations_noob(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_corporations(hack, 'noob'))


def hack_user_corporations_mid(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_corporations(hack, 'middle'))


def hack_user_corporations_pro(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_corporations(hack, 'pro'))


def hack_user_subscriptions_noob(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_subscriptions(hack, 'noob'))


def hack_user_subscriptions_mid(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_subscriptions(hack, 'middle'))


def hack_user_subscriptions_pro(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_subscriptions(hack, 'pro'))


def hack_user_bank_history_noob(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_bank_history(hack, 'noob'))


def hack_user_bank_history_mid(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_bank_history(hack, 'middle'))


def hack_user_bank_history_pro(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_bank_history(hack, 'pro'))


def hack_user_misconduct_records_noob(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_misconduct_records(hack, 'noob'))


def hack_user_misconduct_records_mid(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_misconduct_records(hack, 'middle'))


def hack_user_misconduct_records_pro(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_misconduct_records(hack, 'pro'))


def hack_user_police_data_noob(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_police_data(hack, 'noob'))


def hack_user_police_data_mid(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_police_data(hack, 'middle'))


def hack_user_police_data_pro(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_police_data(hack, 'pro'))


def hack_user_security_data_noob(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_security_data(hack, 'noob'))


def hack_user_security_data_mid(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_security_data(hack, 'middle'))


def hack_user_security_data_pro(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    context.bot.sendMessage(update.message.chat_id, text=hack_user_security_data(hack, 'pro'))


def hack_finish_hacking(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        context.bot.sendMessage(update.message.chat_id, text=hack)
        return
    hack.finish_hack()


def main():
    logger.info("Loading handlers for telegram bot")

    dp = DjangoTelegramBot.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("hack", initiate_hack_noob))

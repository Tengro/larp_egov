from larp_egov.apps.common.bot_commands.safe_message_send import safe_message_send
from larp_egov.apps.hacking.bot_commands.common import (
    initiate_hack, hack_create_report,
    hack_create_transaction, hack_decline_report, hack_delete_report,
    hack_finish_report, hack_inspect_special, hack_perform_special,
    hack_user_corporations, hack_user_subscriptions, hack_user_bank_history,
    hack_user_misconduct_records, hack_user_police_data, hack_user_security_data,
    perform_active_countermeasures,
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
from larp_egov.apps.common.utils.throttling import throttling_decorator
logger = logging.getLogger(__name__)


def get_active_hack(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    hack = HackingSession.objects.filter(is_active=True, hacker=requester).first()
    if hack:
        return hack
    return NO_ACTIVE_HACK


@throttling_decorator
def initiate_hack_noob(update, context):
    hacker = get_user_by_telegram_id(update.message.chat_id)
    if not hacker:
        safe_message_send(context.bot, update.message.chat_id, text=UNREGISTERED)
        return
    target = get_user_by_character_id(update.message.text[6:])
    initiate_hack(hacker, target, 'noob')


@throttling_decorator
def initiate_hack_mid(update, context):
    hacker = get_user_by_telegram_id(update.message.chat_id)
    if not hacker:
        safe_message_send(context.bot, update.message.chat_id, text=UNREGISTERED)
        return
    target = get_user_by_character_id(update.message.text[6:])
    initiate_hack(hacker, target, 'middle')


@throttling_decorator
def initiate_hack_pro(update, context):
    hacker = get_user_by_telegram_id(update.message.chat_id)
    if not hacker:
        safe_message_send(context.bot, update.message.chat_id, text=UNREGISTERED)
        return
    target = get_user_by_character_id(update.message.text[5:])
    initiate_hack(hacker, target, 'pro')


@throttling_decorator
def hack_create_report_noob(update, context):
    message = update.message.text[20:]
    user_code, misconduct_type = message.split(' ')
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_create_report(hack, 'noob', user_code, misconduct_type))


@throttling_decorator
def hack_create_report_mid(update, context):
    message = update.message.text[20:]
    user_code, misconduct_type = message.split(' ')
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_create_report(hack, 'middle', user_code, misconduct_type))


@throttling_decorator
def hack_create_report_pro(update, context):
    message = update.message.text[14:]
    user_code, misconduct_type = message.split(' ')
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_create_report(hack, 'pro', user_code, misconduct_type))


@throttling_decorator
def hack_create_transaction_noob(update, context):
    message = update.message.text[25:]
    user_code, amount = message.split(' ')
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_create_transaction(hack, 'noob', user_code, amount))


@throttling_decorator
def hack_create_transaction_mid(update, context):
    message = update.message.text[25:]
    user_code, amount = message.split(' ')
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_create_transaction(hack, 'middle', user_code, amount))


@throttling_decorator
def hack_create_transaction_pro(update, context):
    message = update.message.text[17:]
    user_code, amount = message.split(' ')
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_create_transaction(hack, 'pro', user_code, amount))


@throttling_decorator
def hack_decline_report_noob(update, context):
    misconduct_id = update.message.text[21:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_decline_report(hack, 'noob', misconduct_id))


@throttling_decorator
def hack_decline_report_mid(update, context):
    misconduct_id = update.message.text[21:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_decline_report(hack, 'middle', misconduct_id))


@throttling_decorator
def hack_decline_report_pro(update, context):
    misconduct_id = update.message.text[15:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_decline_report(hack, 'pro', misconduct_id))


@throttling_decorator
def hack_delete_report_noob(update, context):
    misconduct_id = update.message.text[20:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_delete_report(hack, 'noob', misconduct_id))


@throttling_decorator
def hack_delete_report_mid(update, context):
    misconduct_id = update.message.text[20:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_delete_report(hack, 'middle', misconduct_id))


@throttling_decorator
def hack_delete_report_pro(update, context):
    misconduct_id = update.message.text[14:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_delete_report(hack, 'pro', misconduct_id))


@throttling_decorator
def hack_finish_report_noob(update, context):
    misconduct_id = update.message.text[20:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_finish_report(hack, 'noob', misconduct_id))


@throttling_decorator
def hack_finish_report_mid(update, context):
    misconduct_id = update.message.text[20:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_finish_report(hack, 'middle', misconduct_id))


@throttling_decorator
def hack_finish_report_pro(update, context):
    misconduct_id = update.message.text[15:]
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_finish_report(hack, 'pro', misconduct_id))


@throttling_decorator
def hack_inspect_special_noob(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_inspect_special(hack, 'noob'))


@throttling_decorator
def hack_inspect_special_mid(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_inspect_special(hack, 'middle'))


@throttling_decorator
def hack_inspect_special_pro(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_inspect_special(hack, 'pro'))


@throttling_decorator
def hack_perform_special_noob(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_perform_special(hack, 'noob'))


@throttling_decorator
def hack_perform_special_mid(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_perform_special(hack, 'middle'))


@throttling_decorator
def hack_perform_special_pro(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_perform_special(hack, 'pro'))


@throttling_decorator
def hack_user_corporations_noob(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_corporations(hack, 'noob'))


@throttling_decorator
def hack_user_corporations_mid(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_corporations(hack, 'middle'))


@throttling_decorator
def hack_user_corporations_pro(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_corporations(hack, 'pro'))


@throttling_decorator
def hack_user_subscriptions_noob(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_subscriptions(hack, 'noob'))


@throttling_decorator
def hack_user_subscriptions_mid(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_subscriptions(hack, 'middle'))


@throttling_decorator
def hack_user_subscriptions_pro(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_subscriptions(hack, 'pro'))


@throttling_decorator
def hack_user_bank_history_noob(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_bank_history(hack, 'noob'))


@throttling_decorator
def hack_user_bank_history_mid(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_bank_history(hack, 'middle'))


@throttling_decorator
def hack_user_bank_history_pro(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_bank_history(hack, 'pro'))


@throttling_decorator
def hack_user_misconduct_records_noob(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_misconduct_records(hack, 'noob'))


@throttling_decorator
def hack_user_misconduct_records_mid(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_misconduct_records(hack, 'middle'))


@throttling_decorator
def hack_user_misconduct_records_pro(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_misconduct_records(hack, 'pro'))


@throttling_decorator
def hack_user_police_data_noob(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_police_data(hack, 'noob'))


@throttling_decorator
def hack_user_police_data_mid(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_police_data(hack, 'middle'))


@throttling_decorator
def hack_user_police_data_pro(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_police_data(hack, 'pro'))


@throttling_decorator
def hack_user_security_data_noob(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_security_data(hack, 'noob'))


@throttling_decorator
def hack_user_security_data_mid(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_security_data(hack, 'middle'))


@throttling_decorator
def hack_user_security_data_pro(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    safe_message_send(context.bot, update.message.chat_id, text=hack_user_security_data(hack, 'pro'))


@throttling_decorator
def hack_finish_hacking(update, context):
    hack = get_active_hack(update)
    if not isinstance(hack, HackingSession):
        safe_message_send(context.bot, update.message.chat_id, text=hack)
        return
    hack.finish_hack()


@throttling_decorator
def active_coutermeasures(update, context):
    caller = get_user_by_telegram_id(update.message.chat_id)
    if not caller:
        safe_message_send(context.bot, update.message.chat_id, text=UNREGISTERED)
        return
    perform_active_countermeasures(caller)


def main():
    logger.info("Loading handlers for telegram bot")

    dp = DjangoTelegramBot.dispatcher
    # on different commands - answer in Telegram
    # NOOB COMMANDS: TESTED
    dp.add_handler(CommandHandler("hack", initiate_hack_noob))
    dp.add_handler(CommandHandler("hack_police", hack_user_police_data_noob))
    dp.add_handler(CommandHandler("hack_security", hack_user_security_data_noob))
    dp.add_handler(CommandHandler("hack_inspect", hack_inspect_special_noob))
    dp.add_handler(CommandHandler("hack_special", hack_perform_special_noob))
    dp.add_handler(CommandHandler("hack_corporations", hack_user_corporations_noob))
    dp.add_handler(CommandHandler("hack_subscriptions", hack_user_subscriptions_noob))
    dp.add_handler(CommandHandler("hack_bank_history", hack_user_bank_history_noob))
    dp.add_handler(CommandHandler("hack_reports", hack_user_misconduct_records_noob))
    dp.add_handler(CommandHandler("hack_report_create", hack_create_report_noob))
    dp.add_handler(CommandHandler("hack_create_transaction", hack_create_transaction_noob))
    dp.add_handler(CommandHandler("hack_report_decline", hack_decline_report_noob))
    dp.add_handler(CommandHandler("hack_report_delete", hack_delete_report_noob))
    dp.add_handler(CommandHandler("hack_report_finish", hack_finish_report_noob))
    # MIDDLE COMMANDS
    dp.add_handler(CommandHandler("h4ck", initiate_hack_mid))
    dp.add_handler(CommandHandler("h4ck_p0lice", hack_user_police_data_mid))
    dp.add_handler(CommandHandler("h4ck_secur1ty", hack_user_security_data_mid))
    dp.add_handler(CommandHandler("h4ck_insp3ct", hack_inspect_special_mid))
    dp.add_handler(CommandHandler("h4ck_speci4l", hack_perform_special_mid))
    dp.add_handler(CommandHandler("h4ck_corp0rations", hack_user_corporations_mid))
    dp.add_handler(CommandHandler("h4ck_subscr1ptions", hack_user_subscriptions_mid))
    dp.add_handler(CommandHandler("h4ck_bank_hist0ry", hack_user_bank_history_mid))
    dp.add_handler(CommandHandler("h4ck_rep0rts", hack_user_misconduct_records_mid))
    dp.add_handler(CommandHandler("h4ck_rep0rt_creat3", hack_create_report_mid))
    dp.add_handler(CommandHandler("h4ck_cre4te_transacti0n", hack_create_transaction_mid))
    dp.add_handler(CommandHandler("h4ck_rep0rt_d3cline", hack_decline_report_mid))
    dp.add_handler(CommandHandler("h4ck_rep0rt_d3lete", hack_delete_report_mid))
    dp.add_handler(CommandHandler("h4ck_rep0rt_f1nish", hack_finish_report_mid))
    # PRO COMMANDS
    dp.add_handler(CommandHandler("xfr", initiate_hack_pro))
    dp.add_handler(CommandHandler("xfr_zdc", hack_user_police_data_pro))
    dp.add_handler(CommandHandler("xfr_icke", hack_user_security_data_pro))
    dp.add_handler(CommandHandler("xfr_tizce", hack_inspect_special_pro))
    dp.add_handler(CommandHandler("xfr_izcd", hack_perform_special_pro))
    dp.add_handler(CommandHandler("xfr_ckzketi", hack_user_corporations_pro))
    dp.add_handler(CommandHandler("xfr_iuickzeti", hack_user_subscriptions_pro))
    dp.add_handler(CommandHandler("xfr_utl_riek", hack_user_bank_history_pro))
    dp.add_handler(CommandHandler("xfr_kzkei", hack_user_misconduct_records_pro))
    dp.add_handler(CommandHandler("xfr_kzke_cke", hack_create_report_pro))
    dp.add_handler(CommandHandler("xfr_cke_ekticet", hack_create_transaction_pro))
    dp.add_handler(CommandHandler("xfr_kzke_bcdt", hack_decline_report_pro))
    dp.add_handler(CommandHandler("xfr_kzke_bde", hack_delete_report_pro))
    dp.add_handler(CommandHandler("xfr_kzke_atir", hack_finish_report_pro))
    # Finish Hack
    dp.add_handler(CommandHandler("finish_hack", hack_finish_hacking))
    dp.add_handler(CommandHandler("counterhack", active_coutermeasures))

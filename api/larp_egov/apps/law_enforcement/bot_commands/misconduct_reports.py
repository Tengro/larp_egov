import decimal
from django.utils.translation import ugettext_lazy as _
from larp_egov.apps.accounts.selectors import (
    get_user_by_character_id, get_user_by_telegram_id,
    get_all_characters_in_game
)
from larp_egov.apps.law_enforcement.models import MisconductReport, MisconductReportStatus, MisconductType
from larp_egov.apps.common.bot_commands._common_texts import UNREGISTERED, NO_ACCESS_DATA, NO_ACCESS_COMMAND, NO_REPORT_FOUND, validate_police


def file_misconduct_report(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    message = update.message.text[8:]
    user_code, misconduct_type = message.split(' ')
    user = get_user_by_character_id(user_code)
    if not user:
        return _("Не можу знайти такого користувача у базі даних. Скаргу не надіслано.")
    misconduct_type = MisconductType.objects.filter(misconduct_code=misconduct_type).first()
    if not misconduct_type:
        return _("Не можу знайти код правопорушення у базі даних. Скаргу не надіслано")
    MisconductReport.create_misconduct_report(requester, user, misconduct_type)
    return None


def assign_report_to_yourself(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not validate_police(requester):
        return NO_ACCESS_COMMAND
    report_id = update.message.text[8:]
    report = MisconductReport.objects.filter(misconduct_id=report_id).first()
    if not report:
        return _("Скарги з таким номером не знайдено. Перевірте ІД скарги")
    report.assign_report(requester)


def decline_selected_report(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not validate_police(requester):
        return NO_ACCESS_COMMAND
    report_id = update.message.text[7:]
    report = MisconductReport.objects.filter(officer_in_charge=requester, misconduct_id=report_id).first()
    if not report:
        return NO_REPORT_FOUND
    report.decline_report()


def process_assigned_report(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not validate_police(requester):
        return NO_ACCESS_COMMAND
    report_id = update.message.text[9:]
    report = MisconductReport.objects.filter(officer_in_charge=requester, misconduct_id=report_id).first()
    if not report:
        return NO_REPORT_FOUND
    report.process_report()


def finish_assigned_report(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not validate_police(requester):
        return NO_ACCESS_COMMAND
    report_id = update.message.text[8:]
    report = MisconductReport.objects.filter(officer_in_charge=requester, misconduct_id=report_id).first()
    if not report:
        return NO_REPORT_FOUND
    report.finish_report()


def set_penalty_to_report(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not validate_police(requester):
        return NO_ACCESS_COMMAND
    report_id, penalty_amount = update.message.text[13:].split(' ')
    report = MisconductReport.objects.filter(officer_in_charge=requester, misconduct_id=report_id).first()
    if not report:
        return NO_REPORT_FOUND
    try:
        penalty_amount = decimal.Decimal(penalty_amount)
    except decimal.InvalidOperation:
        return _("Некоректна сума стягнення!")
    report.set_penalty(penalty_amount)


def approve_autopenalty_to_report(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not validate_police(requester):
        return NO_ACCESS_COMMAND
    report_id = update.message.text[13:]
    report = MisconductReport.objects.filter(officer_in_charge=requester, misconduct_id=report_id).first()
    if not report:
        return NO_REPORT_FOUND
    report.set_auto_penalty()


def freeze_amount(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not validate_police(requester):
        return NO_ACCESS_COMMAND
    message = update.message.text[8:]
    result_data = message.split(' ')
    if len(result_data) == 2:
        user_code, amount = result_data
    elif len(result_data) > 2:
        user_code = result_data[0]
        amount = result_data[1]
    user = get_user_by_character_id(user_code)
    if not user:
        return _("Користувач з таким ID не знайдений. Транзакція не надіслана")
    try:
        amount = decimal.Decimal(amount)
    except decimal.InvalidOperation:
        return _("Сума не розпізнана")
    user_message = f"Змінено суму заморожених коштів на вашому рахунку. Нова заморожена сума {amount}. Відповідальний офіцер: {requester.full_name}"
    police_message = f"Змінено суму заморожених коштів на рахунку {user.full_name}. Нова заморожена сума {amount}."
    user.freeze(amount, user_message)
    requester.send_message(police_message)

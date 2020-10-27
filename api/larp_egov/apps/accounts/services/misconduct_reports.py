import decimal
from larp_egov.apps.accounts.selectors import (
    get_user_by_character_id, get_user_by_telegram_id,
    get_all_characters_in_game
)
from larp_egov.apps.law_enforcement.models import MisconductReport, MisconductReportStatus, MisconductType


def validate_police(character):
    return (character.is_police or character.is_security)


def file_misconduct_report(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    message = update.message.text[8:]
    user_code, misconduct_type = message.split(' ')
    user = get_user_by_character_id(user_code)
    if not user:
        return "Can\'t find user in database; report not filed"
    misconduct_type = MisconductType.objects.filter(misconduct_code=misconduct_type).first()
    if not misconduct_type:
        return "Can\'t find misconduct type of this code; report not filed"
    MisconductReport.create_misconduct_report(requester, user, misconduct_type)
    return None


def assign_report_to_yourself(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    if not validate_police(requester):
        return "You have no access to this command"
    report_id = update.message.text[8:]
    report = MisconductReport.objects.filter(misconduct_id=report_id).first()
    if not report:
        return "No such report found. Check report ID please"
    report.assign_report(requester)


def decline_selected_report(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    if not validate_police(requester):
        return "You have no access to this command"
    report_id = update.message.text[7:]
    report = MisconductReport.objects.filter(officer_in_charge=requester, misconduct_id=report_id).first()
    if not report:
        return "No such report found. Check report ID or assigned office of the report please"
    report.decline_report()


def process_assigned_report(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    if not validate_police(requester):
        return "You have no access to this command"
    report_id = update.message.text[9:]
    report = MisconductReport.objects.filter(officer_in_charge=requester, misconduct_id=report_id).first()
    if not report:
        return "No such report found. Check report ID or assigned office of the report please"
    report.process_report()


def finish_assigned_report(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    if not validate_police(requester):
        return "You have no access to this command"
    report_id = update.message.text[8:]
    report = MisconductReport.objects.filter(officer_in_charge=requester, misconduct_id=report_id).first()
    if not report:
        return "No such report found. Check report ID or assigned office of the report please"
    report.finish_report()


def set_penalty_to_report(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    if not validate_police(requester):
        return "You have no access to this command"
    report_id, penalty_amount = update.message.text[13:].split(' ')
    report = MisconductReport.objects.filter(officer_in_charge=requester, misconduct_id=report_id).first()
    if not report:
        return "No such report found. Check report ID or assigned office of the report please"
    try:
        penalty_amount = decimal.Decimal(penalty_amount)
    except decimal.InvalidOperation:
        return "Incorrect penalty amount!"
    report.set_penalty(penalty_amount)


def approve_autopenalty_to_report(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    if not validate_police(requester):
        return "You have no access to this command"
    report_id = update.message.text[13:]
    report = MisconductReport.objects.filter(officer_in_charge=requester, misconduct_id=report_id).first()
    if not report:
        return "No such report found. Check report ID or assigned office of the report please"
    report.set_auto_penalty()

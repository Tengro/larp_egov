from larp_egov.apps.accounts.selectors import (
    get_user_by_character_id, get_user_by_telegram_id,
    get_all_characters_in_game
)
from larp_egov.apps.law_enforcement.models import MisconductReport, MisconductReportStatus, MisconductType


def validate_police(character):
    return (character.is_police or character.is_security)


def validate_security(character):
    return character.is_security


def get_own_misconduct_reports(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    reports = MisconductReport.objects.filter(reported_person=requester)
    if not reports:
        return "You have clean record"
    return '\n\n'.join([x.anonymised_string for x in reports])


def get_filed_misconduct_reports(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    reports = MisconductReport.objects.filter(reporter=requester)
    if not reports:
        return "You have filed no reports"
    return '\n\n'.join([x.police_record_string for x in reports])


def get_user_misconduct_reports(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    if not validate_police(requester):
        return "You have no access to this data"
    code = update.message.text[20:]
    user = get_user_by_character_id(code)
    if not user:
        return "No such user exists"
    reports = MisconductReport.objects.filter(reported_person=user)
    if not reports:
        return "This person has clean record"
    return '\n\n'.join([x.police_record_string for x in reports])


def get_user_filed_misconduct_reports(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    if not validate_police(requester):
        return "You have no access to this data"
    code = update.message.text[26:]
    user = get_user_by_character_id(code)
    if not user:
        return "No such user exists"
    reports = MisconductReport.objects.filter(reporter=user)
    if not reports:
        return "This person filed no reports"
    return '\n\n'.join([x.police_record_string for x in reports])


def get_all_assigned_misconduct_reports(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    if not validate_police(requester):
        return "You have no access to this data"
    reports = MisconductReport.objects.filter(officer_in_charge=requester)
    if not reports:
        return "You have no assigned reports"
    return '\n\n'.join([x.police_record_string for x in reports])


def get_open_assigned_misconduct_reports(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    if not validate_police(requester):
        return "You have no access to this data"
    reports = MisconductReport.objects.filter(
        officer_in_charge=requester
    ).exclude(misconduct_status__in=[MisconductReportStatus.DECLINED, MisconductReportStatus.FINISHED])
    if not reports:
        return "You have no assigned reports"
    return '\n\n'.join([x.police_record_string for x in reports])


def get_unassigned_misconduct_reports(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    if not validate_police(requester):
        return "You have no access to this data"
    reports = MisconductReport.objects.filter(officer_in_charge=None)
    if not reports:
        return "No assigned reports in database!"
    return '\n\n'.join([x.police_record_string for x in reports])


def get_all_misconduct_types(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    return '\n\n'.join([x.display_data for x in MisconductType.objects.all()])


def get_all_police_misconduct_reports(update, override_permissions=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return "Seems like you aren't registered"
    if not validate_police(requester) and not override_permissions:
        return "You have no access to this data"
    reports = MisconductReport.objects.all()
    return '\n\n'.join([x.police_record_string for x in reports])

from larp_egov.apps.hacking.config import HACK_LEVEL_COST_MAPPING
from larp_egov.apps.hacking.models import HackingSession
from larp_egov.apps.law_enforcement.models import MisconductReport, MisconductType
from larp_egov.apps.banking.models import BankTransaction
from django.utils.translation import ugettext_lazy as _
from larp_egov.apps.accounts.selectors import (
    get_user_by_character_id,
)
from larp_egov.apps.common.bot_commands._common_texts import NO_REPORT_FOUND


def initiate_hack(hacker, character, level):
    OPERATION_VALUE = 1
    HackingSession.begin_hack(hacker, character, OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])


def hack_user_corporations(hack, level):
    OPERATION_VALUE = 1
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return
    return "\n\n".join([x.display for x in CorporationMembership.objects.filter(member=hack.target)])


def hack_user_subscriptions(hack, level):
    OPERATION_VALUE = 1
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return
    return "\n\n".join([x.display for x in user.bankusersubscriptionintermediary_set.all()])


def hack_user_security_data(hack, level):
    OPERATION_VALUE = 1
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return
    return hack.target.get_user_security_data()


def hack_user_police_data(hack, level):
    OPERATION_VALUE = 1
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return
    return hack.target.get_user_police_data()


def hack_user_misconduct_records(hack, level):
    OPERATION_VALUE = 1
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return
    reports = MisconductReport.objects.filter(reported_person=hack.target)
    if not reports:
        return _("This person has clean record")
    return '\n\n'.join([x.police_record_string for x in reports])


def hack_user_bank_history(hack, level):
    OPERATION_VALUE = 1
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return
    return '\n\n'.join(
        [
            x.user_transaction_log(hack.target) for x in BankTransaction.objects.get_user_bank_history(hack.target).order_by('created')
        ]
    )


def hack_decline_report(hack, level, misconduct_id):
    OPERATION_VALUE = 1
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return
    report = MisconductReport.objects.filter(misconduct_id=report_id).first()
    if not report:
        return NO_REPORT_FOUND
    report.decline_report(silent=True)
    return "Report successfuly declined"


def hack_finish_report(hack, level, misconduct_id):
    OPERATION_VALUE = 1
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return
    report = MisconductReport.objects.filter(misconduct_id=report_id).first()
    if not report:
        return NO_REPORT_FOUND
    report.finish_report(silent=True)
    return "Report successfuly finished"


def hack_delete_report(hack, level, misconduct_id):
    OPERATION_VALUE = 1
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return
    report = MisconductReport.objects.filter(misconduct_id=report_id).first()
    if not report:
        return NO_REPORT_FOUND
    report.delete()
    return "Report successfuly deleted"


def hack_create_report(hack, level, reported_id, misconduct_type):
    OPERATION_VALUE = 1
    user = get_user_by_character_id(reported_id)
    if not user:
        return _("Can\'t find user in database; report not filed")
    misconduct_type = MisconductType.objects.filter(misconduct_code=misconduct_type).first()
    if not misconduct_type:
        return _("Can\'t find misconduct type of this code; report not filed")
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return
    MisconductReport.create_misconduct_report(hack.target, user, misconduct_type)
    return "Report successfuly created"


def hack_create_transaction(hack, level, reciever_id, amount):
    OPERATION_VALUE = 1
    if amount > hack.target.bank_account:
        return ValueError('Bank account insufficient')
    user = get_user_by_character_id(reciever_id)
    if not user:
        return _("Can\'t find user in database; transaction not sent")
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return
    BankTransaction.create_transaction(hack.target, user, amount, is_anonymous=True)
    return f"Transaction is successful"


def hack_inspect_special(hack, level):
    OPERATION_VALUE = 1
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return
    if hack.target.has_special_hack_value:
        value = hack.target.special_hack_pro_price * HACK_LEVEL_COST_MAPPING[level]
        return f"Target has special hack protocol; system tick cost: {value}"
    return f"Target hasn't any special hack protocol"


def hack_perform_special(hack, level):
    OPERATION_VALUE = hack.target.special_hack_pro_price
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return
    return f"Please, contact gamemasters immidiately (successful hack of {hack.target.character_id})"

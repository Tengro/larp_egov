import decimal
from larp_egov.apps.hacking.config import HACK_LEVEL_COST_MAPPING
from larp_egov.apps.hacking.models import HackingSession
from larp_egov.apps.law_enforcement.models import MisconductReport, MisconductType
from larp_egov.apps.banking.models import BankTransaction, CorporationMembership
from django.utils.translation import ugettext_lazy as _
from larp_egov.apps.accounts.selectors import (
    get_user_by_character_id,
)
from larp_egov.apps.common.bot_commands._common_texts import (
    NO_REPORT_FOUND, NO_CORPORATIONS, NO_SUBSCRIPTIONS,
    HACK_TERMINATED
)


def initiate_hack(hacker, character, level):
    OPERATION_VALUE = 1
    HackingSession.begin_hack(hacker, character, OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])


def hack_user_corporations(hack, level):
    OPERATION_VALUE = 1
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return HACK_TERMINATED
    qs = CorporationMembership.objects.filter(member=hack.target)
    if not qs:
        return NO_CORPORATIONS
    return "\n\n".join([x.display for x in qs])


def hack_user_subscriptions(hack, level):
    OPERATION_VALUE = 1
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return HACK_TERMINATED
    qs = hack.target.bankusersubscriptionintermediary_set.all()
    if not qs:
        return NO_SUBSCRIPTIONS
    return "\n\n".join([x.display for x in qs])


def hack_user_security_data(hack, level):
    OPERATION_VALUE = 2
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return HACK_TERMINATED
    return hack.target.get_user_security_data()


def hack_user_police_data(hack, level):
    OPERATION_VALUE = 1
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return HACK_TERMINATED
    return hack.target.get_user_police_data()


def hack_user_misconduct_records(hack, level):
    OPERATION_VALUE = 1
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return HACK_TERMINATED
    reports = MisconductReport.objects.filter(reported_person=hack.target)
    if not reports:
        return _("Немає скарг на користувача")
    return '\n\n'.join([x.police_record_string for x in reports])


def hack_user_bank_history(hack, level):
    OPERATION_VALUE = 2
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return HACK_TERMINATED
    if not BankTransaction.objects.get_user_bank_history(hack.target).order_by('created').exists():
        return _("У користувача немає банківської історії")
    return '\n\n'.join(
        [
            x.user_transaction_log(hack.target) for x in BankTransaction.objects.get_user_bank_history(hack.target).order_by('created')
        ]
    )


def hack_decline_report(hack, level, misconduct_id):
    OPERATION_VALUE = 2
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return HACK_TERMINATED
    report = MisconductReport.objects.filter(reported_person=hack.target, misconduct_id=misconduct_id).first()
    if not report:
        return NO_REPORT_FOUND
    report.decline_report(silent=True)
    return _("Report successfuly declined")


def hack_finish_report(hack, level, misconduct_id):
    OPERATION_VALUE = 3
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return HACK_TERMINATED
    report = MisconductReport.objects.filter(reported_person=hack.target, misconduct_id=misconduct_id).first()
    if not report:
        return NO_REPORT_FOUND
    report.finish_report(silent=True)
    return _("Розгляд скарги успішно завершено")


def hack_delete_report(hack, level, misconduct_id):
    OPERATION_VALUE = 5
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return HACK_TERMINATED
    report = MisconductReport.objects.filter(reported_person=hack.target, misconduct_id=misconduct_id).first()
    if not report:
        return NO_REPORT_FOUND
    report.delete()
    return _("Скаргу успішно видалено")


def hack_create_report(hack, level, reported_id, misconduct_type):
    OPERATION_VALUE = 1
    user = get_user_by_character_id(reported_id)
    if not user:
        return str(_("Немає такого користувача у базі даних. Скаргу не відправлено."))
    misconduct_type = MisconductType.objects.filter(misconduct_code=misconduct_type).first()
    if not misconduct_type:
        return str(_("Немає такого типу правопорушень у базі даних. Скаргу не відправлено"))
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return HACK_TERMINATED
    MisconductReport.create_misconduct_report(hack.target, user, misconduct_type, is_silent=True)
    return _("Скаргу успішно відправлено")


def hack_create_transaction(hack, level, reciever_id, amount):
    OPERATION_VALUE = 5
    try:
        amount = decimal.Decimal(amount)
    except decimal.InvalidOperation:
        return str(_("Некоректна сума"))
    if amount > hack.target.bank_account:
        return str(_('Недостатньо коштів на рахунку'))
    user = get_user_by_character_id(reciever_id)
    if not user:
        return str(_("Не можу знайти отримувача у базі даних; транзакція не надіслана"))
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return HACK_TERMINATED
    BankTransaction.create_transaction(hack.target, user, amount, is_anonymous=True)
    return _("Tранзакцію успішно створено")


def hack_inspect_special(hack, level):
    OPERATION_VALUE = 1
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return HACK_TERMINATED
    if hack.target.has_special_hack_value:
        value = hack.target.special_hack_pro_price * HACK_LEVEL_COST_MAPPING[level]
        return _("Ціль можливо зламати особливим методом; вартість: {value}/{value_1}/{value_2} залежно від команди".format(
            value=value, value_1=value * 3, value_2=value * 5)
        )
    return _("Target hasn't any special hack protocol")


def hack_perform_special(hack, level):
    OPERATION_VALUE = hack.target.special_hack_pro_price
    if not hack.target.has_special_hack_value:
        return _("Немає особливого протоклу зламу; команду не виконано")
    hack.decrease_ticks(OPERATION_VALUE * HACK_LEVEL_COST_MAPPING[level])
    if not hack.is_active:
        return HACK_TERMINATED
    if hack.target.custom_special_hack_text_field:
        return "Проведено особливий злам користувача {char_id}. Результат: {result}".format(
            char_id=hack.target.character_id,
            result=hack.target.custom_special_hack_text_field
        )
    return _("Проведено особливий злам користувача {char_id}. Негайно знайдіть майстрів".format(char_id=hack.target.character_id))


def perform_active_countermeasures(user):
    user.send_message("Використовуються заходи активної протидії...")
    active_sesstions = user.hack_attacks.filter(is_active=True)
    for session in active_sesstions:
        session.is_active = False
        session.save()
        session.hacker.system_heat += 1
        session.hacker.save()
        session.hacker.send_message(f"Ціль використала засоби активної протидії зламу. Злам перервано. Рівень вашої підозрілої активності підвищено до {session.hacker.system_heat}")
    user.send_message("Цілісність захисту відновлено, відміняю підозрілі транзакції...")
    for transaction in user.sent_transactions.filter(is_finished=False).filter(is_cancelled=False):
        transaction.cancel_transaction(reason="Відмінена автоматично як підозріла заходами активної протидії зламу")
    user.send_message("Починаю відновлення активності... зачекайте... процес завершиться не більш ніж за півгодини...")
    user.requests_made_since_last_purge = 1000
    user.save()

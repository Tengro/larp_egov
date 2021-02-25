from larp_egov import celery_app
from larp_egov.apps.law_enforcement.models import MisconductReport, MisconductPenaltyStatus, MisconductReportStatus
from larp_egov.apps.banking.models import BankTransaction
from larp_egov.apps.accounts.models import UserAccount


@celery_app.task
def notify_unassigned_tasks():
    unassigned_tasks = MisconductReport.objects.filter(officer_in_charge=None)
    for item in unassigned_tasks:
        item.notify_unassigmnent_status()


@celery_app.task
def notify_unrevised_tasks():
    unassigned_tasks = MisconductReport.objects.filter(misconduct_status=MisconductReportStatus.REVISED)
    for item in unassigned_tasks:
        item.notify_unassigmnent_status(f"Скарга {item.misconduct_id} все ще на розгляді!")


@celery_app.task
def notify_unresolved_tasks():
    unassigned_tasks = MisconductReport.objects.filter(misconduct_status=MisconductReportStatus.PROCESSED)
    for item in unassigned_tasks:
        item.notify_unassigmnent_status(f"Скарга {item.misconduct_id} все ще в обробці!")


@celery_app.task
def collect_penalties():
    uncollected_penalties = MisconductReport.objects.filter(penalty_status=MisconductPenaltyStatus.PROCESSED)
    service_account = UserAccount.objects.get_service_account()
    for item in uncollected_penalties:
        try:
            BankTransaction.create_transaction(
                item.reported_person,
                service_account,
                item.penalty_amount,
                comment=f"Стягнення за скаргою {item.misconduct_id}"
            )
            item.penalty_status = MisconductPenaltyStatus.CLOSED
            item.save()
            item.finish_report()
        except ValueError:
            item.notify_officer(
                f'Не стягнуто суму стягнення з {item.reported_person.character_id}; недостатньо коштів'
            )

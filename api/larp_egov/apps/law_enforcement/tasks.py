from larp_egov import celery_app
from larp_egov.apps.law_enforcement.models import MisconductReport, MisconductPenaltyStatus
from larp_egov.apps.banking.models import BankTransaction
from larp_egov.apps.accounts.models import UserAccount


@celery_app.task
def notify_unassigned_tasks():
    unassigned_tasks = MisconductReport.objects.filter(officer_in_charge=None)
    for item in unassigned_tasks:
        item.notify_unassigmnent_status()


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
                comment=f"Misconduct penalty for misconduct id {item.uuid}"
            )
            item.penalty_status = MisconductPenaltyStatus.CLOSED
            item.save()
        except ValueError:
            item.notify_officer(
                f'Misconduct penalty from {item.reported_person.character_id} not collected; insufficient funds'
            )
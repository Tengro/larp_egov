from larp_egov import celery_app
from larp_egov.apps.banking.models import BankTransaction, BankSubscription, BankSubscriptionPeriodChoices


@celery_app.task
def finish_pending_transactions():
    for item in BankTransaction.objects.unresolved():
        item.finish_transaction()


@celery_app.task
def collect_six_hours_subscriptions():
    subscriptions = BankSubscription.objects.filter(extraction_period=BankSubscriptionPeriodChoices.SIX)
    for item in subscriptions:
        item.extract_payments()

@celery_app.task
def collect_twelve_hours_subscriptions():
    subscriptions = BankSubscription.objects.filter(extraction_period=BankSubscriptionPeriodChoices.TWELVE)
    for item in subscriptions:
        item.extract_payments()

@celery_app.task
def collect_twenty_four_hours_subscriptions():
    subscriptions = BankSubscription.objects.filter(extraction_period=BankSubscriptionPeriodChoices.PER_DAY)
    for item in subscriptions:
        item.extract_payments()

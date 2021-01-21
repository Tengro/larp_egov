from larp_egov import celery_app
from larp_egov.apps.hacking.models import HackingSession
from larp_egov.apps.accounts.models import UserAccount
from larp_egov.apps.hacking.config import (
    TIMER_TICK_REDUCTION,
    HEAT_DISSIPATION_LEVEL,
    HEAT_ALERT_LEVEL
)


@celery_app.task
def detoriate_active_hacks():
    for item in HackingSession.objects.active():
        item.decrease_ticks(TIMER_TICK_REDUCTION)


@celery_app.task
def raise_system_heat_alarm():
    security_officers = UserAccount.objects.get_security_officers()
    for user in UserAccount.objects.filter(system_heat__gte=HEAT_ALERT_LEVEL):
        for officer in security_officers:
            officer.send_message(f"User {user.characrer_id} generated critical amount of system heat. Hacking activity suspected.")


@celery_app.task
def disspate_heat():
    for user in UserAccount.objects.filter(system_heat__gt=0):
        user.system_heat -= HEAT_DISSIPATION_LEVEL
        if user.system_heat < 0:
            user.system_heat = 0
        user.save()

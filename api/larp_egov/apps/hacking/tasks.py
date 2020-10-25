from larp_egov import celery_app
from larp_egov.apps.hacking.models import HackingSession
from larp_egov.apps.hacking.config import TIMER_TICK_REDUCTION


@celery_app.task
def detoriate_active_hacks():
    for item in HackingSession.objects.active():
        item.decrease_ticks(TIMER_TICK_REDUCTION)

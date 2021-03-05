from ..django import TIME_ZONE as DJANGO_TIME_ZONE
from ..environment import env
from celery.schedules import crontab


CELERY_TASK_ALWAYS_EAGER = env.bool("LARP_EGOV_CELERY_TASK_ALWAYS_EAGER", default=False)
CELERY_BROKER_URL = env.str("LARP_EGOV_CELERY_BROKER", default="redis://redis:6379/1")
CELERY_RESULT_BACKEND = env.str("LARP_EGOV_CELERY_RESULT_BACKEND", default="rpc://")

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = DJANGO_TIME_ZONE

CELERY_BEAT_SCHEDULE = {
    'six_hour_subscriptions': {
        'task': 'larp_egov.apps.banking.tasks.collect_six_hours_subscriptions',
        'schedule': crontab(
            minute='0',
            hour='*/6'
        ),
    },
    'twelve_hour_subscriptions': {
        'task': 'larp_egov.apps.banking.tasks.collect_twelve_hours_subscriptions',
        'schedule': crontab(
            minute='0',
            hour='*/12'
        ),
    },
    'per_day_subscriptions': {
        'task': 'larp_egov.apps.banking.tasks.collect_twenty_four_hours_subscriptions',
        'schedule': crontab(
            minute='30',
            hour='23'
        ),
    },
    'finish_transactions': {
        'task': 'larp_egov.apps.banking.tasks.finish_pending_transactions',
        'schedule': crontab(
            minute='*/5',
        ),
    },
    'detoriate_hacks': {
        'task': 'larp_egov.apps.hacking.tasks.detoriate_active_hacks',
        'schedule': crontab(
            minute='*/3',
        ),
    },
    'raise_heat_alarm': {
        'task': 'larp_egov.apps.hacking.tasks.raise_system_heat_alarm',
        'schedule': crontab(
            minute='*/30',
        ),
    },
    'disspate_heat': {
        'task': 'larp_egov.apps.hacking.tasks.disspate_heat',
        'schedule': crontab(
            minute='0',
        ),
    },
    'collect_penalties': {
        'task': 'larp_egov.apps.law_enforcement.tasks.collect_penalties',
        'schedule': crontab(
            minute='0',
            hour='*/3'
        ),
    },
    'notify_assignments': {
        'task': 'larp_egov.apps.law_enforcement.tasks.notify_unassigned_tasks',
        'schedule': crontab(
            minute='0',
            hour='*/3'
        ),
    },
    'notify_revisions': {
        'task': 'larp_egov.apps.law_enforcement.tasks.notify_unrevised_tasks',
        'schedule': crontab(
            minute='0',
            hour='*/6'
        ),
    },
    'notify_resolutions': {
        'task': 'larp_egov.apps.law_enforcement.tasks.notify_unresolved_tasks',
        'schedule': crontab(
            minute='0',
            hour='*/8'
        ),
    },
    'purge_call_count': {
        'task': 'larp_egov.apps.common.tasks.purge_call_count',
        'schedule': crontab(
            minute='*/30',
        ),
    },
    # 'refresh_hook': {
    #     'task': 'larp_egov.apps.common.tasks.refresh_hook',
    #     'schedule': crontab(
    #         minute='*/5'
    #     )
    # }
}

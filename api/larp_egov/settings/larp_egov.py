from datetime import timedelta

from .environment import env


LARP_EGOV_FEATURES = env.list("LARP_EGOV_FEATURES", default=[])

LARP_EGOV_EMAIL_FROM = env.str("LARP_EGOV_EMAIL_FROM", default="no-reply@example.com")

LARP_EGOV_AUTH_COOKIE_NAME = env.str("LARP_EGOV_AUTH_COOKIE_NAME", default="a")

# Reset password link lifetime interval (in seconds). By default: 1 hour.
LARP_EGOV_RESET_PASSWORD_EXPIRATION_DELTA = timedelta(seconds=env.int("LARP_EGOV_RESET_PASSWORD_EXPIRATION_DELTA", default=3600))

LIVE_SUBSCRIPTIONS = False

if "LOG_SQL" in LARP_EGOV_FEATURES:  # pragma: no cover
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {"require_debug_true": {"()": "django.utils.log.RequireDebugTrue"}},
        "formatters": {
            "simple": {"format": "[%(asctime)s] %(levelname)s %(message)s"},
            "verbose": {"format": "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"},
            "sql": {"()": "larp_egov.loggers.SQLFormatter", "format": "[%(duration).3f] %(statement)s"},
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "verbose", "level": "DEBUG"},
            "sql": {"class": "logging.StreamHandler", "formatter": "sql", "level": "DEBUG"},
        },
        "loggers": {
            "django.db.backends": {
                "handlers": ["sql"],
                "level": "DEBUG",
                "filters": ["require_debug_true"],
                "propagate": False,
            },
            "django.db.backends.schema": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        },
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

DJANGO_TELEGRAMBOT = {

    'MODE' : env.str("LARP_EGOV_BOT_MODE", default='POLLING'), #(Optional [str]) # The default value is WEBHOOK,
                        # otherwise you may use 'POLLING'
                        # NB: if use polling you must provide to run
                        # a management command that starts a worker

    'WEBHOOK_SITE' : 'https://atomlarp.com',
    'WEBHOOK_PREFIX' : '/bot', # (Optional[str]) # If this value is specified,
                                  # a prefix is added to webhook url

    #'WEBHOOK_CERTIFICATE' : 'cert.pem', # If your site use self-signed
                         #certificate, must be set with location of your public key
                         #certificate.(More info at https://core.telegram.org/bots/self-signed )


    'BOTS' : [
        {
           'TOKEN': env.str("LARP_EGOV_BOT_TOKEN"), #Your bot token.

           #'ALLOWED_UPDATES':(Optional[list[str]]), # List the types of
                                                   #updates you want your bot to receive. For example, specify
                                                   #``["message", "edited_channel_post", "callback_query"]`` to
                                                   #only receive updates of these types. See ``telegram.Update``
                                                   #for a complete list of available update types.
                                                   #Specify an empty list to receive all updates regardless of type
                                                   #(default). If not specified, the previous setting will be used.
                                                   #Please note that this parameter doesn't affect updates created
                                                   #before the call to the setWebhook, so unwanted updates may be
                                                   #received for a short period of time.

           #'TIMEOUT':(Optional[int|float]), # If this value is specified,
                                   #use it as the read timeout from the server

           #'WEBHOOK_MAX_CONNECTIONS':(Optional[int]), # Maximum allowed number of
                                   #simultaneous HTTPS connections to the webhook for update
                                   #delivery, 1-100. Defaults to 40. Use lower values to limit the
                                   #load on your bot's server, and higher values to increase your
                                   #bot's throughput.

           #'POLL_INTERVAL' : (Optional[float]), # Time to wait between polling updates from Telegram in
                           #seconds. Default is 0.0

           #'POLL_CLEAN':(Optional[bool]), # Whether to clean any pending updates on Telegram servers before
                                   #actually starting to poll. Default is False.

           #'POLL_BOOTSTRAP_RETRIES':(Optional[int]), # Whether the bootstrapping phase of the `Updater`
                                   #will retry on failures on the Telegram server.
                                   #|   < 0 - retry indefinitely
                                   #|     0 - no retries (default)
                                   #|   > 0 - retry up to X times

           #'POLL_READ_LATENCY':(Optional[float|int]), # Grace time in seconds for receiving the reply from
                                   #server. Will be added to the `timeout` value and used as the read timeout from
                           #server (Default: 2).
        },
        #Other bots here with same structure.
    ],

}
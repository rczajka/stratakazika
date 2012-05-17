from datetime import timedelta

BROKER_URL = "django://"

CELERYBEAT_SCHEDULE = {
    "steal": {
        "task": "strata.tasks.steal",
        "schedule": timedelta(seconds=10),
    },
}

CELERY_DISABLE_RATE_LIMITS = True

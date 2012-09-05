from shutil import copy
from tempfile import mktemp
from celery.task import task
from django.conf import settings
from strata import api


@task(ignore_result=True)
def steal():
    if hasattr(settings, 'STRATA_COPY_SOURCE'):
        out_path = mktemp(prefix='pirate-copy-',
                          dir=getattr(settings, 'STRATA_COPY_DIR'))
        copy(settings.STRATA_COPY_SOURCE, out_path)
    api.inc_the_counter()


@task(ignore_result=True)
def inc_counter_by_name(name):
    api.inc_counter_by_name(name)


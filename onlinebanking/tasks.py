from __future__ import absolute_import, unicode_literals

import logging
logger = logging.getLogger(__name__)

import random
from datetime import datetime as dt
from datetime import timedelta
from decimal import *

from django.utils.timezone import make_aware
from django.core.management import call_command
from django.conf import settings
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from .models import User, Account, Transaction

@periodic_task(run_every=crontab(hour=0))
def generate_transaction():
    pass
    #call_command('mocktransactions', '--numdays=1')

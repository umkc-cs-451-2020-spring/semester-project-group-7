import logging
logger = logging.getLogger(__name__)

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware

from onlinebanking.models import User, Account, Transaction


class Command(BaseCommand):
    def handle(self, *args, **options):

        mock_accounts = Account.objects.filter(mock_transactions=True)
        logger.info(mock_accounts)
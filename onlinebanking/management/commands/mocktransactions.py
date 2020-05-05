import logging
logger = logging.getLogger(__name__)

import random
from datetime import datetime as dt
from datetime import timedelta
import time
from decimal import *

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware
from django.db.models import F

from onlinebanking.models import User, Account, Transaction


class Command(BaseCommand):
    help = 'Generate transactions'
    def add_arguments(self, parser):
        parser.add_argument(
            '--numdays',
            nargs='+',
            type=int,
        )

    def handle(self, *args, **options):
        logger.info(f'Generating transactions')
        transactions = {
            1: {
                "Gaming computer": (-2000,-3500),
                "Washer and dryer": (-1500,-2500),
                "User car": (-4000,-5500),
                "Sky diving": (-1000,-1750),
                "VR Headset": (-1500,-1600),
                "Bonus": (5000,7000),
            },
            10: {
                "Computer game": (-30, -75),
                "Candy": (-1, -15),
                "Olive Garden": (-35, -85),
                "Paycheck": (2000, 2500),
                "Ebay sale": (50, 90),
                "Internet bill": (-50, -50),
                "Water bill": (-50, -90),
                "Electricity bill": (-100, 10),
            },
            7: {
                "Paycheck": (1000, 1250),
            },
            33: {
                "Gas": (-15, -45),
                "Fast food": (-15, -45),
            },
            50: {
                "Groceries": (-50, -150),
                "Amazon": (-30, -450),
                "Coffee": (-5, -7),
            },
        }

        mock_accounts = Account.objects.filter(mock_transactions=True)
        numdays = 180  #6 months
        if options['numdays']:
            numdays = options['numdays'][0]

        for account in mock_accounts:
            now = dt.now()
            logger.info(f'Account: {account}')

            past = now - timedelta(days=numdays)
            if Transaction.objects.filter(account=account,posted__gte=make_aware(past)).exists():
                account.mock_transactions = False
                account.save()
                logger.warn("Transactions exist after mock data start date. You about broke something...")
                continue

            bulk_transactions = []
            balance = account.balance
            last_transaction_number = account.last_transaction_number

            for date in reversed([now - timedelta(days=x) for x in range(numdays)]):
                date = date.replace(hour=0, minute=0, second=0)
                num_transactions = random.choices([0,1,2,3,4,5],[0.14, 0.19, 0.44, 0.11, 0.07, 0.05])[0]
                
                if not num_transactions:
                    continue # none today go to next day

                for posted in sorted([make_aware(date + timedelta(minutes=random.randint(0,1440))) for x in range(num_transactions)]):

                    transaction_group = random.choices(list(transactions.values()), [x/100 for x in transactions.keys()])[0]
                    desc = random.choice(list(transaction_group.keys()))
                    min_amt, max_amt = sorted(transaction_group[desc])
                    amount = Decimal(random.randint(min_amt * 100, max_amt * 100) / 100)

                    balance = balance + amount
                    
                    if balance <= -50:
                        continue # account balance too low

                    last_transaction_number += 1

                    bulk_transactions.append(Transaction(
                        account=account,
                        transaction_number=last_transaction_number,
                        balance=balance,
                        posted=posted,
                        amount=amount,
                        description=desc,
                    ))

                    logger.info(
                        f'\naccount={account}, '
                        f'transaction_number={last_transaction_number}, '
                        f'balance={balance:.2f}, '
                        f'posted={posted}, '
                        f'amount={amount:.2f}, '
                        f'description={desc}, '
                    )

            for trans in bulk_transactions:
                acct = Account.objects.get(pk=account.pk)
                acct.last_transaction_number = trans.transaction_number
                acct.balance = trans.balance
                acct.save()
                time.sleep(.04)
                trans.save()
                time.sleep(.06)

            acct.mock_transactions = False
            acct.save()

import django_filters
from larp_egov.apps.banking.models import BankTransaction
from larp_egov.apps.accounts.models import UserAccount


class BankTransactionFilter(django_filters.FilterSet):

    class Meta:
        model = BankTransaction
        fields = [
            'amount', 'sender', 'reciever',
            'is_finished', 'is_cancelled',
        ]

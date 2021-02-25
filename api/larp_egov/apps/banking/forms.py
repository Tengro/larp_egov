from larp_egov.apps.banking.models import BankTransaction
from django.forms import ModelForm
from django.core.exceptions import ValidationError


class BankTransactionModelForm(ModelForm):
    class Meta:
        model = BankTransaction
        fields = ('reciever', 'amount', 'comment')

        # if sender.bank_account < amount:
        #     raise ValueError('Bank account insufficient')

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            ValidationError(_("Value is too low!"))
        return amount

    def save(self):
        transaction = super().save()
        transaction.send_creation_message()
        return transaction

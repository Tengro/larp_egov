from larp_egov.apps.banking.models import BankTransaction
from django.forms import ModelForm, IntegerField
from django.core.exceptions import ValidationError
from larp_egov.apps.accounts.selectors import get_user_by_character_id
from django.utils.translation import ugettext_lazy as _


class BankTransactionModelForm(ModelForm):
    reciever = IntegerField()

    class Meta:
        model = BankTransaction
        fields = ('reciever', 'amount', 'comment')

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise ValidationError(_("Занадто мала сума!"))
        if self.sender.bank_account < amount:
            raise ValueError('Недостатньо коштів на рахунку')
        return amount

    def clean_reciever(self):
        reciever = self.cleaned_data['reciever']
        user = get_user_by_character_id(reciever)
        if not user:
            raise ValidationError(_("Користувач з таким ID не знайдений. Транзакція не надіслана"))
        return user

    def save(self):
        transaction = super().save()
        transaction.sender = self.sender
        transaction.save()
        transaction.send_creation_message()
        return transaction

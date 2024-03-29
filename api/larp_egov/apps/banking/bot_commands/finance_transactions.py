import decimal
from django.utils.translation import ugettext_lazy as _
from larp_egov.apps.accounts.selectors import (
    get_user_by_character_id, get_user_by_telegram_id,
)
from larp_egov.apps.accounts.models import UserAccount
from larp_egov.apps.banking.models import BankTransaction
from larp_egov.apps.common.bot_commands._common_texts import UNREGISTERED, NO_ACCESS_DATA, NO_USER, validate_security


def get_own_bank_data(update):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not BankTransaction.objects.get_user_bank_history(requester).order_by('created').exists():
        return "Немає банківських транзакцій"
    return '\n\n'.join(
        [
            x.user_transaction_log(requester) for x in BankTransaction.objects.get_user_bank_history(requester).order_by('created')
        ]
    )


def get_full_bank_data(update, override_permissions=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not validate_security(requester) and not override_permissions:
        return NO_ACCESS_DATA
    if not BankTransaction.objects.all().exists():
        return "Немає банківських транзакцій"
    return '\n\n'.join(
        [
            x.transaction_log for x in BankTransaction.objects.all().order_by('created')
        ]
    )


def get_user_bank_data(update, override_permissions=False, is_full=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    if not validate_security(requester) and not override_permissions:
        return NO_ACCESS_DATA
    code = update.message.text[23:]
    user = get_user_by_character_id(code)
    if not user:
        return NO_USER
    if not BankTransaction.objects.get_user_bank_history(requester).order_by('created').exists():
        return "Немає банківських транзакцій"
    if not is_full:
        return '\n\n'.join(
            [
                x.user_transaction_log(user) for x in BankTransaction.objects.get_user_bank_history(user).order_by('created')
            ]
        )
    return '\n\n'.join(
            [
                x.transaction_log for x in BankTransaction.objects.get_user_bank_history(user).order_by('created')
            ]
        )


def create_transaction(update, is_anonymous=False):
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    message = update.message.text[6:]
    result_data = message.split(' ')
    if len(result_data) == 2:
        user_code, amount = result_data
        comment = ''
    elif len(result_data) > 2:
        user_code = result_data[0]
        amount = result_data[1]
        comment = ' '.join(result_data[2:])
    user = get_user_by_character_id(user_code)
    if not user:
        return _("Користувач з таким ID не знайдений. Транзакція не надіслана")
    try:
        amount = decimal.Decimal(amount)
    except decimal.InvalidOperation:
        return _("Сума не розпізнана")
    try:
        BankTransaction.create_transaction(requester, user, amount, is_anonymous, comment)
    except ValueError as e:
        return f'{e}'


def cancel_transaction(update):

    service_account = UserAccount.objects.get_service_account()
    requester = get_user_by_telegram_id(update.message.chat_id)
    if not requester:
        return UNREGISTERED
    transaction_id = update.message.text[8:]
    transaction = BankTransaction.objects.unresolved().filter(sender=requester).filter(transaction_id=transaction_id).first()
    if not transaction:
        return str(_("Не можу знайти відповідну транзакціию. Перевірте ІД транзакції"))
    if transaction.reciever == service_account:
        return str(_("Транзакції на рахунок TengrOS не можуть бути відмінені"))
    transaction.cancel_transaction()

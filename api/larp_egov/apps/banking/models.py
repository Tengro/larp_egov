from django.db import models
from django.conf import settings
from django.utils.timezone import now
from larp_egov.apps.common.models import CoreModel, CoreManager, CoreQuerySet
from larp_egov.apps.accounts.models import UserAccount
from larp_egov.apps.law_enforcement.models import MisconductReport
from django_extensions.db.fields import RandomCharField
from django.utils.translation import ugettext_lazy as _


class BankTransactionQuerySet(CoreQuerySet):
    def finished(self):
        return self.filter(is_finished=True)

    def cancelled(self):
        return self.filter(is_cancelled=True)

    def unresolved(self):
        return self.filter(is_finished=False).filter(is_cancelled=False)

    def get_user_bank_history(self, user):
        return self.filter(models.Q(sender=user) | models.Q(reciever=user))


class BankTransactionManager(CoreManager):
    def get_queryset(self):
        return BankTransactionQuerySet(self.model, using=self._db).select_related('sender', 'reciever')

    def get_user_bank_history(self, user):
        return self.get_queryset().get_user_bank_history(user)

    def finished(self):
        return self.get_queryset().finished()

    def cancelled(self):
        return self.get_queryset().cancelled()

    def unresolved(self):
        return self.get_queryset().unresolved()


class BankTransaction(CoreModel):
    amount = models.DecimalField(max_digits=12, decimal_places=1, null=True)
    sender = models.ForeignKey(UserAccount, related_name='sent_transactions', null=True, on_delete=models.SET_NULL)
    reciever = models.ForeignKey(UserAccount, related_name='recieved_transactions', null=True, on_delete=models.SET_NULL)
    is_anonymous = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    time_finished = models.DateTimeField(null=True, blank=True)
    comment = models.CharField(max_length=512, blank=True, null=True)
    transaction_id = RandomCharField(length=12, include_alpha=False, unique=True, null=True)

    objects = BankTransactionManager()

    @property
    def trransaction_status(self):
        if self.is_finished:
            return 'ЗАВЕРШЕНО'
        if self.is_cancelled:
            return 'ВІДМІНЕНО'
        return 'НА РОЗГЛЯДІ'

    @property
    def transaction_log(self):
        return f"{self.transaction_id} | {self.sender} -> {self.reciever}: {self.amount}; status: {self.trransaction_status}; {self.comment}"

    def user_transaction_log(self, user):
        sender = self.sender
        reciever = self.reciever
        if self.is_anonymous and self.sender == user:
            reciever = 'АНОНІМ'
        elif self.is_anonymous and self.reciever == user:
            sender = 'АНОНІМ'
        return f"{self.transaction_id} | {sender} -> {reciever}: {self.amount}; status: {self.trransaction_status}; {self.comment}"

    @classmethod
    def create_transaction(cls, sender, reciever, amount, is_anonymous=False, comment=''):
        if sender.bank_account < amount:
            raise ValueError('Недостатньо коштів на рахунку')
        if amount <= 0:
            raise ValueError('Занадто мале значення!')
        transaction = cls.objects.create(
            sender=sender,
            reciever=reciever,
            amount=amount,
            is_anonymous=is_anonymous,
            comment=comment
        )
        transaction.send_creation_message()

    def send_creation_message(self):
        creation_message = f'Транзакція {self.transaction_id} створена.'
        if self.comment:
            creation_message += f' Коментар до транзакції: {self.comment}'
        self.sender.withdraw(self.amount, creation_message)
        self.reciever.send_message(creation_message)

    def cancel_transaction(self, reason=None):
        if self.is_cancelled or self.is_finished:
            return
        cancell_message = f'Транзакцію {self.transaction_id} відмінено.'
        if reason:
            cancell_message += f' Reason: {reason}'
        self.sender.deposit(self.amount, cancell_message)
        self.reciever.send_message(cancell_message)
        self.is_cancelled = True
        self.save()

    def finish_transaction(self):
        if self.is_finished or self.is_cancelled:
            return
        approve_message = f'Транзакцію {self.transaction_id} успішно завершено'
        self.is_finished = True
        self.time_finished = now()
        self.sender.send_message(approve_message)
        self.reciever.deposit(self.amount, approve_message)
        self.save()


class BankSubscriptionPeriodChoices(models.IntegerChoices):
    SIX = 6, "Раз на шість годин"
    TWELVE = 12, "Раз на дванадцять годин"
    PER_DAY = 24, "Раз на двадцять чотири години"


class BankUserSubscriptionIntermediary(CoreModel):
    subscriber = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    subscription = models.ForeignKey('BankSubscription', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=True)
    subscription_request_id = RandomCharField(length=5, include_alpha=False, unique=True, null=True)

    def approve_subscription(self, user):
        service_account = UserAccount.objects.get_service_account()
        if not user.is_staff:
            raise ValueError("Incorrect user")
        try:
            BankTransaction.create_transaction(
                user,
                service_account,
                self.subscription.amount,
                comment=f"Регулярний платіж: {self.subscription.title}"
            )
        except ValueError:
            subscriber.send_message('Недостатньо коштів на рахунку. Запит відхилено.')
            user.send_message('Недостатньо коштів на рахунку. Запит відхилено.')
            self.delete()
            return
        self.is_approved = True
        self.save()
        self.subscriber.send_message(f'Ваш запит на ліцензію {self.subscription.title} задовольнили.')

    @property
    def display(self):
        result = self.subscription.display
        if not self.is_approved:
            result += f"ОЧІКУЄ НА РОЗГЛЯД; ID ЗАПИТУ {self.subscription_request_id}"
        return result


class BankSubscription(CoreModel):
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=1, null=True)
    subscribers = models.ManyToManyField(
        UserAccount,
        related_name='subscriptions',
        through='BankUserSubscriptionIntermediary'
    )
    is_governmental_tax = models.BooleanField(default=False)
    extraction_period = models.IntegerField(
        choices=BankSubscriptionPeriodChoices.choices,
        default=BankSubscriptionPeriodChoices.PER_DAY
    )
    limited_approval = models.BooleanField(default=False)
    subscription_id = RandomCharField(length=4, include_alpha=False, unique=True, null=True)

    @property
    def display(self):
        result = f"{self.subscription_id}: {self.title}. {self.description}"
        if self.is_governmental_tax:
            result += " ОБОВ'ЯЗКОВИЙ ПЛАТІЖ!"
        return result

    def extract_payments(self):
        service_account = UserAccount.objects.get_service_account()
        for user in self.subscribers.all():
            intermediary = BankUserSubscriptionIntermediary.objects.filter(
                subscriber=user,
                subscription=self
            ).first()
            if not intermediary or not itermediary.is_approved:
                continue
            try:
                BankTransaction.create_transaction(
                    user,
                    service_account,
                    self.amount,
                    comment=f"Регулярний платіж: {self.title}"
                )
            except ValueError:
                self.process_payment_failure(user)

    def cancel_subscription(self, user, forced=False):
        if self.is_governmental_tax and not forced:
            user.send_message("Обов'язковий платіж неможливо відмінити без дозвошу ШІ. Зв'язжіться з ШІ")
            return
        self.subscribers.remove(user)
        user.send_message(f"Дія ліцензії {self.title} зупинена за вашим запитом")

    def create_subscription(self, user):
        service_account = UserAccount.objects.get_service_account()
        if self.limited_approval:
            self.subscribers.add(user, through_defaults={'is_approved': False})
            self.notify_ai_for_approval(user)
            user.send_message('Запит на ліцензію надіслано до ШІ')
            return
        try:
            BankTransaction.create_transaction(
                user,
                service_account,
                self.amount,
                comment=f"Регулярний платіж: {self.title}"
            )
        except ValueError:
            user.send_message('Недостатньо коштів для отримання ліцензії')
            return
        user.send_message('Ліцензію надано!')
        self.subscribers.add(user)

    def notify_ai_for_approval(self, user):
        itermediary = BankUserSubscriptionIntermediary.objects.get(subscription=self, is_approved=False, subscriber=user)
        ai_accounts = UserAccount.objects.get_ai_accounts()
        for user in ai_accounts:
            user.send_message(f'Необхідно підтвердити ліцензію для {user.character_id}, тип ліцензії {self.title}, id запиту: {itermediary.subscription_request_id}')

    def process_payment_failure(self, user):
        service_account = UserAccount.objects.get_service_account()
        if self.is_governmental_tax:
            insufficient_payment = self.amount - user.bank_account
            BankTransaction.create_transaction(
                user,
                service_account,
                user.bank_account,
                comment=f"Регулярний обов'язковий платіж: {self.title}; частина"
            )
            MisconductReport.create_tax_related_report(user, insufficient_payment)
            user.send_message(f'Платіж {self.title} не сплачено; скарга на несплату надіслана автоматично')
        else:
            self.cancel_subscription(user)
            user.send_message(f'Ліцензію {self.title} зупинено через несплату')


class CorporationStatus(models.IntegerChoices):
    AFFILIATED = 1, "Членство"
    MEMBER = 2, "Членство з доступом до фінансів"
    PRIVILEDGED_MEMBER = 3, "Членство з доступом до фінансів та списку учасників"
    EXECUTIVE = 4, "Повне необмежене членство"


class CorporationMembership(CoreModel):
    corporation = models.ForeignKey('Corporation', on_delete=models.CASCADE)
    member = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    status = models.IntegerField(choices=CorporationStatus.choices, default=CorporationStatus.AFFILIATED)

    @property
    def display(self):
        return f"{self.member}\n{self.corporation.display};\n{self.get_status_display()}"


class Corporation(CoreModel):
    linked_account = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    members = models.ManyToManyField(UserAccount, through=CorporationMembership, related_name='corporate_membership')
    title = models.CharField(max_length=512)

    @property
    def display(self):
        return f'{self.title}.\nID корпорації: {self.corporation_id}'

    @property
    def corporation_id(self):
        return self.linked_account.character_id

    @property
    def corporation_bank_account(self):
        return self.linked_account.bank_account

    def check_permission(self, user, lowest_level, override_access=False):
        membership = CorporationMembership.objects.filter(corporation=self, member=user).first()
        if (not membership or membership.status < lowest_level) and not override_access:
            user.send_message(_('Недостатній рівень доступу'))
            return False
        return True

    def display_members(self, user, override_access=False):
        if not self.check_permission(user, CorporationStatus.PRIVILEDGED_MEMBER, override_access=override_access):
            return
        return '\n\n'.join([x.display for x in CorporationMembership.objects.filter(corporation=self)])

    def display_transaction_history(self, user, override_access=False):
        if not self.check_permission(user, CorporationStatus.EXECUTIVE, override_access=override_access):
            return
        return '\n\n'.join([x.user_transaction_log(user) for x in BankTransaction.objects.get_user_bank_history(self.linked_account).order_by('created')])

    def display_account_data(self, user, override_access=False):
        if not self.check_permission(user, CorporationStatus.MEMBER, override_access=override_access):
            return
        return _("{title}. \nID корпорації {corporation_id}. \nСтан рахунку: {funds}.".format(
            title=self.title, corporation_id=self.corporation_id, funds=self.corporation_bank_account,
        ))

    def withdraw_funds(self, user, amount):
        if not self.check_permission(user, CorporationStatus.MEMBER):
            return
        BankTransaction.create_transaction(self.linked_account, user, amount)

    def deposit_funds(self, user, amount):
        if not self.check_permission(user, CorporationStatus.AFFILIATED):
            return
        BankTransaction.create_transaction(user, self.linked_account, amount)

    def add_user(self, adder, user):
        if not self.check_permission(adder, CorporationStatus.EXECUTIVE):
            return
        user.send_message(f"Вас було додано до корпорації {self.title}!")
        self.members.add(user)

    def remove_user(self, remover, user):
        if not self.check_permission(remover, CorporationStatus.EXECUTIVE):
            return
        user.send_message(f"Вас було викинуто з корпорації {self.title}!")
        self.members.remove(user)

    def promote_user(self, promoter, user):
        if not self.check_permission(promoter, CorporationStatus.EXECUTIVE):
            promoter.send_message("Вашого статусу недостатньо")
            return
        membership = CorporationMembership.objects.filter(corporation=self, member=user).first()
        if not membership:
            promoter.send_message(f'Користвуач {user.character_id} не є членом корпорації!')
            return
        if membership.status == CorporationStatus.EXECUTIVE:
            promoter.send_message(f'Користвуач {user.character_id} уже найвищого рівня!')
            return
        membership.status += 1
        membership.save()
        promoter.send_message(f'Користвуача {user.character_id} підвищено!')
        user.send_message(f'Вас підвищили у корпорації {self.title}!')
        return

    def demote_user(self, demoter, user):
        if not self.check_permission(demoter, CorporationStatus.EXECUTIVE):
            return
        membership = CorporationMembership.objects.filter(corporation=self, member=user).first()
        if not membership:
            demoter.send_message(f'Користвуач {user.character_id} не є членом корпорації!')
            return
        if membership.status == CorporationStatus.AFFILIATED:
            demoter.send_message(f'Корстувач {user.character_id} уже найнижчого рівня!')
            return
        membership.status -= 1
        membership.save()
        demoter.send_message(f'Користвуача {user.character_id} понижено!')
        user.send_message(f'Вас понизили у корпорації {self.title}')
        return

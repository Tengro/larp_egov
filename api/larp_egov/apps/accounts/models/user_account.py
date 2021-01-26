import random
import string

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django_extensions.db.fields import RandomCharField
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.utils.translation import ugettext_lazy as _
from django_telegrambot.apps import DjangoTelegramBot
from larp_egov.apps.common.bot_commands.safe_message_send import safe_message_send


from larp_egov.apps.common import models as core_models
from larp_egov.apps.common.models import CoreModel


class UserManager(core_models.CoreManager, BaseUserManager):
    def get_queryset(self):
        return core_models.CoreQuerySet(self.model, using=self._db)

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must give an email address")

        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def get_service_account(self):
        return self.get_queryset().get(is_service_account=True)

    def get_ai_accounts(self):
        return self.get_queryset().filter(is_staff=True)

    def get_police_officers(self):
        return self.get_queryset().filter(is_police=True)

    def get_security_officers(self):
        return self.get_queryset().filter(is_security=True) 


class UserAccount(PermissionsMixin, CoreModel, AbstractBaseUser):

    email = models.EmailField(verbose_name=gettext_lazy("Email"), max_length=128, unique=True)
    is_service_account = models.BooleanField(default=False)
    first_name = models.CharField(verbose_name=gettext_lazy("first name"), max_length=30, blank=True, null=True)
    last_name = models.CharField(verbose_name=gettext_lazy("last name"), max_length=30, blank=True, null=True)
    is_staff = models.BooleanField(
        gettext_lazy("staff status"),
        default=False,
        help_text=gettext_lazy("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        gettext_lazy("active"),
        default=True,
        help_text=gettext_lazy(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(default=timezone.now)
    date_of_birth = models.DateField(null=True)
    telegram_id = models.CharField(max_length=512, null=True, blank=True)
    character_id = RandomCharField(length=6, include_alpha=False, unique=True, null=True)
    place_of_work = models.CharField(max_length=512, null=True)
    bank_account = models.DecimalField(max_digits=12, decimal_places=1, default=0)
    is_verified = models.BooleanField(
        gettext_lazy("verified"),
        default=False,
        help_text=gettext_lazy(
            "Designates whether this user should have access to game functionality."
        ),
    )
    police_comment_field = models.TextField(null=True, blank=True)
    security_comment_field = models.TextField(null=True, blank=True)
    is_police = models.BooleanField(
        gettext_lazy("police"),
        default=False,
        help_text=gettext_lazy(
            "Designates whether this user should have access to police functionality."
        ),
    )
    is_security = models.BooleanField(
        gettext_lazy("security"),
        default=False,
        help_text=gettext_lazy(
            "Designates whether this user should have access to security functionality."
        ),
    )
    is_hacker = models.BooleanField(
        gettext_lazy("hacker"),
        default=False,
        help_text=gettext_lazy(
            "Designates whether this user should have access to hacker functionality."
        ),
    )
    is_corporate_fiction_account = models.BooleanField(
        gettext_lazy("corporative fiction"),
        default=False,
        help_text=gettext_lazy(
            "Designates whether this user is pure corporative fiction"
        ),
    )
    complex_service_acc = models.BooleanField(
        gettext_lazy("service acc"),
        default=False,
        help_text=gettext_lazy(
            "Designates whether has ComplexHack property"
        ),
    )
    defence_level = models.IntegerField(default=0)
    system_heat = models.IntegerField(default=0)
    has_special_hack_value = models.BooleanField(default=False)
    special_hack_pro_price = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("first_name", "last_name")

    def __str__(self):
        return f"{self.full_name} [id {self.character_id}]"

    @property
    def display_data(self):
        return self.__str__()

    def get_short_name(self) -> str:
        return str(self.email)

    def get_full_name(self) -> str:
        if self.first_name and self.last_name:
            full_name = f"{self.first_name} {self.last_name}"
        else:
            full_name = self.get_short_name()
        return full_name

    @property
    def full_name(self):
        return self.get_full_name()

    @property
    def notification_salutation(self):
        if self.first_name and self.last_name:
            salutation = f"{self.first_name} {self.last_name}"
        else:
            salutation = gettext_lazy("Dear client")
        return salutation

    def send_message(self, text):
        if self.telegram_id:
            dp = DjangoTelegramBot.dispatcher.bot
            safe_message_send(dp, self.telegram_id, str(text))

    def withdraw(self, amount, message):
        self.bank_account = self.bank_account - amount
        self.send_message(message)
        self.save()

    def deposit(self, amount, message):
        self.bank_account = self.bank_account + amount
        self.send_message(message)
        self.save()

    @property
    def security_comment_string(self):
        return _('Security comment: {security_comment_field}').format(security_comment_field=self.security_comment_field)

    @property
    def police_comment_string(self):
        return _('Police comment: {police_comment_field}').format(police_comment_field=self.police_comment_field)

    @property
    def common_introspect_data(self):
        id_string = _('Citizen ID: {character_id}').format(character_id=self.character_id)
        name_string = _("Name: {full_name}.").format(full_name=self.full_name)
        work_string = _("Workplace: {place_of_work}.").format(place_of_work=self.place_of_work)
        date_of_birth = _("Date of birth: {date_of_birth}").format(date_of_birth=self.date_of_birth)
        return f"{id_string}\n{name_string}\n{work_string}\n{date_of_birth}\n"

    def get_user_introspect(self):
        account_string = _("Available funds: {bank_account}").format(bank_account=self.bank_account)
        defence_string = _("Personal data defence level: {defence_level}").format(defence_level=self.defence_level)
        result = f"{self.common_introspect_data}{account_string}\n{defence_string}"
        return result

    def get_user_police_data(self):
        result = f"{self.common_introspect_data}{self.police_comment_string}"
        return result

    def get_user_security_data(self):
        introspect = self.get_user_introspect()
        result = f"{introspect}\n{self.security_comment_string}"
        return result

    def get_full_user_introspect(self):
        introspect = self.get_user_introspect()
        result = f"{introspect}\n{self.security_comment_string}\n{self.police_comment_string}"
        return result

import random
import string

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django_extensions.db.fields import RandomCharField
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django_telegrambot.apps import DjangoTelegramBot

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
        return self.get_queryset().get(is_staff=True)

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
    telegram_id = models.CharField(max_length=512, null=True)
    character_id = RandomCharField(length=8, lowercase=True, unique=True, null=True)
    place_of_work = models.CharField(max_length=512, null=True)
    bank_account = models.DecimalField(max_digits=12, decimal_places=1, null=True)
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
    defence_level = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("first_name", "last_name")

    def __str__(self):
        return self.email

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
        return self.get_full_name

    @property
    def notification_salutation(self):
        if self.first_name and self.last_name:
            salutation = f"{self.first_name} {self.last_name}"
        else:
            salutation = gettext_lazy("Dear client")
        return salutation

    def send_message(self, text):
        dp = DjangoTelegramBot.dispatcher.bot
        dp.sendMessage(self.telegram_id, text)

    def withdraw(self, amount, message):
        self.bank_account = self.bank_account - amount
        self.send_message(message)
        self.save()

    def deposit(self, amount, message):
        self.bank_account = self.bank_account + amount
        self.send_message(message)
        self.save()

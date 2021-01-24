from django.views.generic.list import ListView

from larp_egov.apps.banking.models import (
    BankSubscription, BankTransaction,
    Corporation, BankUserSubscriptionIntermediary,
    CorporationMembership
)
from django.contrib.auth.mixins import LoginRequiredMixin


class AllSubscriptionsList(LoginRequiredMixin, ListView):
    model = BankSubscription

    template_name = 'banking/all_subscriptions.html'


class AllCorporationList(LoginRequiredMixin, ListView):
    model = Corporation

    template_name = 'banking/all_corporations.html'


class PersonalTransactionList(LoginRequiredMixin, ListView):
    model = BankTransaction

    template_name = 'banking/personal_transactions.html'

    def get_queryset(self):
        user = self.request.user
        return BankTransaction.objects.get_user_bank_history(user)


class PersonalSubscriptionList(LoginRequiredMixin, ListView):
    model = BankUserSubscriptionIntermediary

    template_name = 'banking/personal_subscriptions.html'

    def get_queryset(self):
        user = self.request.user
        return BankUserSubscriptionIntermediary.objects.filter(subscriber=user).select_related('subscription')


class PersonalCorporationMembership(LoginRequiredMixin, ListView):
    model = CorporationMembership

    template_name = 'banking/personal_corporations.html'

    def get_queryset(self):
        user = self.request.user
        return CorporationMembership.objects.filter(member=user).select_related('corporation')

# TODO: Add SubscriptionRequest, TransactionCreate, Transaction Cancel, security views (All transactions + filtering)

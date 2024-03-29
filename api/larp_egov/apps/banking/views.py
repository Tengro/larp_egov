from django.views.generic.list import ListView

from larp_egov.apps.banking.models import (
    BankSubscription, BankTransaction,
    Corporation, BankUserSubscriptionIntermediary,
    CorporationMembership
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from larp_egov.apps.banking.filters import BankTransactionFilter
from larp_egov.apps.banking.forms import BankTransactionModelForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from django.utils.translation import ugettext_lazy as _
from django_filters.views import FilterView


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


class SecurityBankingDashboard(LoginRequiredMixin, UserPassesTestMixin, FilterView):
    model = BankTransaction

    template_name = 'banking/security_transactions_dashboard.html'
    filterset_class = BankTransactionFilter

    def test_func(self):
        return self.request.user.is_security


class BankTransactionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = BankTransactionModelForm
    template_name = 'banking/create_transaction.html'
    success_url = reverse_lazy("banking:personal_transactions")
    success_message = _("Transaction successfully made")

    def get_form_kwargs(self):
        kwargs = super(BankTransactionCreateView, self).get_form_kwargs()
        kwargs['initial']['reciever'] = self.request.GET.get('reciever')
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        setattr(form, 'sender', self.request.user)
        return form

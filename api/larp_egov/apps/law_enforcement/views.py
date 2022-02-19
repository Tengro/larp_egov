from django.views.generic.list import ListView

from larp_egov.apps.law_enforcement.models import (
    MisconductReport, MisconductType
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_filters.views import FilterView
from larp_egov.apps.law_enforcement.filters import MisconductReportFilter
from larp_egov.apps.accounts.models import UserAccount
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from larp_egov.apps.law_enforcement.forms import MisconductReportModelForm


class AllMisconductTypes(LoginRequiredMixin, ListView):
    model = MisconductType

    template_name = 'law_enforcement/misconduct_types.html'


class PersonalFiledMisconducts(LoginRequiredMixin, ListView):
    model = MisconductReport

    template_name = 'law_enforcement/personal_filed_misconducts.html'

    def get_queryset(self):
        user = self.request.user
        return MisconductReport.objects.filter(reporter=user)


class PersonalMiscondutReports(LoginRequiredMixin, ListView):
    model = MisconductReport

    template_name = 'law_enforcement/personal_misconducts.html'

    def get_queryset(self):
        user = self.request.user
        return MisconductReport.objects.filter(reported_person=user)


class PoliceMisconductDashboard(LoginRequiredMixin, UserPassesTestMixin, FilterView):
    model = MisconductReport

    template_name = 'law_enforcement/police_dashboard.html'
    filterset_class = MisconductReportFilter

    def test_func(self):
        return self.request.user.is_police


class SecurityPoliceAllUserAccounts(LoginRequiredMixin, UserPassesTestMixin, ListView):
    queryset = UserAccount.objects.exclude(is_corporate_fiction_account=True).exclude(is_fiction_account=True)

    template_name = 'law_enforcement/user_dashboard.html'
    context_object_name = 'person_list'

    def test_func(self):
        return self.request.user.is_police_or_security


class PoliceCommentView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    queryset = UserAccount.objects.exclude(is_corporate_fiction_account=True).exclude(is_fiction_account=True)
    fields = ['police_comment_field', ]
    template_name = 'law_enforcement/user_police_comment.html'
    success_url = reverse_lazy("law_enforcement:account_list")
    success_message = _("Comment successfully updated")
    slug_field = 'character_id'
    slug_url_kwarg = 'character_id'

    def test_func(self):
        return self.request.user.is_police


class SecurityCommentView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    queryset = UserAccount.objects.exclude(is_corporate_fiction_account=True).exclude(is_fiction_account=True)
    fields = ['security_comment_field', ]
    template_name = 'law_enforcement/user_security_comment.html'
    success_url = reverse_lazy("law_enforcement:account_list")
    success_message = _("Comment successfully updated")
    slug_field = 'character_id'
    slug_url_kwarg = 'character_id'

    def test_func(self):
        return self.request.user.is_security


class FileMisconductReportView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = MisconductReportModelForm
    template_name = 'law_enforcement/file_misconduct_report.html'
    success_url = reverse_lazy("law_enforcement:filed_personal_reports")
    success_message = _("Report successfully filed")

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(FileMisconductReportView, self).get_form_kwargs()
        kwargs['initial']['reported_person'] = self.request.GET.get('reported_person')
        return kwargs


class PoliceFrozenSumEditView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    queryset = UserAccount.objects.exclude(is_corporate_fiction_account=True).exclude(is_fiction_account=True)
    fields = ['frozen_sum', ]
    template_name = 'law_enforcement/user_freeze_police.html'
    success_url = reverse_lazy("law_enforcement:account_list")
    success_message = _("Frozen sum successfully updated")
    slug_field = 'character_id'
    slug_url_kwarg = 'character_id'

    def test_func(self):
        return self.request.user.is_police

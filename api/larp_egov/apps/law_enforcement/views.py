from django.views.generic.list import ListView

from larp_egov.apps.law_enforcement.models import (
    MisconductReport, MisconductType
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from larp_egov.apps.law_enforcement.filters import MisconductReportFilter


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


class PoliceMisconductDashboard(LoginRequiredMixin, FilterView):
    model = MisconductReport

    template_name = 'law_enforcement/police_dashboard.html'
    filterset_class = MisconductReportFilter


# TODO: Add police views (all misconducts + filtering), add_report

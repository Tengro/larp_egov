import django_filters
from larp_egov.apps.law_enforcement.models import MisconductReport
from larp_egov.apps.accounts.models import UserAccount


class MisconductReportFilter(django_filters.FilterSet):
    officer_in_charge = django_filters.ModelChoiceFilter(queryset=UserAccount.objects.get_police_officers())

    class Meta:
        model = MisconductReport
        fields = [
            'reporter', 'reported_person', 'officer_in_charge',
            'misconduct_status', 'penalty_status', 'misconduct_type'
        ]

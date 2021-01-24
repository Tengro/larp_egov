import django_filters
from larp_egov.apps.law_enforcement.models import MisconductReport


class MisconductReportFilter(django_filters.FilterSet):

    class Meta:
        model = MisconductReport
        fields = [
            'reporter', 'reported_person', 'officer_in_charge',
            'misconduct_status', 'penalty_status', 'misconduct_type'
        ]

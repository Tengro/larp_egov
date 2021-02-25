from larp_egov.apps.law_enforcement.models import MisconductReport
from django.forms import ModelForm
from django.core.exceptions import ValidationError


class MisconductReportModelForm(ModelForm):
    class Meta:
        model = MisconductReport
        fields = ('reported_person', 'misconduct_type')

    def clean_reported_person(self):
        reported_person = self.cleaned_data['reported_person']
        if (reported_person.is_corporate_fiction_account or reported_person.is_fiction_account or reported_person.is_service_account):
            raise ValidationError(_("You can't report misconducts on service accounts directly!"))
        return reported_person

    def save(self):
        report = super().save()
        if report.misconduct_type.suggested_penalty:
            report.penalty_amount = report.misconduct_type.suggested_penalty
            report.save()
        report.send_report_notifications()
        return report

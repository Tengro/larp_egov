from larp_egov.apps.law_enforcement.models import MisconductReport
from django.forms import ModelForm, CharField
from django.core.exceptions import ValidationError
from larp_egov.apps.accounts.selectors import get_user_by_character_id
from django.utils.translation import ugettext_lazy as _


class MisconductReportModelForm(ModelForm):
    reported_person = CharField()

    class Meta:
        model = MisconductReport
        fields = ('reported_person', 'misconduct_type')

    def clean_reported_person(self):
        reported_person = self.cleaned_data['reported_person']
        reported_person = get_user_by_character_id(reported_person)
        if not reported_person:
            raise ValidationError(_("Користувач з таким ID не знайдений. Скарга не надіслана"))
        if (reported_person.is_corporate_fiction_account or reported_person.is_fiction_account or reported_person.is_service_account):
            raise ValidationError(_("Ви не можете надсилати скарги на технічні акаунти"))
        return reported_person

    def save(self):
        report = super().save()
        if report.misconduct_type.suggested_penalty:
            report.penalty_amount = report.misconduct_type.suggested_penalty
            report.save()
        report.send_report_notifications()
        return report

from django.db import models
from larp_egov.apps.common.models import CoreModel, CoreManager, CoreQuerySet
from larp_egov.apps.accounts.models import UserAccount
from django_extensions.db.fields import RandomCharField


class MisconductReportStatus(models.IntegerChoices):
    SENT = 0, "Report sent"
    REVISED = 1, "Report revised"
    DECLINED = 2, "Report declined"
    PROCESSED = 3, "Report is being processed"
    FINISHED = 4, "Report is finished"


class MisconductPenaltyStatus(models.IntegerChoices):
    OPEN = 0, "Penalty open"
    PROCESSED = 1, "Penalty is active"
    CLOSED = 2, "Penalty is paid"
    CLOSED_UNPAID = 3, "Closed without payment"


class MisconductType(CoreModel):
    title = models.CharField(max_length=512)
    misconduct_code = models.CharField(max_length=8)
    suggested_penalty = models.DecimalField(max_digits=12, decimal_places=1, null=True,  blank=True)

    def __str__(self):
        return self.title

    @property
    def display_data(self):
        return f"{self.title}; code: {self.misconduct_code}"


class MisconductReport(CoreModel):
    reporter = models.ForeignKey(UserAccount, related_name='reported_misconducts',  null=True, on_delete=models.SET_NULL)
    reported_person = models.ForeignKey(UserAccount, related_name='misconduct_record', null=True, on_delete=models.SET_NULL)
    officer_in_charge = models.ForeignKey(UserAccount, related_name='assigned_misconducts', null=True,  on_delete=models.SET_NULL)
    misconduct_status = models.IntegerField(choices=MisconductReportStatus.choices, default=MisconductReportStatus.SENT)
    penalty_amount = models.DecimalField(max_digits=12, decimal_places=1, null=True, blank=True)
    penalty_status = models.IntegerField(choices=MisconductPenaltyStatus.choices, default=MisconductPenaltyStatus.OPEN)
    misconduct_type = models.ForeignKey(MisconductType, related_name='existing_misconducts', on_delete=models.CASCADE)
    misconduct_id = RandomCharField(length=10, include_alpha=False, unique=True, null=True)

    def __str__(self):
        return f"{self.reporter} report on {self.reported_person} accused in {self.misconduct_type.title}."

    @property
    def police_record_string(self):
        reporter_string = f"Reporter: {self.reporter}."
        reported_person = f"Reported: {self.reported_person}."
        misconduct_type = f'Misconduct: {self.misconduct_type}.'
        penalty = f"Penalty amount: {self.penalty_amount}."
        report_status = f"Report status: {self.misconduct_status.label}."
        penalty_status = f"Penalty status: {self.penalty_status}."
        report_id = f"Report ID: {self.misconduct_id}"
        result = f"{reporter_string}\n{reported_person}\n{misconduct_type}\n{penalty}\n{report_status}\n{penalty_status}\n{report_id}"
        if officer_in_charge:
            result += f"\nOfficer in charge: {self.officer_in_charge}."
        return result

    @property
    def anonymised_string(self):
        reported_person = f"Reported: {self.reported_person}."
        misconduct_type = f'Misconduct: {self.misconduct_type}.'
        penalty = f"Penalty amount: {self.penalty_amount}."
        report_status = f"Report status: {self.misconduct_status.label}."
        penalty_status = f"Penalty status: {self.penalty_status}."
        report_id = f"Report ID: {self.misconduct_id}"
        result = f"{reporter_string}\n{reported_person}\n{misconduct_type}\n{penalty}\n{report_status}\n{penalty_status}\n{report_id}"
        if officer_in_charge:
            result += f"\nOfficer in charge: {self.officer_in_charge.full_name}."
        return result


    @classmethod
    def create_misconduct_report(cls, reporter, reported_person, misconduct_type, penalty_amount=None):
        if not penalty_amount:
            penalty_amount = misconduct_type.suggested_penalty
        item = cls.objects.create(
            reporter=reporter,
            reported_person=reported_person,
            misconduct_type=misconduct_type,
            penalty_amount=penalty_amount
        )
        item.notify_unassigmnent_status(text=f'Misconduct report {item.misconduct_id} of the misconduct {misconduct_type.title} was created!')
        creation_message = f'Misconduct report for {misconduct_type.title} id {item.misconduct_id} was filed'
        reporter.send_message(creation_message)
        reported_person.send_message(creation_message)

    @classmethod
    def create_tax_related_report(cls, reported_person, penalty_amount):
        misconduct_type = MisconductType.objects.get_or_create(misconduct_code='TAX_FAIL')
        service_account = UserAccount.objects.get_service_account()
        cls.create_misconduct_report(service_account, reported_person, misconduct_type, penalty_amount)

    def notify_unassigmnent_status(self, text=''):
        if not text:
            text = f'Misconduct report {self.misconduct_id} unassigned!'
        for item in UserAccount.objects.get_police_officers():
            item.send_message(text)

    def notify_officer(self, text):
        if self.officer_in_charge:
            self.officer_in_charge.send_message(text)
        return

    def notify_unrevised_report(self):
        if self.officer_in_charge and self.misconduct_status == MisconductReportStatus.REVISED:
            self.notify_officer(f"Misconduct {self.misconduct_id} still on revision; decline or process it!")

    def notify_unprocessed_report(self):
        if self.officer_in_charge and self.misconduct_status == MisconductReportStatus.PROCESSED:
            self.notify_officer(f"Misconduct {self.misconduct_id} still in process!")

    def assign_report(self, user):
        if not user.is_police:
            raise ValueError('Can\'t assign report to someone not in police')
        if self.officer_in_charge:
            self.notify_officer(f'Misconduct report {self.misconduct_id} was reassigned to {user}')
        self.officer_in_charge = user
        if self.misconduct_status < MisconductReportStatus.REVISED:
            self.misconduct_status = MisconductReportStatus.REVISED
        assignment_message = f"Misconduct report {self.misconduct_id} assigned. Officer in charge: {user.full_name}."
        self.reporter.send_message(assignment_message)
        self.reported_person.send_message(assignment_message)
        self.save()

    def decline_report(self):
        closure_message = f"Misconduct report {self.misconduct_id} was declined."
        self.reported_person.send_message(closure_message)
        self.notify_officer(closure_message)
        self.penalty_status = MisconductPenaltyStatus.CLOSED
        self.misconduct_status = MisconductReportStatus.DECLINED
        self.save()

    def process_report(self):
        if self.misconduct_status < MisconductReportStatus.PROCESSED:
            self.misconduct_status = MisconductReportStatus.PROCESSED
        self.save()

    def finish_report(self):
        if self.penalty_status == MisconductPenaltyStatus.PROCESSED:
            self.notify_officer('Penalty hasn\'t been processed! Closing without payment')
            self.penalty_status = MisconductPenaltyStatus.CLOSED_UNPAID
        if self.misconduct_status < MisconductReportStatus.FINISHED:
            self.misconduct_status = MisconductReportStatus.FINISHED
        self.reported_person.send_message(f"Misconduct {self.misconduct_id} finalized.")
        self.notify_officer(f"Misconduct {self.misconduct_id} finalized.")
        self.save()

    def set_penalty(self, penalty=None):
        if not penalty:
            penalty = self.misconduct_type.suggested_penalty
        if self.misconduct_status != MisconductReportStatus.PROCESSED:
            self.notify_officer('Can\'t set penalty for not processed orders!')
            return
        self.penalty_status == MisconductPenaltyStatus.PROCESSED
        self.penalty_amount = penalty
        penalty_message = f"Penalty for misconduct report {self.misconduct_id} assigned. Penalty: {self.penalty_amount}"
        self.reported_person.send_message(penalty_message)
        self.notify_officer(penalty_message)
        self.save()

    def set_auto_penalty(self):
        self.set_penalty(self.misconduct_type.suggested_penalty)

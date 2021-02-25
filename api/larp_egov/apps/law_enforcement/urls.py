from django.urls import path
from larp_egov.apps.law_enforcement.views import (
    AllMisconductTypes, PersonalFiledMisconducts, PersonalMiscondutReports,
    PoliceMisconductDashboard, SecurityPoliceAllUserAccounts,
    PoliceCommentView, SecurityCommentView, FileMisconductReportView
)


urlpatterns = [
    path("misconduct-types/", AllMisconductTypes.as_view(), name="all_misconducts"),
    path("me/reports/", PersonalMiscondutReports.as_view(), name="personal_reports"),
    path("me/filed-reports/", PersonalFiledMisconducts.as_view(), name="filed_personal_reports"),
    path("me/file-report/", FileMisconductReportView.as_view(), name="file_report"),
    path("misconduct-dashboard/", PoliceMisconductDashboard.as_view(), name="misconduct_dashboard"),
    path("registerd-person-list/", SecurityPoliceAllUserAccounts.as_view(), name="account_list"),
    path("comment/<int:character_id>/police/", PoliceCommentView.as_view(), name="police_comment_edit"),
    path("comment/<int:character_id>/security/", SecurityCommentView.as_view(), name="security_comment_edit"),
]

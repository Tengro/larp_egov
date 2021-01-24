from django.urls import path
from larp_egov.apps.law_enforcement.views import (
    AllMisconductTypes, PersonalFiledMisconducts, PersonalMiscondutReports,
    PoliceMisconductDashboard,
)


urlpatterns = [
    path("misconduct-types/", AllMisconductTypes.as_view(), name="all_misconducts"),
    path("me/reports/", PersonalMiscondutReports.as_view(), name="personal_reports"),
    path("me/filed-reports/", PersonalFiledMisconducts.as_view(), name="filed_personal_reports"),
    path("misconduct-dashboard/", PoliceMisconductDashboard.as_view(), name="misconduct_dashboard"),
]

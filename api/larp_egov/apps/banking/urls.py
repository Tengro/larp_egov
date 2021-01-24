from django.urls import path
from larp_egov.apps.banking.views import (
    AllCorporationList, AllSubscriptionsList, PersonalCorporationMembership,
    PersonalSubscriptionList, PersonalTransactionList
)


urlpatterns = [
    path("corporations/", AllCorporationList.as_view(), name="all_corporations"),
    path("subscriptions/", AllSubscriptionsList.as_view(), name="subscriptions"),
    path("me/corporations/", PersonalCorporationMembership.as_view(), name="personal_corporations"),
    path("me/subscriptions/", PersonalSubscriptionList.as_view(), name="personal_subscriptions"),
    path("me/transactions/", PersonalTransactionList.as_view(), name="personal_transactions"),
]

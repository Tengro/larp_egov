from django.urls import path
from larp_egov.apps.accounts.views import (
    register, UserProfileView, AtomLoginView,
    CommonHelpView, SearchView, PublicProfileView
)
from django.contrib.auth import views as auth_views

# from larp_egov.apps.accounts.api.v1.views.login import LoginView, LogoutView
# from larp_egov.apps.accounts.api.v1.views.password import (
#     ChangePasswordAPIView,
#     ConfirmResetPasswordAPIView,
#     ResetPasswordAPIView,
# )
# from larp_egov.apps.accounts.api.v1.views.registration import RegistrationAPIView
# from larp_egov.apps.accounts.api.v1.views.user_profile import UserProfileAPIView


urlpatterns = [
    # path("login/", LoginView.as_view(), name="login"),
    # path("logout/", LogoutView.as_view(), name="logout"),
    # path("me/", UserProfileAPIView.as_view(), name="user-profile"),
    # path("password/", ChangePasswordAPIView.as_view(), name="change-password"),
    # path("password/confirm/", ConfirmResetPasswordAPIView.as_view(), name="confirm-reset-password"),
    # path("password/reset/", ResetPasswordAPIView.as_view(), name="reset-password"),
    path("registration/", register, name="registration"),
    path("login/", AtomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("help/", CommonHelpView.as_view(), name="help"),
    path('search-result/', SearchView.as_view(), name='search'),
    path('public-profile/<slug:character_id>/', PublicProfileView.as_view(), name='public_profile')
]

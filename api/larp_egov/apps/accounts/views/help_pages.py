from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django_telegrambot.apps import DjangoTelegramBot
from django.contrib.auth.mixins import UserPassesTestMixin


class CommonHelpView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/help.html"
    login_url = reverse_lazy('accounts:login')


class PoliceHelpView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "accounts/police_help.html"
    login_url = reverse_lazy('accounts:login')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_police


class SecurityHelpView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "accounts/security_help.html"
    login_url = reverse_lazy('accounts:login')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_security

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django_telegrambot.apps import DjangoTelegramBot
from django.contrib.auth.mixins import UserPassesTestMixin


class CommonHelpView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/help.html"
    login_url = reverse_lazy('accounts:login')

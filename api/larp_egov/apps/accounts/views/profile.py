from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django_telegrambot.apps import DjangoTelegramBot


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"
    login_url = reverse_lazy('accounts:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        if not user.telegram_id:
            context['bot_name'] = DjangoTelegramBot.dispatcher.bot.name
        return context

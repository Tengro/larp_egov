from django.views.generic import TemplateView, View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django_telegrambot.apps import DjangoTelegramBot
from larp_egov.apps.accounts.models import UserAccount


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"
    login_url = reverse_lazy('accounts:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.telegram_id:
            context['bot_name'] = DjangoTelegramBot.dispatcher.bot.name
        return context


class SearchView(ListView):
    model = UserAccount
    template_name = 'accounts/search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        result = UserAccount.objects.exclude(is_corporate_fiction_account=True).exclude(is_fiction_account=True)
        query = self.request.GET.get('search')
        if query:
            result = result.filter(character_id__contains=query)
        else:
            result = None
        return result


class PublicProfileView(LoginRequiredMixin, DetailView):
    template_name = "accounts/public_profile.html"
    login_url = reverse_lazy('accounts:login')
    model = UserAccount
    slug_field = 'character_id'
    slug_url_kwarg = 'character_id'
    context_object_name = 'person'

    def get_queryset(self):
        return UserAccount.objects.exclude(is_corporate_fiction_account=True).exclude(is_fiction_account=True)

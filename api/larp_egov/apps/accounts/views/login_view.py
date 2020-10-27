from django.contrib.auth.views import LoginView


class AtomLoginView(LoginView):
    template_name = 'accounts/login.html'

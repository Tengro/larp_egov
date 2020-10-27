from django.urls import reverse_lazy
from larp_egov.apps.accounts.forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: not u.is_authenticated)
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse_lazy('accounts:profile'))
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

from django.views.generic.edit import FormView
from larp_egov.apps.accounts.forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            return redirect('deeplink')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

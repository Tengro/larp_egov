from django.views.generic.edit import FormView
from larp_egov.apps.accounts.forms import RegisterForm
from django.contrib import messages
from django.shortcuts import render, redirect


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('deeplink')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

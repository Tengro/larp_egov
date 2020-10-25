from django import forms
from django.contrib.auth.forms import UserCreationForm
from larp_egov.apps.accounts.models import UserAccount


class RegisterForm(UserCreationForm):

    class Meta:
        model = UserAccount
        fields = ["email", "first_name", "last_name", "password1", "password2"]

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

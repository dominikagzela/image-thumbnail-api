from django import forms
from .models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class LoginUserForm(forms.Form):
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(max_length=30)
    password = forms.CharField(min_length=4, max_length=20,
                               widget=forms.PasswordInput)

    # def clean_password(self):
    #     cd = super().clean()
    #     username = cd.get('username')
    #     password = cd.get('password')
    #     user = authenticate(username=username, password=password)
    #     if user is None:
    #         raise ValidationError('Email or password is incorrect!')
    #     return password

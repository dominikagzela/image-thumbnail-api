from django import forms
from .models import User, TierImage
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator


class LoginUserForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


# class TierImageForm(forms.ModelForm):
#     duration = forms.IntegerField()
#
#     class Meta:
#         model = TierImage
#         fields = ['upload_file', 'duration']
#
#     def clean_duration(self):
#         duration = self.cleaned_data['duration']
#         tier = self.cleaned_data['tier']
#         if tier.expiring_links and (duration < 300 or duration > 400):
#             raise forms.ValidationError('Duration should be between 300 and 400.')
#         return duration

class TierImageForm(forms.ModelForm):
    class Meta:
        model = TierImage
        fields = ['upload_file', 'duration']
        widgets = {
            'upload_file': forms.ClearableFileInput(attrs={'required': True}),
            'duration': forms.NumberInput(attrs={'required': True}),
        }
        labels = {
            'upload_file': 'Image',
            'duration': 'Duration (in seconds)',
        }
        help_texts = {
            'duration': 'Enter a number between 300 and 300.000',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # get the logged-in user from the view
        super().__init__(*args, **kwargs)
        if user and user.tier and not user.tier.expiring_links:
            self.fields['duration'].widget = forms.HiddenInput()
            self.fields['duration'].required = False

    def clean_duration(self):
        duration = self.cleaned_data['duration']
        if duration is not None and not (300 <= duration <= 300000):
            raise ValidationError('Duration should be a number between 300 and 300000')
        return duration

    # def clean_duration(self):
    #     user = self.request.user  # get the logged-in user from the form
    #     duration = self.cleaned_data['duration']
    #     if user and user.tier and not user.tier.expiring_links and not duration:
    #         raise forms.ValidationError('This field is required.')
    #     return duration

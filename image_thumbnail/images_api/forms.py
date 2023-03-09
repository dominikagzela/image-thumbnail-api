from django import forms
from .models import TierImage
from django.core.exceptions import ValidationError


class LoginUserForm(forms.Form):
    """
    Login User form that allows a user to log in with their username and password.
    """
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class TierImageForm(forms.ModelForm):
    """
    Tier Image form that allows a user to upload an image associated with their account tier.
    """
    class Meta:
        model = TierImage
        fields = ['upload_file', 'duration']
        widgets = {
            'upload_file': forms.ClearableFileInput(attrs={'required': True,
                                                           'accept': '.jpg, .png'}),

            'duration': forms.NumberInput(attrs={'required': True,
                                                 'min': '300',
                                                 'max': '300000'}),
        }
        labels = {
            'upload_file': 'Image',
            'duration': 'Duration (in seconds)',
        }
        help_texts = {
            'upload_file': 'Upload image in .jpg or .png format',
            'duration': 'Enter a number between 300 and 300000',
        }
        error_messages = {
            'upload_file': {
                'invalid_image': 'Please upload a valid JPG or PNG image file.'},
            'duration': {
                'invalid_duration': 'Please enter the number between 300 and 300000'}
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.tier and not user.tier.expiring_links:
            self.fields['duration'].widget = forms.HiddenInput()
            self.fields['duration'].required = False

    def clean_upload_file(self):
        upload_file = self.cleaned_data.get('upload_file')
        if upload_file:
            if not upload_file.name[-4:].lower() in ('.jpg', '.png'):
                raise forms.ValidationError('Uploaded image should be in JPG or PNG format')
        return upload_file

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if duration is not None and not (300 <= duration <= 300000):
            raise ValidationError('Duration should be a number between 300 and 300000')
        return duration

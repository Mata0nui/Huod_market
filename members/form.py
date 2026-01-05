from django import forms
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar', 'password', 'email')
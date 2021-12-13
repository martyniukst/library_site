from django.forms import ModelForm
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','middle_name','last_name','email']
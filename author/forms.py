from django.forms import ModelForm
from .models import Author
from django import forms


class CreateAuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name','surname','patronymic']
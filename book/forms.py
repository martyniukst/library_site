from django.forms import ModelForm
from .models import Book


class CreateBookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name','authors','description','count']

class UpdateBookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name','description','count']
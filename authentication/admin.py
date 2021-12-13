from django.contrib import admin
from book.models import Book
from .models import CustomUser
from author.models import Author
from order.models import Order

admin.site.register(Book)
admin.site.register(CustomUser)
admin.site.register(Author)
admin.site.register(Order)
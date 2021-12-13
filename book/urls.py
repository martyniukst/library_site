from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.all_books, name='all_books'),
    path('create_book/', views.create_book, name='create_book'),
    path('<int:id>/', views.show_book_by_id, name='book_id'),
    path('delete_book/<int:id>/', views.delete_book, name='delete_book'),
    path('update_book/<int:id>/', views.update_book, name='update_book'),
    path('unordered_book/', views.unordered_book, name='unordered_book'),

]

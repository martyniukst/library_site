from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.all_authors, name='all_authors'),
    path('create_author/', views.create_author, name='create_author'),
    path('<int:id>/', views.show_author_by_id, name='author_id'),
    path('delete_author/<int:id>/', views.delete_author, name='delete_author'),
    path('update_author/<int:id>/', views.update_author, name='update_author'),
]

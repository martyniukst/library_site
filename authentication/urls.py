from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_all_users, name='all_users'),
    path('create_user/', views.create_user, name='create_user'),
    path('<int:id>/', views.show_user_by_id, name='user_id'),
    path('<int:id>/order/', views.user_order, name='order'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('update_user/<int:id>/', views.update_user, name='update_user'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.log_out, name='logout')
]

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.show_all_orders, name='all_orders'),
    path('create_order/', views.create_order, name='create_order'),
    path('<int:id>/', views.show_order_by_id, name='order_id'),
    path('delete_order/<int:id>/', views.delete_order, name='delete_order'),
    path('update_order/<int:id>/', views.update_order, name='update_order'),
    path('expired_order/', views.show_expired_order, name='expired_order'),
]

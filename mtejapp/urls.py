from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name="home"),
    path('products/',views.products, name="products"),
    path('customer/<str:pk>', views.customer, name="customer"),
    path('create_order', views.createOrder, name="create_order"),
    path('update/<str:pk>', views.orderUpdate, name='update'),
    path('deleteOrder/<str:pk>', views.deleteOrder, name="delete"),
    path('createCustomer', views.createUser, name="createCustomer"),
    path('updateCustomer/<str:pk>', views.updateUser, name="updateC"),
    path('deleteCustomer/<str:pk>/', views.deleteUser, name='deleteC')


    ]
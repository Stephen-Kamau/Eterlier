from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.homePageView, name='home'),
    path('eterly/create/', views.create_Eterly, name='create_Eterly'),
    path('eterly/verify/', views.eterly_verification, name='eterly_verification'),
    path('branch/create/', views.create_branch, name='create_branch'),
    path('branch/', views.get_all_my_branches, name='get_all_my_branches'),
    path('addcat/', views.add_food_category, name='add_food_category'),
    path('addsubcat/', views.add_food_sub_category, name='add_food_sub_category'),
    path('add/', views.add_food_product, name='add_food_sub_category'),


    path('order-product/', views.orderProduct, name='order_product'),
]

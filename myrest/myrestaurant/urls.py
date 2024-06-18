# myrestaurant/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category-list'),
    path('myrestaurant/', views.category_list, name='category-list'),
    path('category/<int:category_id>/', views.category_detail, name='category-detail'),
    path('myrestaurant/basket/', views.view_basket, name='basket'),
    path('myrestaurant/add-to-basket/', views.add_to_basket, name='add-to-basket'),
    path('api/Baskets/UpdateBasket', views.update_basket, name='update-basket'),
    
]
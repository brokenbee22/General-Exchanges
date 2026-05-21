from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/checkout/', views.checkout, name='checkout'),
    path('orders/<int:order_id>/success/', views.order_success, name='order_success'),
    path('seller/register/', views.seller_register, name='seller_register'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/products/add/', views.add_product, name='add_product'),
    path('seller/products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('seller/products/<int:pk>/delete/', views.delete_product, name='delete_product'),
]

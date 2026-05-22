from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('checkout/<int:pk>/', views.checkout, name='checkout'),

    path('cart/', views.cart_view, name='cart'),
    path('cart/checkout/', views.cart_checkout, name='cart_checkout'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:pk>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),

    path('seller/register/', views.seller_register, name='seller_register'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/products/add/', views.add_product, name='add_product'),
    path('seller/products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('seller/products/<int:pk>/delete/', views.delete_product, name='delete_product'),

    path('order/<int:order_id>/success/', views.order_success, name='order_success'),
]
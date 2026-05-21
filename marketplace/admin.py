from django.contrib import admin
from .models import Order, OrderItem, Product, SellerProfile


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'city', 'state', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'state', 'city')
    search_fields = ('business_name', 'user__username', 'city')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'price', 'unit', 'quantity_available', 'city', 'is_active')
    list_filter = ('category', 'unit', 'is_active', 'state', 'city')
    search_fields = ('name', 'description', 'material_type', 'seller__business_name')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'quantity', 'unit', 'price_at_purchase', 'line_total')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer_name', 'seller', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('buyer_name', 'buyer_email', 'seller__business_name', 'tracking_number')
    inlines = [OrderItemInline]

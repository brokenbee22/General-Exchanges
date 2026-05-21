from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Seller info is separate from the regular user account.
# I did it like this so sellers can log in normally, but still have business details.
class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50, default='Texas')
    business_address = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name


# Product listing for raw materials.
# This is still simple on purpose, but it has the main fields a seller would need.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('wood', 'Wood'),
        ('steel', 'Steel'),
        ('cement', 'Cement'),
        ('bricks', 'Bricks'),
        ('sand', 'Sand'),
        ('gravel', 'Gravel'),
        ('plywood', 'Plywood'),
        ('drywall', 'Drywall'),
        ('roofing', 'Roofing'),
        ('pvc', 'PVC'),
        ('copper', 'Copper'),
        ('aluminum', 'Aluminum'),
        ('other', 'Other'),
    ]

    UNIT_CHOICES = [
        ('piece', 'Piece'),
        ('pallet', 'Pallet'),
        ('bag', 'Bag'),
        ('ton', 'Ton'),
        ('linear_ft', 'Linear Foot'),
        ('sq_ft', 'Square Foot'),
        ('bundle', 'Bundle'),
    ]

    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    material_type = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)
    quantity_available = models.PositiveIntegerField()
    minimum_order_quantity = models.PositiveIntegerField(default=1)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50, default='Texas')
    delivery_notes = models.TextField(blank=True, help_text='Example: freight delivery, local delivery, pickup, etc.')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})


# Basic order model for the checkout flow.
# No real card payments yet. For now it works like a test checkout / order request.
class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('accepted', 'Accepted by Seller'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    buyer_name = models.CharField(max_length=120)
    buyer_email = models.EmailField()
    buyer_phone = models.CharField(max_length=30, blank=True)
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    shipping_address = models.TextField()
    delivery_notes = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    tracking_carrier = models.CharField(max_length=80, blank=True)
    tracking_number = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} - {self.buyer_name}'


# Each order can have products inside it.
# I kept this even though checkout starts with one product, because later carts can reuse it.
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order, Product


# Form for a business that wants to sell on the site.
class SellerRegistrationForm(UserCreationForm):
    business_name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=30)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=50, initial='Texas')
    business_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Seller product form.
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'description',
            'material_type',
            'price',
            'unit',
            'quantity_available',
            'minimum_order_quantity',
            'city',
            'state',
            'delivery_notes',
            'image',
            'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'delivery_notes': forms.Textarea(attrs={'rows': 3}),
        }


# Buyer checkout form. This is not charging a card yet.
class CheckoutForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = Order
        fields = [
            'buyer_name',
            'buyer_email',
            'buyer_phone',
            'shipping_address',
            'delivery_notes',
            'quantity',
        ]
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3}),
            'delivery_notes': forms.Textarea(attrs={'rows': 3}),
        }

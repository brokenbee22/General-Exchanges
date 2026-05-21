from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CheckoutForm, ProductForm, SellerRegistrationForm
from .models import Order, OrderItem, Product, SellerProfile


def home(request):
    # main page where buyers browse products from approved sellers
    products = Product.objects.filter(is_active=True, seller__is_approved=True)

    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    city = request.GET.get('city', '').strip()

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(material_type__icontains=query)
            | Q(seller__business_name__icontains=query)
        )

    if category:
        products = products.filter(category=category)

    if city:
        products = products.filter(city__icontains=city)

    return render(request, 'marketplace/home.html', {
        'products': products,
        'category_choices': Product.CATEGORY_CHOICES,
        'selected_category': category,
        'query': query,
        'city': city,
    })


def product_detail(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk,
        is_active=True,
        seller__is_approved=True
    )

    return render(request, 'marketplace/product_detail.html', {
        'product': product
    })


def checkout(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk,
        is_active=True,
        seller__is_approved=True
    )

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            if quantity < product.minimum_order_quantity:
                form.add_error('quantity', f'Minimum order is {product.minimum_order_quantity}.')

            elif quantity > product.quantity_available:
                form.add_error('quantity', 'That quantity is higher than what the seller has available.')

            else:
                subtotal = product.price * Decimal(quantity)

                # General Exchange takes 5% from the seller payout.
                # Buyer does not see this as an extra fee.
                platform_fee = (subtotal * Decimal('0.05')).quantize(Decimal('0.01'))
                seller_payout = subtotal - platform_fee

                order = form.save(commit=False)
                order.seller = product.seller
                order.subtotal = subtotal
                order.platform_fee = platform_fee
                order.total = subtotal
                order.save()

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    quantity=quantity,
                    unit=product.get_unit_display(),
                    price_at_purchase=product.price,
                    line_total=subtotal,
                )

                product.quantity_available -= quantity
                product.save()

                messages.success(
                    request,
                    'Order placed. This is a test checkout, so no real payment was charged.'
                )

                return redirect('order_success', order_id=order.id)

    else:
        form = CheckoutForm(initial={'quantity': product.minimum_order_quantity})

    quantity = request.POST.get('quantity') or product.minimum_order_quantity

    try:
        quantity = int(quantity)
    except ValueError:
        quantity = product.minimum_order_quantity

    subtotal = product.price * Decimal(quantity)

    # Keep this calculated for backend/seller logic, but do not show it to the buyer.
    platform_fee = (subtotal * Decimal('0.05')).quantize(Decimal('0.01'))
    seller_payout = subtotal - platform_fee

    return render(request, 'marketplace/checkout.html', {
        'form': form,
        'product': product,
        'subtotal': subtotal,
        'total': subtotal,
        'seller_payout': seller_payout,
    })


def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    return render(request, 'marketplace/order_success.html', {
        'order': order
    })


def seller_register(request):
    # seller signs up, then I approve the account manually in admin
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            SellerProfile.objects.create(
                user=user,
                business_name=form.cleaned_data['business_name'],
                phone_number=form.cleaned_data['phone_number'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                business_address=form.cleaned_data['business_address'],
            )

            login(request, user)

            messages.success(
                request,
                'Seller account created. An admin needs to approve it before products go live.'
            )

            return redirect('seller_dashboard')

    else:
        form = SellerRegistrationForm()

    return render(request, 'marketplace/seller_register.html', {
        'form': form
    })


@login_required
def seller_dashboard(request):
    seller = get_object_or_404(SellerProfile, user=request.user)
    products = seller.products.all()
    orders = seller.orders.all()

    return render(request, 'marketplace/seller_dashboard.html', {
        'seller': seller,
        'products': products,
        'orders': orders,
    })


@login_required
def add_product(request):
    seller = get_object_or_404(SellerProfile, user=request.user)

    if not seller.is_approved:
        messages.warning(
            request,
            'Your seller account needs admin approval before adding products.'
        )
        return redirect('seller_dashboard')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = seller
            product.save()

            messages.success(request, 'Product added successfully.')
            return redirect('seller_dashboard')

    else:
        form = ProductForm(initial={
            'city': seller.city,
            'state': seller.state
        })

    return render(request, 'marketplace/product_form.html', {
        'form': form,
        'title': 'Add Product'
    })


@login_required
def edit_product(request, pk):
    seller = get_object_or_404(SellerProfile, user=request.user)
    product = get_object_or_404(Product, pk=pk)

    if product.seller != seller:
        raise PermissionDenied

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('seller_dashboard')

    else:
        form = ProductForm(instance=product)

    return render(request, 'marketplace/product_form.html', {
        'form': form,
        'title': 'Edit Product'
    })


@login_required
def delete_product(request, pk):
    seller = get_object_or_404(SellerProfile, user=request.user)
    product = get_object_or_404(Product, pk=pk)

    if product.seller != seller:
        raise PermissionDenied

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('seller_dashboard')

    return render(request, 'marketplace/delete_product.html', {
        'product': product
    })

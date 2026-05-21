from pathlib import Path
from shutil import copyfile

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from marketplace.models import Product, SellerProfile


class Command(BaseCommand):
    help = 'Adds one fake steel seller/listing so the homepage is not empty.'

    def handle(self, *args, **options):
        # This is just sample data for testing the marketplace locally.
        username = 'conroe_steel_demo'
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': 'demo@generalexchanges.local',
                'first_name': 'Demo',
                'last_name': 'Seller',
            },
        )

        if created:
            user.set_password('demo12345')
            user.save()

        seller, _ = SellerProfile.objects.get_or_create(
            user=user,
            defaults={
                'business_name': 'Conroe Steel Supply Co.',
                'phone_number': '936-555-0198',
                'city': 'Conroe',
                'state': 'Texas',
                'business_address': '100 Demo Yard Rd, Conroe, TX',
                'is_approved': True,
            },
        )

        # If the seller already existed but was not approved, approve it for the demo.
        if not seller.is_approved:
            seller.is_approved = True
            seller.save()

        media_products = Path(settings.MEDIA_ROOT) / 'products'
        media_products.mkdir(parents=True, exist_ok=True)

        source_img = Path(settings.BASE_DIR) / 'media' / 'products' / 'conroe_steel_demo.jpg'
        final_img = media_products / 'conroe_steel_demo.jpg'

        if source_img.exists() and not final_img.exists():
            copyfile(source_img, final_img)

        product, created = Product.objects.get_or_create(
            seller=seller,
            name='Galvanized Steel Beams Bundle',
            defaults={
                'category': 'steel',
                'description': 'Fictional demo listing for galvanized steel beams sold by a local supplier in Conroe, Texas. Good placeholder listing for testing the marketplace layout.',
                'material_type': 'Galvanized steel',
                'price': '1295.00',
                'unit': 'bundle',
                'quantity_available': 18,
                'minimum_order_quantity': 1,
                'city': 'Conroe',
                'state': 'Texas',
                'delivery_notes': 'Fictional seller-managed delivery. Local delivery available around Conroe and Houston area. Freight required for larger orders.',
                'image': 'products/conroe_steel_demo.jpg',
                'is_active': True,
            },
        )

        if not product.image:
            product.image = 'products/conroe_steel_demo.jpg'
            product.save()

        self.stdout.write(self.style.SUCCESS('Demo steel listing is ready. Refresh the homepage.'))

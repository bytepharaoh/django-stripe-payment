# payments/management/commands/create_sample_data.py
# Create this file structure: payments/management/commands/create_sample_data.py
# Also create __init__.py in both management and commands folders

from django.core.management.base import BaseCommand
from payments.models import Item, Discount, Tax, Order


class Command(BaseCommand):
    help = 'Creates sample data for testing the application'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create Items
        items_data = [
            {
                'name': 'Premium Headphones',
                'description': 'High-quality wireless headphones with noise cancellation',
                'price': 299.99,
                'currency': 'usd'
            },
            {
                'name': 'Smart Watch',
                'description': 'Fitness tracker with heart rate monitor and GPS',
                'price': 199.99,
                'currency': 'usd'
            },
            {
                'name': 'Laptop Stand',
                'description': 'Ergonomic aluminum laptop stand for better posture',
                'price': 49.99,
                'currency': 'usd'
            },
            {
                'name': 'Mechanical Keyboard',
                'description': 'RGB backlit mechanical keyboard with blue switches',
                'price': 149.99,
                'currency': 'usd'
            },
            {
                'name': 'Wireless Mouse',
                'description': 'Ergonomic wireless mouse with precision tracking',
                'price': 79.99,
                'currency': 'usd'
            },
        ]

        items = []
        for item_data in items_data:
            item, created = Item.objects.get_or_create(
                name=item_data['name'],
                defaults=item_data
            )
            items.append(item)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created item: {item.name}'))
            else:
                self.stdout.write(f'  Item already exists: {item.name}')

        # Create Discounts
        discounts_data = [
            {
                'name': 'Summer Sale',
                'code': 'SUMMER20',
                'discount_type': 'percentage',
                'value': 20.00,
                'active': True
            },
            {
                'name': 'New Customer',
                'code': 'WELCOME10',
                'discount_type': 'fixed',
                'value': 10.00,
                'active': True
            },
        ]

        for discount_data in discounts_data:
            discount, created = Discount.objects.get_or_create(
                code=discount_data['code'],
                defaults=discount_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created discount: {discount.code}'))
            else:
                self.stdout.write(f'  Discount already exists: {discount.code}')

        # Create Taxes
        taxes_data = [
            {
                'name': 'US Sales Tax',
                'rate': 8.50,
                'country': 'US',
                'active': True
            },
            {
                'name': 'EU VAT',
                'rate': 20.00,
                'country': 'EU',
                'active': True
            },
        ]

        for tax_data in taxes_data:
            tax, created = Tax.objects.get_or_create(
                name=tax_data['name'],
                country=tax_data['country'],
                defaults=tax_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created tax: {tax.name}'))
            else:
                self.stdout.write(f'  Tax already exists: {tax.name}')

        # Create sample orders
        if len(items) >= 3:
            order, created = Order.objects.get_or_create(
                id=1,
                defaults={
                    'status': 'pending',
                    'discount': Discount.objects.filter(code='SUMMER20').first(),
                    'tax': Tax.objects.filter(country='US').first(),
                }
            )
            if created:
                order.items.add(items[0], items[2])  # Headphones + Laptop Stand
                self.stdout.write(self.style.SUCCESS('✓ Created sample order #1'))
            else:
                self.stdout.write('  Order #1 already exists')

        self.stdout.write(self.style.SUCCESS('\n✅ Sample data creation complete!'))
        self.stdout.write('\nYou can now:')
        self.stdout.write('1. View items at http://localhost:8000/')
        self.stdout.write('2. Access admin at http://localhost:8000/admin/')
        self.stdout.write('3. Test payments with Stripe test cards')
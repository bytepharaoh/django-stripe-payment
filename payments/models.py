from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Item(models.Model):
    """
    Represents a purchasable item in the store.
    """
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]
    
    name = models.CharField(max_length=200, help_text="Item name")
    description = models.TextField(help_text="Item description")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Price in selected currency"
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='usd',
        help_text="Currency for this item"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return f"{self.name} - {self.get_display_price()}"

    def get_display_price(self):
        """Returns formatted price with currency symbol"""
        symbols = {'usd': '$', 'eur': '€'}
        symbol = symbols.get(self.currency, self.currency.upper())
        return f"{symbol}{self.price}"

    def get_stripe_price(self):
        """Returns price in cents for Stripe API"""
        return int(self.price * 100)


class Discount(models.Model):
    """
    Represents a discount that can be applied to orders.
    """
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    name = models.CharField(max_length=100, help_text="Discount name")
    code = models.CharField(max_length=50, unique=True, help_text="Discount code")
    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default='percentage'
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Percentage (0-100) or fixed amount"
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'

    def __str__(self):
        if self.discount_type == 'percentage':
            return f"{self.name} ({self.code}) - {self.value}%"
        return f"{self.name} ({self.code}) - ${self.value}"

    def calculate_discount(self, amount):
        """Calculate discount amount based on type"""
        if self.discount_type == 'percentage':
            return (amount * self.value) / 100
        return self.value


class Tax(models.Model):
    """
    Represents a tax rate that can be applied to orders.
    """
    name = models.CharField(max_length=100, help_text="Tax name (e.g., VAT, Sales Tax)")
    rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Tax rate as percentage (e.g., 20 for 20%)"
    )
    country = models.CharField(max_length=2, help_text="ISO country code (e.g., US, GB)")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['country', 'name']
        verbose_name = 'Tax'
        verbose_name_plural = 'Taxes'

    def __str__(self):
        return f"{self.name} ({self.country}) - {self.rate}%"

    def calculate_tax(self, amount):
        """Calculate tax amount"""
        return (amount * self.rate) / 100


class Order(models.Model):
    """
    Represents an order containing multiple items.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    items = models.ManyToManyField(Item, related_name='orders')
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    tax = models.ForeignKey(
        Tax,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

    def get_subtotal(self):
        """Calculate subtotal (sum of all items)"""
        return sum(item.price for item in self.items.all())

    def get_discount_amount(self):
        """Calculate discount amount"""
        if self.discount and self.discount.active:
            return self.discount.calculate_discount(self.get_subtotal())
        return 0

    def get_tax_amount(self):
        """Calculate tax amount (after discount)"""
        if self.tax and self.tax.active:
            amount_after_discount = self.get_subtotal() - self.get_discount_amount()
            return self.tax.calculate_tax(amount_after_discount)
        return 0

    def get_total(self):
        """Calculate total amount (subtotal - discount + tax)"""
        subtotal = self.get_subtotal()
        discount = self.get_discount_amount()
        tax = self.get_tax_amount()
        return subtotal - discount + tax

    def get_currency(self):
        """Get currency from first item (assumes all items same currency)"""
        first_item = self.items.first()
        return first_item.currency if first_item else 'usd'
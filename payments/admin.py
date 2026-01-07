from django.contrib import admin
from .models import Item, Discount, Tax, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Admin interface for Item model
    """
    list_display = ['name', 'price', 'currency', 'created_at']
    list_filter = ['currency', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Item Information', {
            'fields': ('name', 'description', 'price', 'currency')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """
    Admin interface for Discount model
    """
    list_display = ['name', 'code', 'discount_type', 'value', 'active', 'created_at']
    list_filter = ['discount_type', 'active', 'created_at']
    search_fields = ['name', 'code']
    ordering = ['name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Discount Information', {
            'fields': ('name', 'code', 'discount_type', 'value', 'active')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    """
    Admin interface for Tax model
    """
    list_display = ['name', 'rate', 'country', 'active', 'created_at']
    list_filter = ['country', 'active', 'created_at']
    search_fields = ['name', 'country']
    ordering = ['country', 'name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Tax Information', {
            'fields': ('name', 'rate', 'country', 'active')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


class OrderItemInline(admin.TabularInline):
    """
    Inline display for items in an order
    """
    model = Order.items.through
    extra = 1
    verbose_name = "Order Item"
    verbose_name_plural = "Order Items"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for Order model
    """
    list_display = ['id', 'status', 'get_total_display', 'items_count', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'stripe_session_id']
    ordering = ['-created_at']
    readonly_fields = ['stripe_session_id', 'created_at', 'updated_at', 'display_totals']
    
    filter_horizontal = ['items']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('status', 'items')
        }),
        ('Pricing', {
            'fields': ('discount', 'tax', 'display_totals')
        }),
        ('Payment', {
            'fields': ('stripe_session_id',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def items_count(self, obj):
        """Display number of items in order"""
        return obj.items.count()
    items_count.short_description = 'Items'

    def get_total_display(self, obj):
        """Display formatted total"""
        currency_symbols = {'usd': '$', 'eur': '€'}
        currency = obj.get_currency()
        symbol = currency_symbols.get(currency, currency.upper())
        return f"{symbol}{obj.get_total():.2f}"
    get_total_display.short_description = 'Total'

    def display_totals(self, obj):
        """Display breakdown of totals"""
        if obj.pk:  # Only show if object is saved
            subtotal = obj.get_subtotal()
            discount = obj.get_discount_amount()
            tax = obj.get_tax_amount()
            total = obj.get_total()
            
            currency_symbols = {'usd': '$', 'eur': '€'}
            currency = obj.get_currency()
            symbol = currency_symbols.get(currency, currency.upper())
            
            return (
                f"Subtotal: {symbol}{subtotal:.2f}\n"
                f"Discount: -{symbol}{discount:.2f}\n"
                f"Tax: +{symbol}{tax:.2f}\n"
                f"Total: {symbol}{total:.2f}"
            )
        return "Save the order first to see totals"
    display_totals.short_description = 'Price Breakdown'
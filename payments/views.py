import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item, Order

# Initialize Stripe with secret key
stripe.api_key = settings.STRIPE_SECRET_KEY


def item_detail(request, id):
    """
    Display item detail page with buy button
    GET /item/{id}
    """
    item = get_object_or_404(Item, id=id)
    
    context = {
        'item': item,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    
    return render(request, 'payments/item_detail.html', context)


def create_checkout_session(request, id):
    """
    Create Stripe Checkout Session for an item
    GET /buy/{id}
    Returns JSON with session ID
    """
    try:
        item = get_object_or_404(Item, id=id)
        
        # Determine success and cancel URLs
        domain = request.build_absolute_uri('/')[:-1]  # Remove trailing slash
        success_url = f"{domain}/success/"
        cancel_url = f"{domain}/cancel/"
        
        # Create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                    'unit_amount': item.get_stripe_price(),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        
        return JsonResponse({'id': session.id})
        
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def order_detail(request, id):
    """
    Display order detail page with buy button
    GET /order/{id}
    """
    order = get_object_or_404(Order, id=id)
    
    context = {
        'order': order,
        'items': order.items.all(),
        'subtotal': order.get_subtotal(),
        'discount_amount': order.get_discount_amount(),
        'tax_amount': order.get_tax_amount(),
        'total': order.get_total(),
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    
    return render(request, 'payments/order_detail.html', context)


def create_order_checkout_session(request, id):
    """
    Create Stripe Checkout Session for an order
    GET /buy/order/{id}
    Returns JSON with session ID
    """
    try:
        order = get_object_or_404(Order, id=id)
        
        # Determine success and cancel URLs
        domain = request.build_absolute_uri('/')[:-1]
        success_url = f"{domain}/success/"
        cancel_url = f"{domain}/cancel/"
        
        # Build line items for all items in order
        line_items = []
        for item in order.items.all():
            line_items.append({
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                    'unit_amount': item.get_stripe_price(),
                },
                'quantity': 1,
            })
        
        # Prepare session parameters
        session_params = {
            'payment_method_types': ['card'],
            'line_items': line_items,
            'mode': 'payment',
            'success_url': success_url,
            'cancel_url': cancel_url,
        }
        
        # Add discount if available
        if order.discount and order.discount.active:
            discount_amount = int(order.get_discount_amount() * 100)  # Convert to cents
            if discount_amount > 0:
                # Create a coupon for this discount
                coupon = stripe.Coupon.create(
                    amount_off=discount_amount,
                    currency=order.get_currency(),
                    duration='once',
                    name=order.discount.name,
                )
                session_params['discounts'] = [{'coupon': coupon.id}]
        
        # Add tax if available
        if order.tax and order.tax.active:
            # Create tax rate
            tax_rate = stripe.TaxRate.create(
                display_name=order.tax.name,
                percentage=float(order.tax.rate),
                inclusive=False,
            )
            # Apply tax to all line items
            for line_item in session_params['line_items']:
                line_item['tax_rates'] = [tax_rate.id]
        
        # Create session
        session = stripe.checkout.Session.create(**session_params)
        
        # Update order with session ID
        order.stripe_session_id = session.id
        order.save()
        
        return JsonResponse({'id': session.id})
        
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def success(request):
    """Success page after payment"""
    return render(request, 'payments/success.html')


def cancel(request):
    """Cancel page if payment is cancelled"""
    return render(request, 'payments/cancel.html')


def home(request):
    """Home page showing all items"""
    items = Item.objects.all()
    return render(request, 'payments/home.html', {'items': items})
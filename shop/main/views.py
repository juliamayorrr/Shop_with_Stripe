import stripe
from django.contrib.sessions.models import Session
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from shop import settings
from .models import Item, Order, Discount
from .utils import get_active_order


stripe.api_key = settings.STRIPE_SECRET_KEY

def item(request, id):
    item = get_object_or_404(Item, pk=id)
    data = {
        'title': 'Item',
        'item': item,
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'main/item.html', data)


def cart(request):
    data = {
        'title': 'Cart',
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    order = get_active_order(request)
    if order:
        data['order'] = order
        data['items'] = order.items.all()

    return render(request, 'main/cart.html', data)


def cart_add(request, id):
    if request.method == 'POST':
        item = get_object_or_404(Item, pk=id)
        order = get_active_order(request)
        if order:
            if order.currency != item.currency:
                messages.warning(request, 'You can only add items with same currency to your cart.')
                return redirect('cart')
        else:
            order = Order.objects.create(currency=item.currency, session_key=request.session.session_key)
            request.session['order_id'] = order.pk

        if order.items.filter(pk=item.pk).exists():
            messages.info(request, 'Item already in cart')
        else:
            order.items.add(item)
            order.calculate_total()

        return redirect('cart')


def cart_remove(request, id):
    if request.method == 'POST':
        item = get_object_or_404(Item, pk=id)
        order = get_active_order(request)
        if order:
            order.items.remove(item)
            if order.items.exists():
                order.calculate_total()
            else:
                order.delete()
                del request.session['order_id']

        return redirect('cart')


def buy_item(request, id):
    item = get_object_or_404(Item, pk=id)
    order = Order.objects.create(currency=item.currency)
    order.items.add(item)
    order.calculate_total()

    intent = stripe.PaymentIntent.create(
        amount=order.get_stripe_amount(),
        currency=order.currency
    )

    order.stripe_payment_intent_id = intent.id
    order.save()

    return JsonResponse({'clientSecret': intent.client_secret})


def buy_cart(request):
    order = get_active_order(request)
    if not order or not order.items.exists():
        return JsonResponse({'error': 'Cart is empty'}, status=400)

    intent = stripe.PaymentIntent.create(
        amount=order.get_stripe_amount(),
        currency=order.currency
    )

    order.stripe_payment_intent_id = intent.id
    order.save()

    return JsonResponse({'clientSecret': intent.client_secret})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        order = Order.objects.get(stripe_payment_intent_id=intent['id'])
        order.status = Order.Status.PAID
        order.save()

        if order.session_key:
            try:
                session = Session.objects.get(session_key=order.session_key)
                session_data = session.get_decoded()

                if 'order_id' in session_data:
                    del session_data['order_id']
                    session.session_data = Session.objects.encode(session_data)
                    session.save()
            except Session.DoesNotExist:
                pass

    elif event['type'] == 'payment_intent.payment_failed':
        intent = event['data']['object']
        order = Order.objects.get(stripe_payment_intent_id=intent['id'])
        if not order.session_key:
            order.status = Order.Status.FAILED
            order.save()


    return HttpResponse(status=200)


def success_payment(request):
    messages.info(request, 'The order has been successfully placed')

    return redirect('cart')


def apply_promo(request):
    pass
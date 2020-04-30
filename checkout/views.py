from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents

import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, 'There is nothing in your bag right now')
        return redirect(reverse('products'))
    
    current_bag = bag_contents(request)
    total = current_bag['grand-total']
    stripe_total = round(total * 180)
    stripe.api_key = stripe_secret_key
    stripe.PaymentIntent.create(
        amount=stripe_total,
        curreny=settings.STRIPE_CURRENCY,
    )

    print(intent)

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_C9HJQ1QFL2S9E9LgiOW3oXDq00PPJmu2U5',
        'client_secret': 'test client secret',

    }
    return render(request, template, context)

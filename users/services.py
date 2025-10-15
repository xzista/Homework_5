import requests
import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_dollars(amount):
    """Конвертирует рубли в доллары"""
    api_url = 'https://open.er-api.com/v6/latest/RUB'

    response = requests.get(api_url, timeout=5)
    data = response.json()
    rate = data['rates']['USD']
    return amount * rate


def create_stripe_session(payment):
    """Создает сессию на оплату в Stripe"""

    amount_rub = payment.amount

    amount_cents = convert_rub_to_dollars(amount_rub)

    product_name = f"{payment.paid_object._meta.verbose_name}: {payment.paid_object}"
    product = stripe.Product.create(name=product_name)

    price = stripe.Price.create(
        currency="usd",
        unit_amount=amount_cents,
        product=product.id,
    )

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{'price': price.id, 'quantity': 1}],
        mode='payment',
        success_url=f"http://127.0.0.1:8000/payments/{payment.id}/success/",
        cancel_url=f"http://127.0.0.1:8000/payments/{payment.id}/cancel/",
    )

    return session.id, session.url
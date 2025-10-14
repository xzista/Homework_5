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


def create_stripe_price(amount):
    """Создает цену в Stripe"""
    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        # recurring={"interval": "month"},
        product_data={"name": "Gold Plan"},
    )


def create_stripe_session(price):
    """Создает сессию на оплату в Stripe"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/success",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id", session.get("url"))
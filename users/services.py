import stripe

from config.settings import STRIPE_API_KEY
from pycurrency import converter

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_dollars(amount):
    """Конвертирует рубли в доллары"""
    my_converter = converter.Converter(amount, 'RUB', 'USD')
    return my_converter.result()


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
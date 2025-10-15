from decimal import Decimal

import requests
import stripe
from django.contrib.contenttypes.models import ContentType

from config.settings import STRIPE_API_KEY
from materials.models import Course, Lesson

stripe.api_key = STRIPE_API_KEY


def get_content_type_by_name(content_type_name):
    """Получает ContentType по имени модели"""
    if content_type_name == "course":  # id 7
        return ContentType.objects.get_for_model(Course)
    elif content_type_name == "lesson":  # id 8
        return ContentType.objects.get_for_model(Lesson)
    else:
        raise ValueError(f"Неизвестный тип контента: {content_type_name}")


def convert_rub_to_dollars(amount):
    """Конвертирует рубли в доллары"""
    api_url = "https://open.er-api.com/v6/latest/RUB"

    response = requests.get(api_url, timeout=5)
    data = response.json()
    rate = Decimal(str(data["rates"]["USD"]))
    return amount * rate


def create_stripe_session(payment):
    """Создает сессию на оплату в Stripe"""

    amount_rub = payment.amount

    amount_cents = int(convert_rub_to_dollars(amount_rub) * 100)

    product_name = f"{payment.paid_object._meta.verbose_name}: {payment.paid_object}"
    product = stripe.Product.create(name=product_name)

    price = stripe.Price.create(
        currency="usd",
        unit_amount=amount_cents,
        product=product.id,
    )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
        success_url=f"http://127.0.0.1:8000/payments/{payment.id}/success/",
        cancel_url=f"http://127.0.0.1:8000/payments/{payment.id}/cancel/",
    )

    return session.id, session.url

import os

import requests
from dotenv import load_dotenv
from rest_framework import status
import stripe

load_dotenv()
apikey = os.getenv("CUR_API_KEY")
url = os.getenv("CUR_API_URL")

stripe.api_key = os.getenv("STRIPE_API_KEY")
stripe.Price.create(
    currency="usd",
    unit_amount=1000,
    recurring={"interval": "month"},
    product_data={"name": "Gold Plan"},
)

stripe.checkout.Session.create(
    success_url="https://example.com/success",
    line_items=[{"price": "price_1MotwRLkdIwHu7ixYcPLm5uZ", "quantity": 2}],
    mode="payment",
)

stripe.Product.create(name="Gold Plan")


def convert_currencies(rub_price):
    usd_price = 0

    response = requests.get(f"{url}v3/latest?apikey={apikey}&currencies=RUB")
    if response.status_code == status.HTTP_200_OK:
        usd_rate = response.json()["data"]["RUB"]["value"]
        usd_price = rub_price * usd_rate
    return usd_price


def create_product():
    return stripe.Product.create(name="Product")


def create_price(amount):
    """Создаёт цену в страйпе"""

    return stripe.Price.create(
        currency="usd",
        unit_amount=amount,
        product_data={"name": "Payment"},
    )


def create_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
